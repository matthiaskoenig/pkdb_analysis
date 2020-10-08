import pytest
from pkdb_analysis import PKData, filter
from pkdb_analysis.reports import create_table_report
from pkdb_analysis.reports.tables import TableReport, Parameter
from pkdb_analysis.test import TEST_ZIP


# FIXME
# @pytest.mark.skip("FIXME")
def test_tables(tmp_path):
    output_path = tmp_path / "tables"
    xlsx_path = output_path / "tables.xlsx"
    create_table_report(
        zip_data_path=TEST_ZIP,
        dosing_substances=["torasemide"],
        report_substances=[
            "torasemide",
            "torasemide-M1",
            "torasemide-M3",
            "torasemide-M5",
        ],
        excel_path=xlsx_path,
        # google_sheets="TorasemideTables",
        tsv_path=output_path,
        query_data=False,
    )

    assert xlsx_path.exists()
    assert (output_path / "studies.tsv").exists()
    assert (output_path / "pharmacokinetics.tsv").exists()
    assert (output_path / "timecourses.tsv").exists()


def test_create_studies(tmp_path):
    report_substances = [
                            "torasemide",
                            "torasemide-M1",
                            "torasemide-M3",
                            "torasemide-M5",
                        ],

    if not TEST_ZIP.exists():
        raise IOError(
            f"Zip file does not exist: '{TEST_ZIP}'. "
            f"Query the data first with the `query_data=True' flag."
        )
    pkdata = PKData.from_archive(TEST_ZIP)

    study_sids = pkdata.filter_intervention(
        f_idx=filter.f_dosing_in, concise=False ,substances=["torasemide"],
    ).interventions.study_sids

    pkdata = pkdata.filter_study(lambda x: x["sid"].isin(study_sids), concise=False)

    # Create table report
    table_report = TableReport(pkdata=pkdata, substances=report_substances)



    intervention_info = {
        "dosing amount": Parameter(
            measurement_types=["dosing", "qualitative dosing"],
            value_field=["value"],
        ),
        "dosing route": Parameter(
            measurement_types=["dosing", "qualitative dosing"],
            value_field=["route"],
        ),
        "dosing form": Parameter(
            measurement_types=["dosing", "qualitative dosing"], value_field=["form"]
        ),
    }
    studies_interventions = table_report.pkdata.studies.apply(
        table_report._add_information,
        args=(table_report.pkdata, table_report.pkdata_concised, intervention_info, "interventions"),
        axis=1,
    )
