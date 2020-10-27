"""
Summary tables from a PKdata instance.

Tables can be either stored to disk or uploaded to a google spreadsheet.
"""
import logging
from copy import copy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Union

import numpy as np
import pandas as pd

from pkdb_analysis import filter, query_pkdb_data
from pkdb_analysis.data import PKData


# from gspread_pandas import Spread -> removing gspread support for now
Spread = None

logger = logging.getLogger(__name__)


def create_table_report(
    dosing_substances: List,
    report_substances: List,
    studies_content: List = None,
    timecourses_content: List = None,
    pks_content: List = None,
    h5_data_path: Path = None,
    zip_data_path: Path = None,
    excel_path: Path = None,
    tsv_path: Path = None,
    google_sheets: str = None,
    query_data: bool = False,
):
    """Create table report for given substance.

    h5_data_path: PKDB data in HDF5 format (via query function)
    dosing_substances: Set of substances used in Dosing, e.g. {torasemide}
    report_substances: Set of substances in reports

    excel_path: Path to excel file to write the report to
    tsv_path: Path to directory to to which the tsv are written
    google_sheets: Google sheets name for report
    query_data: boolean flag to query the data
    """
    if query_data:
        query_pkdb_data(h5_path=h5_data_path)
    # Load data

    if zip_data_path:
        if not zip_data_path.exists():
            raise IOError(
                f"Zip file does not exist: '{zip_data_path}'. "
                f"Query the data first with the `query_data=True' flag."
            )
        pkdata = PKData.from_archive(zip_data_path)
    elif h5_data_path:
        if not h5_data_path.exists():
            raise IOError(
                f"PKDBData in HDF5 does not exist: '{zip_data_path}'. "
                f"Query the data first with the `query_data=True' flag."
            )
        pkdata = PKData.from_hdf5(h5_data_path)

    # Create table report
    table_report = TableReport(
        pkdata=pkdata,
        substances_output=report_substances,
        substances_intervention=dosing_substances
    )
    table_report.create_tables()

    # serialize table report
    if excel_path is not None:
        table_report.to_excel(excel_path)
    if tsv_path is not None:
        table_report.to_tsv(tsv_path)
    if google_sheets is not None:
        logger.error(
            f"NO SUPPORT FOR GOOGLE SHEETS: see "
            f"https://github.com/matthiaskoenig/pkdb_analysis/issues/36"
        )
        table_report.to_google_sheet(google_sheets)


@dataclass
class Parameter:
    """Helper Class to define how an interactive value can be selected. """

    measurement_types: Union[str, List] = "any"
    value_field: Sequence = "choice"
    substance: str = "any"
    values: Sequence = ("any",)
    only_group: bool = False
    only_individual: bool = False
    groupby: bool = True


class TableReportTypes(Enum):
    """Allowed types of table reports"""

    STUDIES = 1  # overview study content
    TIMECOURSES = 2  # overview timecourse content
    PHARMACOKINETICS = 3  # overview pharmacokinetics content


