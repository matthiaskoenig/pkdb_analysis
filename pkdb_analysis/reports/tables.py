"""
This module creates summary tables from a pkdata instance.

Tables can be either stored to disk or uploaded to a google spreadsheet.
"""
import logging
from typing import Iterable
from pathlib import Path
from copy import copy
from dataclasses import dataclass

import numpy as np
from pkdb_analysis.data import PKData
import pandas as pd
from typing import Dict, Union, List, Sequence
from gspread_pandas import Spread
from enum import Enum

logger = logging.getLogger(__name__)

@dataclass
class Parameter:
    """
    FIXME: Document

    """
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
    """ Summary table for a collection of studies in PK-DB.

    Data is provided as PKData object.
    Export formats are table files or google spreadsheets.

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
    def __init__(self, pkdata: PKData, substances: Iterable=None):
        self.pkdata = pkdata
        if substances is None:
            substances = tuple()
        self.substances = substances

    def create_tables(self, output_path: Path, google_sheets: str=None):
        """Creates all output tables in given output_path."""
        if not output_path.exists():
            logger.warning(f"Output path created: '{output_path.resolve()}'")
            output_path.mkdir()

        self.create_table(
            table_path=output_path / "Studies.tsv",
            google_sheets=google_sheets,
            report_type=TableReportTypes.STUDIES
        )
        self.create_table(
            table_path=output_path / "Timecourses.tsv",
            google_sheets=google_sheets,
            report_type=TableReportTypes.TIMECOURSES
        )
        self.create_table(
            table_path=output_path / "Pharmacokinetics.tsv",
            google_sheets=google_sheets,
            report_type=TableReportTypes.PHARMACOKINETICS
        )

    def create_table(self, table_path: Path,
                     report_type: TableReportTypes=TableReportTypes.STUDIES,
                     google_sheets: str=None):
        """Creates a summary table from PKData.

        :param: substances: iterable of PKDB substance ids for filtering of data
        """
        if not isinstance(report_type, TableReportTypes):
            raise ValueError(
                f"'report_type' must be TableReportTypes, but "
                f"is: {type(report_type), report_type}"
            )

        print(f"Create TableReport: {report_type}")

        if report_type == TableReportTypes.STUDIES:
            table_df = self.studies_table()
        elif report_type == TableReportTypes.TIMECOURSES:
            table_df = self.timecourses_table()
        elif report_type == TableReportTypes.PHARMACOKINETICS:
            table_df = self.pks_table()

        if google_sheets is not None:
            if report_type in {TableReportTypes.STUDIES, TableReportTypes.TIMECOURSES}:
                header_start = 'A4'
                header_size = 4
            elif report_type == TableReportTypes.PHARMACOKINETICS:
                header_start = 'A5'
                header_size = 5

            sheet_name = report_type.name.lower().capitalize()
            print(f"Writing: {google_sheets}.{sheet_name}")
            spread = Spread(google_sheets)
            sheet = spread.find_sheet(sheet_name)
            sheet.resize(header_size, len(table_df.columns))

            spread.df_to_sheet(
                table_df, index=False, headers=False,
                sheet=sheet_name, start=header_start, replace=False
            )

        if str(table_path).endswith(".xlsx"):
            table_df.to_excel(table_path)
        elif str(table_path).endswith(".tsv"):
            table_df.to_csv(table_path, sep='\t')
        else:
            raise AssertionError("wrong format ending (tsv and xlsx are supported")

    def studies_table(self) -> pd.DataFrame:
        """
        Changes studies in place.
        Changes study_keys in place.
        """
        table_keys = []
        table_df = self.pkdata.studies.df.copy()

        subject_info = {
            "sex": Parameter(measurement_types=["sex"], value_field=["choice"]),
            "age": Parameter(measurement_types=["age"],
                             value_field=["mean", "median", "value"]),
            "weight": Parameter(measurement_types=["weight"],
                                value_field=["mean", "median", "value"]),
            "height": Parameter(measurement_types=["height"],
                                value_field=["mean", "median", "value"]),
            "body mass index": Parameter(measurement_types=["bmi"],
                                         value_field=["mean", "median", "value"]),
            "ethnicity": Parameter(measurement_types=["ethnicity"],
                                   value_field=["choice"]),

            # pk effecting factors
            "healthy": Parameter(measurement_types=["healthy"],
                                 value_field=["choice"]),
            "medication": Parameter(measurement_types=["medication"],
                                    value_field=["choice"]),
            "smoking": Parameter(measurement_types=["smoking"],
                                 value_field=["choice"]),
            "oral contraceptives": Parameter(
                measurement_types=["oral contraceptives"], value_field=["choice"]),
            "overnight fast": Parameter(measurement_types=["overnight fast"],
                                        value_field=["choice"]),
            "CYP1A2 genotype": Parameter(measurement_types=["CYP1A2 genotype"],
                                         value_field=["choice"]),
            "abstinence alcohol": Parameter(
                measurement_types=["abstinence alcohol"],
                value_field=["mean", "median", "value", "min", "max"])
        }

        intervention_info = {
            "dosing amount": Parameter(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["value"]),
            "dosing route": Parameter(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["route"]),
            "dosing form": Parameter(
                measurement_types=["dosing", "qualitative dosing"],
                value_field=["form"]),
        }
        outputs_info = {
            "quantification method": Parameter(measurement_types="any",
                                               value_field=["method"]),
        }

        s_keys = list(subject_info.keys())
        i_keys = list(intervention_info.keys())
        o_keys = list(outputs_info.keys())

        table_keys.extend(["Subjects_individual",
                           "Subjects_groups"])

        for keys in [s_keys, i_keys, o_keys]:
            table_keys.extend(copy(keys))
            keys.append("sid")

        studies_interventions = table_df.apply(
            self._add_information,
            args=(self.pkdata, intervention_info, "interventions"),
            axis=1
        )
        studies_group = table_df.apply(
            self._add_information,
            args=(self.pkdata, subject_info, "groups"),
            axis=1
        )
        studies_group[["Subjects_individual", "Subjects_groups"]] = studies_group[
            ["Subjects_individual", "Subjects_groups"]].astype(int)

        studies_individuals = table_df.apply(
            self._add_information,
            args=(self.pkdata, subject_info, "individuals"),
            axis=1
        )
        table_df = pd.merge(table_df, self._combine(
            studies_group[[*s_keys, "Subjects_individual", "Subjects_groups"]],
            studies_individuals[s_keys]), on="sid")
        table_df = pd.merge(table_df, studies_interventions[i_keys], on="sid")
        studies_outputs = table_df.apply(
            self._add_information,
            args=(self.pkdata, outputs_info, "outputs"),
            axis=1
        )
        studies_timecourses = table_df.apply(
            self._add_information,
            args=(self.pkdata, outputs_info, "timecourses"),
            axis=1
        )
        table_df = pd.merge(
            table_df, self._combine(studies_outputs[o_keys], studies_timecourses[o_keys])
        )
        # reformating things
        table_keys, table_df = self._format_table_information(table_df=table_df,
                                                              table_keys=table_keys)
        table_final_df = table_df[table_keys]
        return table_final_df

    def timecourses_table(self) -> pd.DataFrame:
        table_keys = []
        table_df = self.pkdata.studies.df.copy()

        timecourse_fields = {
            "individual": {"value_field": ["value"], "only_individual": True},
            "group": {"value_field": ["mean", "median"], "only_group": True},
            "error": {"value_field": ["sd", "se", "cv"], "only_group": True},
            "plasma/blood": {"value_field": ["tissue"],
                             "values": ["plasma", "blood", "serum"],
                             "groupby": False},
            "urine": {"value_field": ["tissue"], "values": ["urine"],
                      "groupby": False},
            "saliva": {"value_field": ["tissue"], "values": ["saliva"],
                       "groupby": False},
        }
        timecourse_info = {}
        for substance in self.substances:
            for key, p_kwargs in timecourse_fields.items():
                this_key = f"{substance}_timecourses_{key}"
                timecourse_info[this_key] = Parameter(measurement_types="any",
                                                      substance=substance,
                                                      **p_kwargs)
                table_keys.append(this_key)

        table_df = table_df.apply(
            self._add_information,
            args=(self.pkdata, timecourse_info, "timecourses"),
            axis=1
        )
        table_df = table_df.fillna(" ")

        # reformating things
        table_keys, table_df = self._format_table_information(table_df=table_df,
                                                              table_keys=table_keys)
        return table_df[table_keys]

    def pks_table(self) -> pd.DataFrame:
        table_keys = []
        table_df = self.pkdata.studies.df.copy()
        pks_info = {}
        for substance in self.substances:
            pks_info_substance = {
                f"{substance}_plasma/blood": Parameter(substance=f"{substance}",
                                                    value_field=["tissue"],
                                                    values=["plasma", "blood",
                                                            "serum"],
                                                    groupby=False),
                f"{substance}_urine": Parameter(substance=f"{substance}",
                                                value_field=["tissue"],
                                                values=["urine"],
                                                groupby=False),
                f"{substance}_saliva": Parameter(substance=f"{substance}",
                                                 value_field=["tissue"],
                                                 values=["saliva"],
                                                 groupby=False),
                f"{substance}_vd_individual": Parameter(
                    measurement_types=["vd"], substance=f"{substance}",
                    value_field=["value"], only_individual=True),
                f"{substance}_vd_group": Parameter(measurement_types=["vd"],
                                                   substance=f"{substance}",
                                                   value_field=["mean",
                                                                "median"],
                                                   only_group=True),
                f"{substance}_vd_error": Parameter(measurement_types=["vd"],
                                                   substance=f"{substance}",
                                                   value_field=["sd", "se",
                                                                "cv"],
                                                   only_group=True),
                f"{substance}_clearance_individual": Parameter(
                    measurement_types=["clearance"], substance=f"{substance}",
                    value_field=["value"], only_individual=True),
                f"{substance}_clearance_group": Parameter(
                    measurement_types=["clearance"], substance=f"{substance}",
                    value_field=["mean", "median"], only_group=True),
                f"{substance}_clearance_error": Parameter(
                    measurement_types=["clearance"], substance=f"{substance}",
                    value_field=["sd", "se", "cv"], only_group=True),
                f"{substance}_auc_individual": Parameter(
                    measurement_types=["auc_end", "auc_inf"],
                    substance=f"{substance}", value_field=["value"],
                    only_individual=True),
                f"{substance}_auc_group": Parameter(
                    measurement_types=["auc_end", "auc_inf"],
                    substance=f"{substance}", value_field=["mean", "median"],
                    only_group=True),
                f"{substance}_auc_error": Parameter(
                    measurement_types=["auc_end", "auc_inf"],
                    substance=f"{substance}", value_field=["sd", "se", "cv"],
                    only_group=True),
                f"{substance}_thalf_individual": Parameter(
                    measurement_types=["thalf"], substance=f"{substance}",
                    value_field=["value"], only_individual=True),
                f"{substance}_thalf_group": Parameter(
                    measurement_types=["thalf"], substance=f"{substance}",
                    value_field=["mean", "median"], only_group=True),
                f"{substance}_thalf_error": Parameter(
                    measurement_types=["thalf"], substance=f"{substance}",
                    value_field=["sd", "se", "cv"], only_group=True),
                f"{substance}_cmax_individual": Parameter(
                    measurement_types=["cmax"], substance=f"{substance}",
                    value_field=["value"], only_individual=True),
                f"{substance}_cmax_group": Parameter(measurement_types=["cmax"],
                                                     substance=f"{substance}",
                                                     value_field=["mean",
                                                                  "median"],
                                                     only_group=True),
                f"{substance}_cmax_error": Parameter(measurement_types=["cmax"],
                                                     substance=f"{substance}",
                                                     value_field=["sd", "se",
                                                                  "cv"],
                                                     only_group=True),
                f"{substance}_tmax_individual": Parameter(
                    measurement_types=["tmax"], substance=f"{substance}",
                    value_field=["value"], only_individual=True),
                f"{substance}_tmax_group": Parameter(measurement_types=["tmax"],
                                                     substance=f"{substance}",
                                                     value_field=["mean",
                                                                  "median"],
                                                     only_group=True),
                f"{substance}_tmax_error": Parameter(measurement_types=["tmax"],
                                                     substance=f"{substance}",
                                                     value_field=["sd", "se",
                                                                  "cv"],
                                                     only_group=True),
                f"{substance}_kel_individual": Parameter(
                    measurement_types=["kel"], substance=f"{substance}",
                    value_field=["value"], only_individual=True),
                f"{substance}_kel_group": Parameter(measurement_types=["kel"],
                                                    substance=f"{substance}",
                                                    value_field=["mean",
                                                                 "median"],
                                                    only_group=True),
                f"{substance}_kel_error": Parameter(measurement_types=["kel"],
                                                    substance=f"{substance}",
                                                    value_field=["sd", "se",
                                                                 "cv"],
                                                    only_group=True)
            }
            pks_info = {**pks_info, **pks_info_substance}

        table_df = table_df.apply(
            self._add_information,
            args=(self.pkdata, pks_info, "outputs"),
            axis=1
        )
        table_keys.extend(pks_info.keys())
        table_df = table_df.fillna(" ")
        # reformating things
        table_keys, table_df = self._format_table_information(table_df=table_df,
                                                              table_keys=table_keys)
        return table_df[table_keys]


    @staticmethod
    def _add_information(study, pkdata, measurement_types: Dict, table: str):
        """ ??? """

        additional_dict = {}

        used_pkdata = pkdata.filter_study(lambda x: x["sid"] == study.sid)
        this_table = getattr(used_pkdata, table)
        has_info_kwargs = {"df": this_table.df, "instance_id": this_table.pk}
        group_df_df = pkdata.groups.df
        study_group_df = group_df_df[group_df_df["study_sid"] == study.sid]
        all_group = study_group_df[study_group_df["group_name"] == "all"]
        subject_size = all_group.group_count.unique()[0]
        has_info_kwargs["Subjects_individual"] = subject_size
        has_info_kwargs["Subjects_groups"] = len(used_pkdata.groups.pks)

        if table == "groups":
            additional_dict["Subjects_individual"] = has_info_kwargs[
                "Subjects_individual"]
            additional_dict["Subjects_groups"] = has_info_kwargs[
                "Subjects_groups"]

        additional_dict = {
            **{key: TableReport._has_info(parameter=parameter, **has_info_kwargs) for
               key, parameter in
               measurement_types.items()}, **additional_dict}

        return study.append(pd.Series(additional_dict))

    @staticmethod
    def _format_table_information(table_keys, table_df):
        """Formats table information in place."""
        table_df = table_df.rename(columns={"reference_date": "publication date"})
        table_df["PKDB identifier"] = table_df["sid"].apply(
            lambda x: f'=HYPERLINK("https://develop.pk-db.com/{x}/";"{x}")')
        table_df["PMID"] = table_df["sid"].apply(lambda
                                                   x: f'=HYPERLINK("https://www.ncbi.nlm.nih.gov/pubmed/{x}";"{x}")')
        table_keys = ["PKDB identifier", "name", "PMID",
                      "publication date", ] + table_keys
        table_df.sort_values(by="publication date", inplace=True)
        return table_keys, table_df

    @staticmethod
    def _add_group_all_count(study_df: pd.DataFrame, pkdata: PKData):
        """ Adds a column with the group count of the all group for every study.
        Changes study in place.
        """
        # get all "all" groups (FIXME: unnecessary repetition)
        all_groups = pkdata.groups_core[pkdata.groups_core["group_name"] == "all"]

        group = all_groups[(all_groups["study_name"] == study_df.name)]

        # check
        assert len(group) == 1, (len(group), study_df.name, group)
        study_df["Group_all_count"] = group["group_count"]

    @staticmethod
    def _has_info(df: pd.DataFrame, instance_id: str, parameter: Parameter, Subjects_groups: int=0 , Subjects_individual: int=0):
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
        if len(df) == 0:
            return None

        for _, instance in df.groupby(instance_id):
            if parameter.measurement_types == "any":
                specific_info = instance
            else:
                specific_info = instance[instance["measurement_type"].isin(parameter.measurement_types)]

            value_types = specific_info[parameter.value_field].applymap(type).stack().unique()

            has_array = False
            for value in value_types:
                if value is np.ndarray:

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
            return " "

        elif all(has_info):
            if compare_length > 0:
                if len(has_info) == compare_length:
                    return "✓"
            else:
                return "✓"
        return "⅟"

    @staticmethod
    def _strict_and_logic(series):
        elements = set(series.dropna().values)
        if len(elements) == 1:
            return list(elements)[0]
        else:
            return " "

    @staticmethod
    def _and_logic(series):
        elements = set(series.dropna().values)
        if len(elements) == 1:
            return list(elements)[0]
        else:
            return "⅟"

    @staticmethod
    def _any_logic(series):
        elements = set([values for values in series.values if values is not None])
        if "✓" in elements:
            return "✓"
        else:
            return " "

    @staticmethod
    def _combine(df1, df2):
        merged = pd.merge(df1, df2, on="sid")

        for column in [c for c in df2.columns if c != "sid"]:
            keys = [f'{column}_x', f'{column}_y']
            merged[column] = merged[keys].apply(TableReport._and_logic, axis=1)

        return merged[df1.columns]

    @staticmethod
    def _extend_study_keys(study_keys):
        return study_keys.extend(["PKDB identifier",
                                 "Name",
                                 "PMID",
                                 "publication date",
                                 "Subjects_individual",
                                 "Subjects_groups"])

    @staticmethod
    def _clear_sheat(spread, header_size, column_length):
        spread.update_cells(
            start=(1, header_size),
            end=(1, 1),
            vals=["" for i in range(0, column_length * 1)],
        )


if __name__ == "__main__":
    pass