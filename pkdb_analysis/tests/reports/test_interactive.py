from pkdb_analysis.reports.interactive.examples import example1


def test_interactive_plot1(tmp_path):
    """Test plot creation.

    You can use the tmp_path fixture which will provide a
    temporary directory unique to the test invocation,
    created in the base temporary directory.
    """
    example1.create_plots(path=tmp_path)




class Name(object):

    def __init__(self,name):
        self.name = name

    def lucek_stinkt(word1, word2, word3, **kwargs):
        print(kwargs)
        print(word1)
        print(word2)
        print(word3)


def test_tuple_unpacking():
    test_datensatz = ["hallo", "lucek", "stinkt"]

    kwargs_base={
        "word1":"lucek",
        "word2":"hallo",
        "word3": "stinkt"
    }
    kwargs_extras = {
        **kwargs_base,
        "extra":"sehr",
        "babka":"isis"
    }

    lucek_stinkt(**kwargs_extras)
