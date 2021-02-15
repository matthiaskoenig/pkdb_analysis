from dataclasses import field, dataclass

from pkdb_analysis import PKDB, PKData
from pkdb_analysis.circos import create_config_files

from pkdb_analysis.reports import create_table_report
from pkdb_analysis.reports.tables import TableReport
from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP
from pkdb_analysis.core import Sid as BaseSid, Core


@dataclass(frozen=True)
class Sid(BaseSid):
    core: Core = field(default=Core(sids=PKDB.query_info_nodes_sids()))


def test_tables(tmp_path):
    output_path = tmp_path / "tables"
    xlsx_path = output_path / "tables.xlsx"
    create_table_report(
        zip_data_path=TESTDATA_CONCISE_FALSE_ZIP,
        dosing_substances=[Sid("torasemide").sid],
        report_substances=[
            Sid("torasemide").sid,
            Sid("torasemide-m1").sid,
            Sid("torasemide-m3").sid,
            Sid("torasemide-m5").sid,
        ],
        excel_path=xlsx_path,
        # google_sheets="TorasemideTables",
        tsv_dir=output_path,
        query_data=False,
    )

    assert xlsx_path.exists()
    assert (output_path / "studies.tsv").exists()
    assert (output_path / "pharmacokinetics.tsv").exists()
    assert (output_path / "timecourses.tsv").exists()

    # data = pd.read_csv(output_path / "timecourses.tsv", sep="\t")


def test_circos_table():
    pkdata = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)
    df_circos = TableReport(pkdata).circos_table()
    assert len(df_circos) > 1


def test_create_config_files_circos(tmp_path):
    pkdata = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)
    df_circos = TableReport(pkdata).circos_table()
    df_circos["type"] = 0
    df_circos["label"] = "caffeine"
    create_config_files(df_circos, tmp_path)
    assert (tmp_path / "timecourse_number.txt").exists()
    assert (tmp_path / "all_subjects_number.txt").exists()
    assert (tmp_path / "output_number.txt").exists()
    assert (tmp_path / "intervention_number.txt").exists()
    assert (tmp_path / "ideogram.txt").exists()


