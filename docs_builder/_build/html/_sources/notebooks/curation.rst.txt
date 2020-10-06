.. code:: ipython3

    from IPython.display import display
    from pkdb_analysis import PKFilter, PKFilterFactory, PKData
    import pandas as pd

Curation and checking of studies
================================

Helpers for simple checking of curated results.

.. code:: ipython3

    # get data for study
    study_name = "Test1"
    pkfilter = PKFilterFactory.by_study_name(study_name)
    data = PKData.from_db(pkfilter=pkfilter)
    print(data)


::


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-2-fdfa447e5e34> in <module>
          2 study_name = "Test1"
          3 pkfilter = PKFilterFactory.by_study_name(study_name)
    ----> 4 data = PKData.from_db(pkfilter=pkfilter)
          5 print(data)


    AttributeError: type object 'PKData' has no attribute 'from_db'


Explore data content
--------------------

.. code:: ipython3

    print(data.groups_pks)
    print(data.individuals_pks)


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-3-cca53507754f> in <module>
    ----> 1 print(data.groups_pks)
          2 print(data.individuals_pks)


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

    <ipython-input-4-968c7907bc28> in <module>
          1 with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    ----> 2     display(data.groups_mi)
          3 
          4 display(data.individuals_mi)
          5 display(data.interventions_mi)


    NameError: name 'data' is not defined

