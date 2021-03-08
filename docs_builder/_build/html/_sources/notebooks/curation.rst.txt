.. code:: ipython3

    from IPython.display import display
    from pkdb_analysis import PKFilter, PKFilterFactory, PKData, PKDB
    import pandas as pd


::


    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-1-9779cd9ede1f> in <module>
          2 get_ipython().run_line_magic('autoreload', '2')
          3 from IPython.display import display
    ----> 4 from pkdb_analysis import PKFilter, PKFilterFactory, PKData, PKDB
          5 import pandas as pd


    ImportError: cannot import name 'PKFilterFactory' from 'pkdb_analysis' (/home/janek/Dev/pkdb_analysis/src/pkdb_analysis/__init__.py)


Curation and checking of studies
================================

Helpers for simple checking of curated results.

.. code:: ipython3

    # get data for study
    study_name = "Test1"
    pkfilter = PKFilterFactory.by_study_name(study_name)
    data = PKDB.query(pkfilter=pkfilter)
    print(data)


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-ea6e6bd278a7> in <module>
          1 # get data for study
          2 study_name = "Test1"
    ----> 3 pkfilter = PKFilterFactory.by_study_name(study_name)
          4 data = PKDB.query(pkfilter=pkfilter)
          5 print(data)


    NameError: name 'PKFilterFactory' is not defined


Explore data content
--------------------

.. code:: ipython3

    print(data.groups.pks)
    print(data.individuals.pks)



::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-21704facd3df> in <module>
    ----> 1 print(data.groups.pks)
          2 print(data.individuals.pks)


    NameError: name 'data' is not defined


.. code:: ipython3

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(data.groups_mi)
        display(data.individuals_mi)
        display(data.interventions_mi)
        display(data.outputs_mi)
        display(data.timecourses_mi)


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-b5f98a7f64fd> in <module>
    ----> 1 with pd.option_context('display.max_rows', None, 'display.max_columns', None):
          2     display(data.groups_mi)
          3     display(data.individuals_mi)
          4     display(data.interventions_mi)
          5     display(data.outputs_mi)


    NameError: name 'pd' is not defined


.. code:: ipython3

    data.timecourses


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-2fde804e136a> in <module>
    ----> 1 data.timecourses
    

    NameError: name 'data' is not defined


.. code:: ipython3

    data.timecourses
    



::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-0d2b1d8dbe58> in <module>
    ----> 1 data.timecourses
          2 


    NameError: name 'data' is not defined



