"""Summary tables from a PKdata instance.

Tables can be either stored to disk or uploaded to a google spreadsheet.
"""
import logging
from copy import copy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Union

import pandas as pd

from pkdb_analysis import filter, query_pkdb_data
from pkdb_analysis.core import Sid
from pkdb_analysis.data import PKData
from pkdb_analysis.utils import create_parent


Spread = None
logger = logging.getLogger(__name__)


def create_table_report(
    dosing_substances: Iterable[Union[str, Sid]],
    report_substances: Iterable[Union[str, Sid]],
    columns: List[str] = None,
    study_info: Dict = None,
    timecourse_info: Dict = None,
    pharmacokinetic_info: Dict = None,
    pkdata: PKData = None,
    h5_data_path: Path = None,
    zip_data_path: Path = None,
    excel_path: Path = None,
    tsv_path: Path = None,
    nbib_path: Path = None,
    google_sheets: str = None,
    query_data: bool = False,
):
    """Create table report for given substance.

    h5_data_path: PKDB data in HDF5 format (via query function)
    dosing_substances: Set of substances used in Dosing, e.g. {torasemide}
    report_substances: Set of substances in reports

    excel_path: Path to excel file to write the report to
    tsv_dir: Path to directory to to which the tsv are written
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
    elif not pkdata:
        raise IOError(
            f"One of the following arguments must be provided: 'zip_data_path','h5_data_path', or 'pkdata'."
        )

    # Create table report
    table_report = TableReport(
        pkdata=pkdata,
        substances_output=[str(item) for item in report_substances],
        substances_intervention=[str(item) for item in dosing_substances],
        study_info=study_info,
        timecourse_info=timecourse_info,
        pharmacokinetic_info=pharmacokinetic_info,
        columns=columns,
    )
    if nbib_path:
        table_report.pkdata.to_medline(nbib_path)
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
class TableContentDefinition:
    """Helper Class to define how an interactive value can be selected."""

    measurement_types: Union[str, List] = "any"
    value_field: Sequence = "choice"
    substance: Union[str, List] = "any"
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

    FIXME: pubmeds must be ints
    FIXME: change order of name/pmid to name | pmid

    """

    DEFAULT_STUDY_INFO = {
        "subject_info": {
            "sex": TableContentDefinition(
                measurement_types=["sex"], value_field=["choice"]
            ),
            "age": TableContentDefinition(
                measurement_types=["age"], value_field=["mean", "median", "value"]
            ),
            "weight": TableContentDefinition(
                measurement_types=["weight"], value_field=["mean", "median", "value"]
            ),
            "height": TableContentDefinition(
                measurement_types=["height"], value_field=["mean", "median", "value"]
            ),
            "body mass index": TableContentDefinition(
                measurement_types=["bmi"], value_field=["mean", "median", "value"]
            ),
            "ethnicity": TableContentDefinition(
                measurement_types=["ethnicity"], value_field=["choice"]
            ),
            # pk effecting factors
            "healthy": TableContentDefinition(
                measurement_types=["healthy"], value_field=["choice"]
            ),
            "medication": TableContentDefinition(
                measurement_types=["medication"], value_field=["choice"]
            ),
            "smoking": TableContentDefinition(
                measurement_types=["smoking"], value_field=["choice"]
            ),
            "oral contraceptives": TableContentDefinition(
                measurement_types=["oral contraceptives"], value_field=["choice"]
            ),
            "overnight fast": TableContentDefinition(
                measurement_types=["overnight fast"], value_field=["choice"]
            ),
            # "CYP1A2 genotype": Parameter(
            #    measurement_types=["CYP1A2 genotype"], value_field=["choice"]
            # ),
            "abstinence alcohol": TableContentDefinition(
                measurement_types=["abstinence alcohol"],
                value_field=["mean", "median", "value", "min", "max"],
            ),
        },
        "intervention_info": {
            "dosing amount": TableContentDefinition(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["value"],
            ),
            "dosing route": TableContentDefinition(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["route"],
            ),
            "dosing form": TableContentDefinition(
                measurement_types=["dosing", "qualitative dosing"], value_field=["form"]
            ),
        },
        "output_info": {
            "quantification method": TableContentDefinition(
                measurement_types="any", value_field=["method"]
            )
        },
    }

    @staticmethod
    def timecourse_info_default(substances) -> Dict:

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
                timecourse_info[this_key] = TableContentDefinition(
                    measurement_types="any", substance=substance, **p_kwargs
                )
        return timecourse_info

    @staticmethod
    def pharmacokinetic_info_default(substances) -> Dict:
        pks_info = {}
        for substance in substances:
            pks_info_substance = {
                f"{substance}_plasma": TableContentDefinition(
                    substance=f"{substance}",
                    value_field=["tissue"],
                    values=["plasma", "blood", "serum"],
                    groupby=False,
                ),
                f"{substance}_urine": TableContentDefinition(
                    substance=f"{substance}",
                    value_field=["tissue"],
                    values=["urine"],
                    groupby=False,
                ),
                f"{substance}_saliva": TableContentDefinition(
                    substance=f"{substance}",
                    value_field=["tissue"],
                    values=["saliva"],
                    groupby=False,
                ),
                f"{substance}_vd_individual": TableContentDefinition(
                    measurement_types=["vd"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_vd_group": TableContentDefinition(
                    measurement_types=["vd"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_vd_error": TableContentDefinition(
                    measurement_types=["vd"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_clearance_individual": TableContentDefinition(
                    measurement_types=["clearance"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_clearance_group": TableContentDefinition(
                    measurement_types=["clearance"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_clearance_error": TableContentDefinition(
                    measurement_types=["clearance"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_auc_individual": TableContentDefinition(
                    measurement_types=["auc-end", "auc-inf"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_auc_group": TableContentDefinition(
                    measurement_types=["auc-end", "auc-inf"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_auc_error": TableContentDefinition(
                    measurement_types=["auc-end", "auc-inf"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_thalf_individual": TableContentDefinition(
                    measurement_types=["thalf"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_thalf_group": TableContentDefinition(
                    measurement_types=["thalf"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_thalf_error": TableContentDefinition(
                    measurement_types=["thalf"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_cmax_individual": TableContentDefinition(
                    measurement_types=["cmax"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_cmax_group": TableContentDefinition(
                    measurement_types=["cmax"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_cmax_error": TableContentDefinition(
                    measurement_types=["cmax"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_tmax_individual": TableContentDefinition(
                    measurement_types=["tmax"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_tmax_group": TableContentDefinition(
                    measurement_types=["tmax"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_tmax_error": TableContentDefinition(
                    measurement_types=["tmax"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
                f"{substance}_kel_individual": TableContentDefinition(
                    measurement_types=["kel"],
                    substance=f"{substance}",
                    value_field=["value"],
                    only_individual=True,
                ),
                f"{substance}_kel_group": TableContentDefinition(
                    measurement_types=["kel"],
                    substance=f"{substance}",
                    value_field=["mean", "median"],
                    only_group=True,
                ),
                f"{substance}_kel_error": TableContentDefinition(
                    measurement_types=["kel"],
                    substance=f"{substance}",
                    value_field=["sd", "se", "cv"],
                    only_group=True,
                ),
            }
            pks_info = {**pks_info, **pks_info_substance}
        return pks_info

    @staticmethod
    def study_info_default():
        return TableReport.DEFAULT_STUDY_INFO

    def __init__(
        self,
        pkdata: PKData,
        substances_output: Iterable = None,
        substances_intervention: Iterable = None,
        study_info: Dict = None,
        timecourse_info: Dict = None,
        pharmacokinetic_info: Dict = None,
        columns: List[str] = None,
    ):
        self.columns = columns
        self.substances_intervention = substances_intervention
        self.pkdata = pkdata
        self.filter_intervention_substances()
        print(self.pkdata)

        # make a conciced copy of data
        tmp_pkdata = self.pkdata.copy()
        tmp_pkdata._concise()
        self.pkdata_concised = tmp_pkdata
        print(self.pkdata_concised)

        self.substances = (
            substances_output if substances_output is not None else tuple()
        )
        if substances_output:
            self.study_info = (
                study_info if study_info is not None else self.study_info_default()
            )
            self.timecourse_info = (
                timecourse_info
                if timecourse_info is not None
                else self.timecourse_info_default(substances_output)
            )
            self.pharmacokinetic_info = (
                pharmacokinetic_info
                if pharmacokinetic_info is not None
                else self.pharmacokinetic_info_default(substances_output)
            )

        self.df_studies = None
        self.df_timecourses = None
        self.df_pharmacokinetics = None

    def filter_intervention_substances(self):
        """Filter the pkdata instance by for studies in which intervetion_substances where administrated"""
        # substance must occur in intervention
        if self.substances_intervention:
            study_sids = self.pkdata.filter_intervention(
                f_idx=filter.f_substance_in,
                substances=self.substances_intervention,
                concise=False,
            ).interventions.study_sids
            self.pkdata = self.pkdata.filter_study(
                lambda x: x["sid"].isin(study_sids), concise=False
            )

    @staticmethod
    def _create_path(path_output):
        """Create folder."""
        if not path_output.exists():
            logger.warning(f"Path created: '{path_output.resolve()}'")
            path_output.mkdir(parents=True)

    def to_excel(self, path_excel: Path):
        """Write all tables excel file."""
        create_parent(path_excel)

        def add_header_format(hformat):
            hformat.set_bold()
            hformat.set_font_color("white")
            hformat.set_bg_color("#434343")
            hformat.set_align("center")
            hformat.set_align("vcenter")
            return hformat

        sheets = {
            "studies": self.df_studies,
            "timecourses": self.df_timecourses,
            "pharmacokinetics": self.df_pharmacokinetics,
        }
        columns_horizontal = ["name", "PKDB", "pubmed"]

        with pd.ExcelWriter(path_excel, engine="xlsxwriter") as writer:

            for key, df in sheets.items():
                df1 = df.copy()
                # hyperlink replacements:
                df1["PKDB"] = df1["PKDB"].apply(
                    lambda x: f'=HYPERLINK("https://alpha.pk-db.com/data/{x}", "{x}")'
                )
                df1["pubmed"] = df1["pubmed"].apply(
                    lambda x: f'=HYPERLINK("https://www.ncbi.nlm.nih.gov/pubmed/{x}", "{x}")'
                )
                df1.to_excel(
                    writer, sheet_name=key, index=False, startrow=1, header=False
                )

                worksheet = writer.sheets[key]
                workbook = writer.book
                header_format = workbook.add_format()
                header_format = add_header_format(header_format)

                # first row
                worksheet.set_row(0, 160, None)

                green = workbook.add_format()
                green.set_bg_color("#B6D7A8")

                orange = workbook.add_format()
                orange.set_bg_color("#FFD966")

                colsformat_default = workbook.add_format()
                colsformat_default.set_bold()
                colsformat_default.set_align("center")

                href_format = workbook.add_format()
                href_format.set_bold()
                href_format.set_align("center")
                href_format.set_font_color("#3C88E5")

                header_format90 = workbook.add_format()
                header_format90.set_rotation(90)
                header_format90 = add_header_format(header_format90)

                worksheet.set_column(0, 0, 18, colsformat_default)
                worksheet.set_column(1, 2, 18, href_format)

                worksheet.set_column(3, len(df.columns.values), 3, colsformat_default)

                for col_num, col_name in enumerate(df.columns.values):
                    if col_name not in columns_horizontal:
                        worksheet.write(0, col_num, col_name, header_format90)
                    else:
                        worksheet.write(0, col_num, col_name, header_format)

                table_len = len(df) + 2
                worksheet.conditional_format(
                    f"A1:ZZ{table_len}",
                    {
                        "type": "cell",
                        "criteria": "equal to",
                        "value": '"✓"',
                        "format": green,
                    },
                )
                worksheet.conditional_format(
                    f"A1:ZZ{table_len}",
                    {
                        "type": "cell",
                        "criteria": "equal to",
                        "value": '"⅟"',
                        "format": orange,
                    },
                )
            writer.save()

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

    def create_tables(self):
        """Creates all output tables in given output_path."""
        self.df_studies = self.create_table(report_type=TableReportTypes.STUDIES)
        self.df_timecourses = self.create_table(
            report_type=TableReportTypes.TIMECOURSES
        )
        self.df_pharmacokinetics = self.create_table(
            report_type=TableReportTypes.PHARMACOKINETICS
        )

    def base_table(self):
        """Create the base table."""
        table = self.pkdata.studies.df.copy()
        table_keys = ["name", "sid", "reference_pmid"]
        table["reference_pmid"] = table["reference_pmid"].apply(self.int_or_none)
        return table[table_keys]

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
        table = self.base_table()

        if report_type == TableReportTypes.STUDIES:
            table = self.studies_table(table)
        elif report_type == TableReportTypes.TIMECOURSES:
            table = self.timecourses_table(table)
        elif report_type == TableReportTypes.PHARMACOKINETICS:
            table = self.pk_table(table)

        # columns rename
        table.rename(
            columns={
                "sid": "PKDB",
                "reference_pmid": "pubmed",
            },
            inplace=True,
        )
        # sort
        table.sort_values(by="name", inplace=True)
        # fill NA
        table.fillna("", inplace=True)

        return table

    def circos_table(self):
        return self.base_table().apply(
            self.add_counts,
            args=(self.pkdata, self.pkdata_concised, False),
            axis=1,
        )

    def studies_table(self, table_df: pd.DataFrame) -> pd.DataFrame:
        """
        Changes studies in place.
        Changes study_keys in place.
        """

        # create extended tables for interventions, groups, ...

        table_keys = list(table_df.columns)
        table_interventions = table_df.apply(
            self._add_information,
            args=(
                self.pkdata_concised.interventions,
                self.study_info["intervention_info"],
            ),
            axis=1,
        )
        table_groups = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.groups, self.study_info["subject_info"]),
            axis=1,
        )
        table_groups = table_groups.apply(
            self.add_counts,
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
            args=(self.pkdata_concised.outputs, self.study_info["output_info"]),
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
        if self.columns:
            return table_df[self.columns]

        return table_df[table_keys]

    def timecourses_table(self, table_df: pd.DataFrame) -> pd.DataFrame:
        """Create timecourse table"""
        table_keys = list(table_df.columns)

        table_df = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.timecourses, self.timecourse_info),
            axis=1,
        )
        table_keys.extend(self.timecourse_info.keys())

        return table_df[table_keys]

    def pk_table(self, table_df: pd.DataFrame) -> pd.DataFrame:
        """Create pharmacokinetics table."""
        table_keys = list(table_df.columns)

        table_df = table_df.apply(
            self._add_information,
            args=(self.pkdata_concised.outputs, self.pharmacokinetic_info),
            axis=1,
        )
        table_keys.extend(self.pharmacokinetic_info.keys())

        return table_df[table_keys]

    @staticmethod
    def add_counts(
        study,
        pkdata: PKData,
        pkdata_concised: PKData,
        only_groups: bool = True,
    ):
        """Add counts of
        individuals, groups, subjects (group=all -> group_count), interventions, outputs, timecourses, scatters"""
        additional_dict = {}
        if only_groups:
            columns = ["groups"]
        else:
            columns = [
                "groups",
                "individuals",
                "interventions",
                "outputs",
                "timecourses",
            ]
        for column in columns:
            pk_dataframe = getattr(pkdata_concised, column)
            study_pk_dataframe = pk_dataframe[pk_dataframe.study_sid == study.sid]
            additional_dict[column] = len(study_pk_dataframe.pks)
            if column == "outputs":
                additional_dict["outputs_calculated"] = len(
                    study_pk_dataframe[study_pk_dataframe["calculated"]].pks
                )

        group_df = pkdata.groups.df
        study_group_df = group_df[group_df["study_sid"] == study.sid]
        all_group = study_group_df[study_group_df["group_name"] == "all"]
        if len(all_group) == 0:
            additional_dict["subjects"] = 0
        else:
            subject_size = all_group.group_count.unique()[0]
            additional_dict["subjects"] = subject_size

        return study.append(pd.Series(additional_dict))

    @staticmethod
    def int_or_none(s) -> int:
        """"""
        try:
            return int(s)

        except ValueError:
            return None

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
    def _add_information(
        row: pd.Series, table: pd.DataFrame, measurement_types: Dict
    ) -> pd.Series:
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
        for key, content_definition in measurement_types.items():
            d[key] = TableReport._cell_content(
                content_definition=content_definition,
                df=df_sid_subset,
                instance_id=table.pk,
            )

        return row.append(pd.Series(d))

    CELL_NOT_REPORTED = ""
    CELL_REPORTED = "✓"
    CELL_PARTLY_REPORTED = "⅟"

    @staticmethod
    def _cell_content(
        df: pd.DataFrame,
        instance_id: str,
        content_definition: TableContentDefinition,
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

        if content_definition.substance != "any":
            if isinstance(content_definition.substance, List):
                df = df[df["substance"].isin(content_definition.substance)]
            else:
                df = df[df["substance"] == content_definition.substance]

        if content_definition.only_group:
            df = df[df["individual_pk"] == -1]
            instance_id = "group_pk"
            compare_length = Subjects_groups

        if content_definition.only_individual:
            df = df[df["group_pk"] == -1]
            instance_id = "individual_pk"
            compare_length = Subjects_individual

        if not content_definition.groupby:
            instance_id = "study_name"

        for _, instance in df.groupby(instance_id):
            if content_definition.measurement_types == "any":
                specific_info = instance
            else:
                specific_info = instance[
                    instance["measurement_type"].isin(
                        content_definition.measurement_types
                    )
                ]

            value_types = (
                specific_info[content_definition.value_field]
                .applymap(type)
                .stack()
                .unique()
            )

            has_array = False
            for value in value_types:
                if value is tuple:
                    has_array = True
                    choices = {True}

            if not has_array:
                this_series = specific_info[content_definition.value_field].max(axis=1)
                choices = set([i for i in this_series.dropna() if i is not None])

            if "any" not in content_definition.values:
                choices = choices & set(content_definition.values)
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
    def _clear_sheat(spread, header_size, column_length):
        spread.update_cells(
            start=(1, header_size),
            end=(1, 1),
            vals=["" for _ in range(0, column_length * 1)],
        )
