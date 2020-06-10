from pkdb_analysis.reports import create_interactive_plots


def test_interactive_plot1(tmp_path):
    """Test plot creation.

    You can use the tmp_path fixture which will provide a
    temporary directory unique to the test invocation,
    created in the base temporary directory.
    """
    create_interactive_plots(path=tmp_path)