class TableReport(object):
    """Summary table for a collection of studies in PK-DB.

    Data is provided as PKData object.
    Export formats are table files or google spreadsheets.

    FIXME: allow creation with different backends -> fix hyperlinks
    """
    DEFAULT_STUDY_INFO = {
        "subject_info": {
            "sex": Parameter(measurement_types=["sex"], value_field=["choice"]),
            "age": Parameter(
                measurement_types=["age"], value_field=["mean", "median", "value"]
            ),
            "weight": Parameter(
                measurement_types=["weight"], value_field=["mean", "median", "value"]
            ),
            "height": Parameter(
                measurement_types=["height"], value_field=["mean", "median", "value"]
            ),
            "body mass index": Parameter(
                measurement_types=["bmi"], value_field=["mean", "median", "value"]
            ),
            "ethnicity": Parameter(
                measurement_types=["ethnicity"], value_field=["choice"]
            ),
            # pk effecting factors
            "healthy": Parameter(measurement_types=["healthy"], value_field=["choice"]),
            "medication": Parameter(
                measurement_types=["medication"], value_field=["choice"]
            ),
            "smoking": Parameter(measurement_types=["smoking"], value_field=["choice"]),
            "oral contraceptives": Parameter(
                measurement_types=["oral contraceptives"], value_field=["choice"]
            ),
            "overnight fast": Parameter(
                measurement_types=["overnight fast"], value_field=["choice"]
            ),
            "CYP1A2 genotype": Parameter(
                measurement_types=["CYP1A2 genotype"], value_field=["choice"]
            ),
            "abstinence alcohol": Parameter(
                measurement_types=["abstinence alcohol"],
                value_field=["mean", "median", "value", "min", "max"],
            ),
        },
        "intervention_info": {
            "dosing amount": Parameter(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["value"],
            ),
            "dosing route": Parameter(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["route"],
            ),
            "dosing form": Parameter(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["form"]
            ),
        },
        "output_info": {
            "quantification method": Parameter(
                measurement_types="any", value_field=["method"]
            )
        }
    }

    @staticmethod
    def _timecourse_info_default(substances) -> Dict:

        timecourse_fields = {
            "individual": {"value_field": ["value"], "only_individual": True},
            "group": {"value_field": ["mean", "median"], "only_group": True},
            "error": {"value_field": ["sd", "se", "cv"], "only_group": True},
            "plasma": {
                "value_field": ["tissue"],
                "values": ["plasma", "blood", "serum"],
                "groupby": False,
            },
            "urine": {"value_field": ["tissue"], "values": ["urine"], "groupby": False},
            "saliva": {
                "value_field": ["tissue"],
                "values": ["saliva"],
                "groupby": False,
            },
        }

        # create info dict for all substances
        timecourse_info = {}
        for substance in substances:
            for key, p_kwargs in timecourse_fields.items():
                this_key = f"{substance}_{key}"
                timecourse_info[this_key] = Parameter(
                    measurement_types="any", substance=substance, **p_kwargs
                )
        return timecourse_info

    @staticmethod
    def _pharmacokinetic_info_default(substances) -> Dict:
        pks_info = {}
        for substance in substances:
            pks_info_substance = {
                f"{substance}_plasma": Parameter(
                    substance=f"{substance}",
                    value_field=["tissue"],
                    values=["plasma", "blood", "serum"],
                    groupby=False,
                ),
                f"{substance}_urine": Parameter(
                    substance=f"{substance}",
                    value_field=["tissue"],
                    values=["urine"],
                    groupby=False,
                ),
                f"{substance}_saliva": Parameter(
                    substance=f"{substance}",
                    value_field=["tissue"],
                    values=["saliva"],
                    groupby=False,
                ),
                f"{substance}_vd_individual": Parameter(
                    measurement_types=["vd"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_vd_group": Parameter(
                    measurement_types=["vd"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_vd_error": Parameter(
                    measurement_types=["vd"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_clearance_individual": Parameter(
                    measurement_types=["clearance"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_clearance_group": Parameter(
                    measurement_types=["clearance"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_clearance_error": Parameter(
                    measurement_types=["clearance"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_auc_individual": Parameter(
                    measurement_types=["auc_end", "auc_inf"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_auc_group": Parameter(
                    measurement_types=["auc_end", "auc_inf"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_auc_error": Parameter(
                    measurement_types=["auc_end", "auc_inf"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_thalf_individual": Parameter(
                    measurement_types=["thalf"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_thalf_group": Parameter(
                    measurement_types=["thalf"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_thalf_error": Parameter(
                    measurement_types=["thalf"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_cmax_individual": Parameter(
                    measurement_types=["cmax"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_cmax_group": Parameter(
                    measurement_types=["cmax"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_cmax_error": Parameter(
                    measurement_types=["cmax"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_tmax_individual": Parameter(
                    measurement_types=["tmax"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_tmax_group": Parameter(
                    measurement_types=["tmax"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_tmax_error": Parameter(
                    measurement_types=["tmax"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_kel_individual": Parameter(
                    measurement_types=["kel"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_kel_group": Parameter(
                    measurement_types=["kel"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_kel_error": Parameter(
                    measurement_types=["kel"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
            }
            pks_info = {**pks_info, **pks_info_substance}
        return pks_info

    def __init__(self,
                 pkdata: PKData,
                 substances_output: Iterable = None,
                 substances_intervention: Iterable = None,
                 study_info: Dict = DEFAULT_STUDY_INFO,
                 timecourse_info: Dict = None,
                 pharmacokinetic_info: Dict = None,

                 ):


        # filter intervention substances
        # FIXME: better filtering
        study_sids = pkdata.filter_intervention(
            f_idx=filter.f_substance_in, substances=substances_intervention, concise=False
        ).interventions.study_sids
        pkdata = pkdata.filter_study(lambda x: x["sid"].isin(study_sids), concise=False)

        self.pkdata = pkdata
        tmp_pkdata = pkdata.copy()
        tmp_pkdata._concise()
        self.pkdata_concised = tmp_pkdata

        self.substances_intervention = substances_intervention
        self.substances = substances_output if substances_output is not None else tuple()
        self.study_info = study_info
        self.timecourse_info = timecourse_info if timecourse_info is not None else self._timecourse_info_default(substances_output)
        self.pharmacokinetic_info = pharmacokinetic_info if pharmacokinetic_info is not None else self._pharmacokinetic_info_default(substances_output)

        self.df_studies = None
        self.df_timecourses = None
        self.df_pharmacokinetics = None


    @staticmethod
    def _create_path(path_output):
        """Create folder."""
        if not path_output.exists():
            logger.warning(f"Path created: '{path_output.resolve()}'")
            path_output.mkdir()

    def to_excel(self, path_excel: Path):
        """Write all tables excel file."""
        self._create_path(path_excel.parent)

        sheets = {
            "studies": self.df_studies,
            "timecourses": self.df_timecourses,
            "pharmacokinetics": self.df_pharmacokinetics,
        }

        with pd.ExcelWriter(path_excel) as writer:
            for key, df in sheets.items():
                df1 = df.copy()
                # hyperlink replacements:
                df1["PKDB"] = df1["PKDB"].apply(
                    lambda x: f'=HYPERLINK("https://alpha.pk-db.com/data/{x}", "{x}")'
                )
                df1["pubmed"] = df1["pubmed"].apply(
                    lambda x: f'=HYPERLINK("https://www.ncbi.nlm.nih.gov/pubmed/{x}", "{x}")'
                )

                df1.to_excel(writer, sheet_name=key, index=False)

    def to_google_sheet(self, google_sheets: str):
        """Write all tables to google calc.

        **Google Spreadsheets**
        Set the `google_sheets` argument to use this option. The admin needs to
        create a google sheet in his google drive account.
        The name of the sheet has to be entered as the `google_sheets` argument.

        IMPORTANT:
        For google sheets to work, ask admin for the google_secret.json and
        copy it in your local config folder.
            cp  ~/.config/gspread_pandas/google_secret.json

        FOR ADMIN:
            1. Go to the Google APIs Console -> https://console.developers.google.com/
            2. Create a new project.
            3. Click Enable API and Services. Search for and enable the Google Drive API.
               Click Enable API and Services. Search for and enable the Google Sheets API.
            4. Create credentials for a Web Server to access Application Data.
            5. Name the service account and grant it a Project Role of Editor.
            6. Download the JSON file.
            7. Copy the JSON file to your code directory and rename it to google_secret.json
        """
        header_start = "A4"
        header_size = 4

        for report_type in [
            TableReportTypes.STUDIES,
            TableReportTypes.TIMECOURSES,
            TableReportTypes.PHARMACOKINETICS,
        ]:
            if report_type == TableReportTypes.STUDIES:
                table_df = self.df_studies
            elif report_type == TableReportTypes.TIMECOURSES:
                table_df = self.df_timecourses
            elif report_type == TableReportTypes.PHARMACOKINETICS:
                table_df = self.df_pharmacokinetics
                header_start = "A5"
                header_size = 5

            # hyperlink replacements:
            df = df.copy()
            df["PKDB"] = df["PKDB"].apply(
                lambda x: f'=HYPERLINK("https://alpha.pk-db.com/data/{x}";"{x}")'
            )
            df["pubmed"] = df["pubmed"].apply(
                lambda x: f'=HYPERLINK("https://www.ncbi.nlm.nih.gov/pubmed/{x}";"{x}")'
            )
            sheet_name = report_type.name.lower().capitalize()
            logger.info(f"Writing: {google_sheets}.{sheet_name}")
            spread = Spread(google_sheets)
            sheet = spread.find_sheet(sheet_name)
            sheet.resize(header_size, len(df.columns))

            spread.df_to_sheet(
                df,
                index=False,
                headers=False,
                sheet=sheet_name,
                start=header_start,
                replace=False,
            )

    def to_tsv(self, path_output: Path, suffix="tsv", sep="\t", index=None, **kwargs):
        """Write all sheets to TSV."""
        self._create_path(path_output)

        self.df_studies.to_csv(
            path_output / f"studies.{suffix}", sep=sep, index=index, **kwargs
        )
        self.df_pharmacokinetics.to_csv(
            path_output / f"pharmacokinetics.{suffix}", sep=sep, index=index, **kwargs
        )
        self.df_timecourses.to_csv(
            path_output / f"timecourses.{suffix}", sep=sep, index=index, **kwargs
        )

    def create_tables(self, content):
        """Creates all output tables in given output_path."""
        self.df_studies = self.create_table(
            report_type=TableReportTypes.STUDIES
        )
        self.df_timecourses = self.create_table(
            report_type=TableReportTypes.TIMECOURSES
        )
        self.df_pharmacokinetics = self.create_table(
            report_type=TableReportTypes.PHARMACOKINETICS
        )

    def create_table(self, report_type: TableReportTypes) -> pd.DataFrame:
        """Creates a summary table from PKData.

        :param: substances: iterable of PKDB substance ids for filtering of data
        """
        if not isinstance(report_type, TableReportTypes):
            raise ValueError(
                f"'report_type' must be TableReportTypes, but "
                f"is: {type(report_type), report_type}"
            )

        logger.info(f"Create TableReport: {report_type}")

        # create the base table
        table = self.pkdata.studies.df.copy()
        table_keys = ["sid", "name", "reference_pmid"]
        table = table[table_keys]
        table_kwargs = {"table_df": table, "table_keys": table_keys}
        if report_type == TableReportTypes.STUDIES:
            table = self.studies_table(**table_kwargs)
        elif report_type == TableReportTypes.TIMECOURSES:
            table = self.timecourses_table(**table_kwargs)
        elif report_type == TableReportTypes.PHARMACOKINETICS:
            table = self.pk_table(**table_kwargs)

        # columns rename
        table.rename(columns={
            "sid": "PKDB",
            "reference_pmid": "pubmed",
        }, inplace=True)
        # sort
        table.sort_values(by="name", inplace=True)
        # fill NA
        table.fillna("", inplace=True)

        return table

    def studies_table(self, table_df: pd.DataFrame, table_keys: List[str]) -> pd.DataFrame:
        """
        Changes studies in place.
        Changes study_keys in place.
        """


        # create extended tables for interventions, groups, ...
        table_interventions = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.interventions, self.study_info["intervention_info"]),
            axis=1,
        )
        table_groups = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.groups, self.study_info["subject_info"]),
            axis=1,
        )
        table_groups = table_groups.apply(
            self._add_group_and_individual_size,
            args=(self.pkdata, self.pkdata_concised),
            axis=1,
        )
        table_groups[["subjects", "groups"]] = table_groups[
            ["subjects", "groups"]
        ].astype(int)
        table_keys.extend(["subjects", "groups"])

        table_individuals = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.individuals, self.study_info["subject_info"]),
            axis=1,
        )

        table_outputs = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.outputs,self.study_info["output_info"]),
            axis=1,
        )
        table_timecourses = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.timecourses, self.study_info["output_info"]),
            axis=1,
        )

        # some helpers to keep order of table_keys
        s_keys = list(self.study_info["subject_info"].keys())
        i_keys = list(self.study_info["intervention_info"].keys())
        o_keys = list(self.study_info["output_info"].keys())

        for keys in [s_keys, i_keys, o_keys]:
            table_keys.extend(copy(keys))
            keys.append("sid")  # ?????

        # merge a ton of tables
        table_df = pd.merge(
            table_df,
            self._combine(
                table_groups[[*s_keys, "subjects", "groups"]],
                table_individuals[s_keys],
            ),
            on="sid",
        )
        table_df = pd.merge(table_df, table_interventions[i_keys], on="sid")
        table_df = pd.merge(
            table_df,
            self._combine(table_outputs[o_keys], table_timecourses[o_keys]),
        )

        return table_df[table_keys]

    def timecourses_table(self, table_df: pd.DataFrame, table_keys: List[str]) -> pd.DataFrame:
        """Create timecourse table"""

        table_df = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.timecourses, self.timecourse_info),
            axis=1,
        )
        return table_df[table_keys]

    def pk_table(self, table_df: pd.DataFrame, table_keys: List[str]) -> pd.DataFrame:
        """Create pharmacokinetics table."""


        table_df = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.outputs, self.pharmacokinetic_info),
            axis=1,
        )
        table_keys.extend(self.pharmacokinetic_info.keys())

        return table_df[table_keys]


    @staticmethod
    def _add_group_and_individual_size(
        study,
        pkdata,
        pkdata_concised,
    ):
        additional_dict = {}
        this_table = getattr(pkdata_concised, "groups")
        groups_concised = this_table[this_table.study_sid == study.sid]
        additional_dict["groups"] = len(groups_concised.pks)

        group_df = pkdata.groups.df
        study_group_df = group_df[group_df["study_sid"] == study.sid]
        all_group = study_group_df[study_group_df["group_name"] == "all"]
        subject_size = all_group.group_count.unique()[0]
        additional_dict["subjects"] = subject_size

        return study.append(pd.Series(additional_dict))


    @staticmethod
    def _add_group_all_count(study_df: pd.DataFrame, pkdata: PKData):
        """Adds a column with the group count of the all group for every study.
        Changes study in place.
        """
        # get "all" groups (FIXME: unnecessary repetition)
        all_groups = pkdata.groups_core[pkdata.groups_core["group_name"] == "all"]
        group = all_groups[(all_groups["study_name"] == study_df.name)]

        # check
        assert len(group) == 1, (len(group), study_df.name, group)
        study_df["Group_all_count"] = group["group_count"]


    @staticmethod
    def _add_information(row: pd.Series, table: pd.DataFrame,
                         measurement_types: Dict) -> pd.Series:
        """
        :param row: series with study ids
        :param table: subset of information
        """
        # FIXME: much too complicated

        # apply iterates over all rows -> returns new rows

        # studies_interventions = table_df.apply(
        #     self._add_information,
        #     args=(self.pkdata_concised.interventions, intervention_info),
        #     axis=1,
        # )

        # DataFrame with multiple rows from study table (e.g. multiple groups per study)
        df_sid_subset = table.df[table.study_sid == row.sid]  # type: pd.DataFrame

        d = dict()
        for key, parameter in measurement_types.items():
            d[key] = TableReport._cell_content(
                parameter=parameter,
                df=df_sid_subset,
                instance_id=table.pk
            )

        return row.append(pd.Series(d))

    CELL_NOT_REPORTED = ""
    CELL_REPORTED = "✓"
    CELL_PARTLY_REPORTED = "⅟"

    @staticmethod
    def _cell_content(
        df: pd.DataFrame,
        instance_id: str,
        parameter: Parameter,
        Subjects_groups: int = 0,
        Subjects_individual: int = 0,
    ) -> str:
        """Creates the cell content.

        :param: DataFrame on which is searched, e.g. subset of groups
        :instance_id:
        """
        if len(df) == 0:
            return TableReport.CELL_NOT_REPORTED

        has_info = []
        compare_length = 0

        if parameter.substance != "any":
            df = df[df["substance"] == parameter.substance]

        if parameter.only_group:
            df = df[df["individual_pk"] == -1]
            instance_id = "group_pk"
            compare_length = Subjects_groups

        if parameter.only_individual:
            df = df[df["group_pk"] == -1]
            instance_id = "individual_pk"
            compare_length = Subjects_individual

        if not parameter.groupby:
            instance_id = "study_name"

        for _, instance in df.groupby(instance_id):
            if parameter.measurement_types == "any":
                specific_info = instance
            else:
                specific_info = instance[
                    instance["measurement_type"].isin(parameter.measurement_types)
                ]

            value_types = (
                specific_info[parameter.value_field].applymap(type).stack().unique()
            )

            has_array = False
            for value in value_types:
                if value is tuple:
                    has_array = True
                    choices = {True}

            if not has_array:
                this_series = specific_info[parameter.value_field].max(axis=1)
                choices = set([i for i in this_series.dropna() if i is not None])

            if "any" not in parameter.values:
                choices = choices & set(parameter.values)
            if len(choices) == 0:
                has_info.append(False)
            elif "NR" in set(choices):
                has_info.append(False)
            else:
                has_info.append(True)

        if not any(has_info) or len(has_info) == 0:
            return TableReport.CELL_NOT_REPORTED

        elif all(has_info):
            if compare_length > 0:
                if len(has_info) == compare_length:
                    return TableReport.CELL_REPORTED
            else:
                return TableReport.CELL_REPORTED
        return TableReport.CELL_PARTLY_REPORTED

    @staticmethod
    def _strict_and_logic(series):
        elements = set(series.dropna().values)
        if len(elements) == 1:
            return list(elements)[0]
        else:
            return TableReport.CELL_NOT_REPORTED

    @staticmethod
    def _and_logic(series):
        elements = set(series.dropna().values)
        if len(elements) == 1:
            return list(elements)[0]
        else:
            return TableReport.CELL_PARTLY_REPORTED

    @staticmethod
    def _any_logic(series):
        elements = set([values for values in series.values if values is not None])
        if TableReport.CELL_REPORTED in elements:
            return TableReport.CELL_REPORTED
        else:
            return TableReport.CELL_NOT_REPORTED

    @staticmethod
    def _combine(df1, df2):
        merged = pd.merge(df1, df2, on="sid")

        for column in [c for c in df2.columns if c != "sid"]:
            keys = [f"{column}_x", f"{column}_y"]
            merged[column] = merged[keys].apply(TableReport._and_logic, axis=1)

        return merged[df1.columns]

    @staticmethod
    def _extend_study_keys(study_keys):
        return study_keys.extend(
            [
                "PKDB identifier",
                "Name",
                "PMID",
                "publication date",
                "subjects",
                "groups",
            ]
        )

    @staticmethod
    def _clear_sheat(spread, header_size, column_length):
        spread.update_cells(
            start=(1, header_size),
            end=(1, 1),
            vals=["" for _ in range(0, column_length * 1)],
        )
