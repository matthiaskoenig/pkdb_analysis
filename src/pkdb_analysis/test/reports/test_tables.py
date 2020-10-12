from pkdb_analysis.reports import create_table_report
from pkdb_analysis.test import TEST_ZIP


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

