.. code:: ipython3

    from IPython.display import display
    from pkdb_analysis import PKFilter, PKFilterFactory, PKData, PKDB
    import pandas as pd

Curation and checking of studies
================================

Helpers for simple checking of curated results.

.. code:: ipython3

    # get data for study
    study_name = "Test1"
    pkfilter = PKFilterFactory.by_study_name(study_name)
    data = PKDB.query(pkfilter=pkfilter)
    print(data)


.. parsed-literal::

    INFO *** Querying data ***
    INFO http://0.0.0.0:8000/api/v1/pkdata/studies/?format=json&page_size=2000&study_name=Test1
    INFO http://0.0.0.0:8000/api/v1/pkdata/studies/?format=json&page_size=2000&study_name=Test1&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/interventions/?format=json&page_size=2000&normed=true&study_name=Test1
    INFO http://0.0.0.0:8000/api/v1/pkdata/interventions/?format=json&page_size=2000&normed=true&study_name=Test1&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&study_name=Test1
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&study_name=Test1&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&study_name=Test1
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&study_name=Test1&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&study_name=Test1
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&study_name=Test1&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/timecourses/?format=json&page_size=2000&study_name=Test1
    INFO http://0.0.0.0:8000/api/v1/pkdata/timecourses/?format=json&page_size=2000&study_name=Test1&page=1


.. parsed-literal::

    ------------------------------
    PKData (140210902454608)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    ------------------------------


Explore data content
--------------------

.. code:: ipython3

    print(data.groups.pks)
    print(data.individuals.pks)



.. parsed-literal::

    set()
    set()


.. code:: ipython3

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(data.groups_mi)
        display(data.individuals_mi)
        display(data.interventions_mi)
        display(data.outputs_mi)
        display(data.timecourses_mi)



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>


.. code:: ipython3

    data.timecourses



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>




.. parsed-literal::

    Empty DataFrame
    Columns: []
    Index: []



.. code:: ipython3

    data.timecourses
    




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>




.. parsed-literal::

    Empty DataFrame
    Columns: []
    Index: []




