.. code:: ipython3

    
    import pandas as pd
    from IPython.display import display
    
    from pkdb_analysis import PKData, PKFilter
    from pkdb_analysis.tests.constants import TEST_HDF5

Working with PK-DB data
=======================

To easily work with PK-DB data we provide the ``pkdb_analysis`` python
library. These includes helper functions for querying data and filter
existing data sets. In the following we provide an overview over the
typical functionality when working with PK-DB data.

The main class to work with is ``PKData``. It is possible to directly
query the database or to load data from file.

Load data from file
-------------------

PKData can be serialized to HDF5 files. In the following we will load
the test data set and print an overview.

.. code:: ipython3

    from pkdb_analysis import PKData, PKFilter
    from pkdb_analysis.tests.constants import TEST_HDF5
    
    data = PKData.from_hdf5(TEST_HDF5)
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (140562873164688)
    ------------------------------
    studies             4 
    groups              8  (   86)
    individuals       246  ( 3144)
    interventions      18  (   18)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
    ------------------------------


Load data from database
-----------------------

Alternatively data can be loaded from the database using the
``PKDB.query()`` function. This is documented in the ``Querying PK-DB``
section.

Accessing groups, individuals, interventions, outputs and timecourses
---------------------------------------------------------------------

All PKData consists of consistent information on: - ``studies``: PK-DB
studies, uniquely identified via a ``study_sid`` - ``groups``: groups,
uniquely identified via ``group_pk`` - ``individuals``: individuals,
uniquely identified via ``individual_pk`` - ``interventions``:
interventions, uniquely identified via ``intervention_pk`` -
``outputs``: outputs, uniquely identified via ``output_pk`` -
``timecourses``: groups, uniquely identified via ``timecourse_pk``

The ``print`` function provides a simple overview over the content

.. code:: ipython3

    print(data)


.. parsed-literal::

    ------------------------------
    PKData (140562873164688)
    ------------------------------
    studies             4 
    groups              8  (   86)
    individuals       246  ( 3144)
    interventions      18  (   18)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
    ------------------------------


We can access the information via the respective fields, e.g., groups
via ``data.groups`` or the multi-index data via ``data.groups_mi``.

.. code:: ipython3

    data.groups




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
          <th>study_sid</th>
          <th>study_name</th>
          <th>group_pk</th>
          <th>group_name</th>
          <th>group_count</th>
          <th>group_parent_pk</th>
          <th>characteristica_pk</th>
          <th>count</th>
          <th>measurement_type</th>
          <th>choice</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>26</td>
          <td>all</td>
          <td>2</td>
          <td>-1</td>
          <td>1068</td>
          <td>2</td>
          <td>abstinence</td>
          <td>None</td>
          <td>cocoa</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>1</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>26</td>
          <td>all</td>
          <td>2</td>
          <td>-1</td>
          <td>1067</td>
          <td>2</td>
          <td>abstinence</td>
          <td>None</td>
          <td>tea</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>2</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>26</td>
          <td>all</td>
          <td>2</td>
          <td>-1</td>
          <td>1066</td>
          <td>2</td>
          <td>abstinence</td>
          <td>None</td>
          <td>coffee</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>3</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>26</td>
          <td>all</td>
          <td>2</td>
          <td>-1</td>
          <td>1065</td>
          <td>2</td>
          <td>species</td>
          <td>homo sapiens</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>4</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>20</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>481</td>
          <td>6</td>
          <td>species</td>
          <td>homo sapiens</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>81</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>25</td>
          <td>80-90</td>
          <td>10</td>
          <td>21</td>
          <td>523</td>
          <td>40</td>
          <td>medication</td>
          <td>N</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>82</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>25</td>
          <td>80-90</td>
          <td>10</td>
          <td>21</td>
          <td>584</td>
          <td>10</td>
          <td>gfr</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>36.99422</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>10.982659</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>milliliter / meter ** 2 / minute</td>
        </tr>
        <tr>
          <th>83</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>25</td>
          <td>80-90</td>
          <td>10</td>
          <td>21</td>
          <td>526</td>
          <td>40</td>
          <td>ethnicity</td>
          <td>caucasian</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>84</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>25</td>
          <td>80-90</td>
          <td>10</td>
          <td>21</td>
          <td>527</td>
          <td>38</td>
          <td>smoking</td>
          <td>N</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>85</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>25</td>
          <td>80-90</td>
          <td>10</td>
          <td>21</td>
          <td>528</td>
          <td>2</td>
          <td>smoking</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
      </tbody>
    </table>
    <p>86 rows × 20 columns</p>
    </div>



.. code:: ipython3

    data.groups_mi




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
          <th></th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>group_name</th>
          <th>group_count</th>
          <th>group_parent_pk</th>
          <th>count</th>
          <th>measurement_type</th>
          <th>choice</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
        <tr>
          <th>group_pk</th>
          <th>characteristica_pk</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">20</th>
          <th>481</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>6</td>
          <td>species</td>
          <td>homo sapiens</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>482</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>6</td>
          <td>healthy</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>483</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>1</td>
          <td>smoking</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>484</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>5</td>
          <td>smoking</td>
          <td>N</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>485</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>6</td>
          <td>age</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>25.0</td>
          <td>37.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>yr</td>
        </tr>
        <tr>
          <th>...</th>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th rowspan="5" valign="top">27</th>
          <th>1086</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
          <td>alcohol</td>
          <td>N</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>1087</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
          <td>weight</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>76.7</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>6.8</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>kilogram</td>
        </tr>
        <tr>
          <th>1088</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
          <td>age</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>27.1</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3.1</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>yr</td>
        </tr>
        <tr>
          <th>1089</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
          <td>ethnicity</td>
          <td>NR</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>1090</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
          <td>overnight fast</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
      </tbody>
    </table>
    <p>86 rows × 18 columns</p>
    </div>



To access the number of items use the ``*_count``.

.. code:: ipython3

    print(f"Number of groups: {data.groups_count}")


.. parsed-literal::

    Number of groups: 8


The ``groups``, ``individuals``, ``interventions``, ``outputs`` and
``timecourses`` are ``pandas.DataFrame`` instances, so all the classical
pandas operations can be applied on the data. For instance to access a
single ``group`` use logical indexing by the ``group_pk`` field. E.g. to
get the group ``20`` use

.. code:: ipython3

    data.groups[data.groups.group_pk==20]




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
          <th>study_sid</th>
          <th>study_name</th>
          <th>group_pk</th>
          <th>group_name</th>
          <th>group_count</th>
          <th>group_parent_pk</th>
          <th>characteristica_pk</th>
          <th>count</th>
          <th>measurement_type</th>
          <th>choice</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>4</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>20</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>481</td>
          <td>6</td>
          <td>species</td>
          <td>homo sapiens</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>5</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>20</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>482</td>
          <td>6</td>
          <td>healthy</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>6</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>20</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>483</td>
          <td>1</td>
          <td>smoking</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>7</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>20</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>484</td>
          <td>5</td>
          <td>smoking</td>
          <td>N</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>8</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>20</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>485</td>
          <td>6</td>
          <td>age</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>25.0</td>
          <td>37.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>yr</td>
        </tr>
        <tr>
          <th>9</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>20</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>486</td>
          <td>6</td>
          <td>overnight fast</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
      </tbody>
    </table>
    </div>



In the group tables multiple rows exist which belong to a single group!
This is important to understand filtering of the data later on. For
instance in this example the information on ``species``, ``healthy``,
``smoking``, ``age`` and ``overnight_fast`` are all separate rows in the
``groups`` table, but belong to a single row.

When looking at the multi-index table this becomes more clear. We now
get the group 20 form the ``groups_mi``. We can simply use the ``.loc``
to lookup the group by ``pk``

.. code:: ipython3

    data.groups_mi.loc[20]




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
          <th>study_sid</th>
          <th>study_name</th>
          <th>group_name</th>
          <th>group_count</th>
          <th>group_parent_pk</th>
          <th>count</th>
          <th>measurement_type</th>
          <th>choice</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
        <tr>
          <th>characteristica_pk</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>481</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>6</td>
          <td>species</td>
          <td>homo sapiens</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>482</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>6</td>
          <td>healthy</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>483</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>1</td>
          <td>smoking</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>484</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>5</td>
          <td>smoking</td>
          <td>N</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>485</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>6</td>
          <td>age</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>25.0</td>
          <td>37.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>yr</td>
        </tr>
        <tr>
          <th>486</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>all</td>
          <td>6</td>
          <td>-1</td>
          <td>6</td>
          <td>overnight fast</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
      </tbody>
    </table>
    </div>



In a similar manner we can explore the other information, i.e.
``individuals``, ``interventions``, ``outputs`` and ``timecourses``.

.. code:: ipython3

    data.individuals_mi




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
          <th></th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>individual_name</th>
          <th>individual_group_pk</th>
          <th>count</th>
          <th>measurement_type</th>
          <th>choice</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
        <tr>
          <th>individual_pk</th>
          <th>characteristica_pk</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">39</th>
          <th>481</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>WS</td>
          <td>20</td>
          <td>6</td>
          <td>species</td>
          <td>homo sapiens</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>482</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>WS</td>
          <td>20</td>
          <td>6</td>
          <td>healthy</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>483</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>WS</td>
          <td>20</td>
          <td>1</td>
          <td>smoking</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>484</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>WS</td>
          <td>20</td>
          <td>5</td>
          <td>smoking</td>
          <td>N</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>486</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>WS</td>
          <td>20</td>
          <td>6</td>
          <td>overnight fast</td>
          <td>Y</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>...</th>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>283</th>
          <th>1068</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>H.C.</td>
          <td>26</td>
          <td>2</td>
          <td>abstinence</td>
          <td>None</td>
          <td>cocoa</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th rowspan="4" valign="top">284</th>
          <th>1065</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>F.M.</td>
          <td>26</td>
          <td>2</td>
          <td>species</td>
          <td>homo sapiens</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>1066</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>F.M.</td>
          <td>26</td>
          <td>2</td>
          <td>abstinence</td>
          <td>None</td>
          <td>coffee</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>1067</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>F.M.</td>
          <td>26</td>
          <td>2</td>
          <td>abstinence</td>
          <td>None</td>
          <td>tea</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
        <tr>
          <th>1068</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>F.M.</td>
          <td>26</td>
          <td>2</td>
          <td>abstinence</td>
          <td>None</td>
          <td>cocoa</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
        </tr>
      </tbody>
    </table>
    <p>3144 rows × 17 columns</p>
    </div>



.. code:: ipython3

    data.interventions_mi




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
          <th>study_sid</th>
          <th>study_name</th>
          <th>raw_pk</th>
          <th>normed</th>
          <th>name</th>
          <th>route</th>
          <th>form</th>
          <th>application</th>
          <th>time</th>
          <th>time_unit</th>
          <th>...</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
        <tr>
          <th>intervention_pk</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>91</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>-1</td>
          <td>False</td>
          <td>po75</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>midazolam</td>
          <td>7.500000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>mg</td>
        </tr>
        <tr>
          <th>92</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>-1</td>
          <td>False</td>
          <td>po15</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>midazolam</td>
          <td>15.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>mg</td>
        </tr>
        <tr>
          <th>93</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>91</td>
          <td>True</td>
          <td>po75</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>midazolam</td>
          <td>0.007500</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>94</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>92</td>
          <td>True</td>
          <td>po15</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>midazolam</td>
          <td>0.015000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>95</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>-1</td>
          <td>False</td>
          <td>iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>midazolam</td>
          <td>0.075000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>mg/kg</td>
        </tr>
        <tr>
          <th>96</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>95</td>
          <td>True</td>
          <td>iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>midazolam</td>
          <td>0.000075</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / kilogram</td>
        </tr>
        <tr>
          <th>97</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>-1</td>
          <td>False</td>
          <td>paracetamol1000mg_iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>constant infusion</td>
          <td>0.0</td>
          <td>min</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>1000.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>mg</td>
        </tr>
        <tr>
          <th>98</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>97</td>
          <td>True</td>
          <td>paracetamol1000mg_iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>constant infusion</td>
          <td>0.0</td>
          <td>min</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>1.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>99</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>-1</td>
          <td>False</td>
          <td>theobromine</td>
          <td>oral</td>
          <td>None</td>
          <td>None</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>theobromine</td>
          <td>1.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>g</td>
        </tr>
        <tr>
          <th>100</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>99</td>
          <td>True</td>
          <td>theobromine</td>
          <td>oral</td>
          <td>None</td>
          <td>None</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>theobromine</td>
          <td>1.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>101</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>-1</td>
          <td>False</td>
          <td>theophylline</td>
          <td>oral</td>
          <td>None</td>
          <td>None</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>theophylline</td>
          <td>1.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>g</td>
        </tr>
        <tr>
          <th>102</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>101</td>
          <td>True</td>
          <td>theophylline</td>
          <td>oral</td>
          <td>None</td>
          <td>None</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>theophylline</td>
          <td>1.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>103</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>-1</td>
          <td>False</td>
          <td>caffeine</td>
          <td>oral</td>
          <td>None</td>
          <td>None</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>caffeine</td>
          <td>1.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>g</td>
        </tr>
        <tr>
          <th>104</th>
          <td>PKDB99997</td>
          <td>Test3</td>
          <td>103</td>
          <td>True</td>
          <td>caffeine</td>
          <td>oral</td>
          <td>None</td>
          <td>None</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>caffeine</td>
          <td>1.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>105</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>-1</td>
          <td>False</td>
          <td>Dcaf</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>caffeine</td>
          <td>200.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>mg</td>
        </tr>
        <tr>
          <th>106</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>105</td>
          <td>True</td>
          <td>Dcaf</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>hr</td>
          <td>...</td>
          <td>caffeine</td>
          <td>0.200000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>107</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>-1</td>
          <td>False</td>
          <td>Dlom</td>
          <td>oral</td>
          <td>capsule</td>
          <td>multiple dose</td>
          <td>NaN</td>
          <td>None</td>
          <td>...</td>
          <td>lomefloxacin</td>
          <td>400.000000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>mg</td>
        </tr>
        <tr>
          <th>108</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>107</td>
          <td>True</td>
          <td>Dlom</td>
          <td>oral</td>
          <td>capsule</td>
          <td>multiple dose</td>
          <td>NaN</td>
          <td>None</td>
          <td>...</td>
          <td>lomefloxacin</td>
          <td>0.400000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram</td>
        </tr>
      </tbody>
    </table>
    <p>18 rows × 22 columns</p>
    </div>



.. code:: ipython3

    data.outputs_mi




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
          <th></th>
          <th></th>
          <th></th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>normed</th>
          <th>calculated</th>
          <th>tissue</th>
          <th>time</th>
          <th>time_unit</th>
          <th>measurement_type</th>
          <th>choice</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
        <tr>
          <th>output_pk</th>
          <th>intervention_pk</th>
          <th>group_pk</th>
          <th>individual_pk</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1409</th>
          <th>96</th>
          <th>-1</th>
          <th>39</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>False</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>thalf</td>
          <td>None</td>
          <td>midazolam</td>
          <td>2.30</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>hr</td>
        </tr>
        <tr>
          <th>1410</th>
          <th>96</th>
          <th>-1</th>
          <th>39</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>False</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>vd</td>
          <td>None</td>
          <td>midazolam</td>
          <td>0.71</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>l/kg</td>
        </tr>
        <tr>
          <th>1411</th>
          <th>96</th>
          <th>-1</th>
          <th>39</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>False</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>clearance</td>
          <td>None</td>
          <td>midazolam</td>
          <td>292.00</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>ml/min</td>
        </tr>
        <tr>
          <th>1412</th>
          <th>96</th>
          <th>-1</th>
          <th>39</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>False</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>clearance_unbound</td>
          <td>None</td>
          <td>midazolam</td>
          <td>5840.00</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>ml/min</td>
        </tr>
        <tr>
          <th>1413</th>
          <th>96</th>
          <th>-1</th>
          <th>39</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>False</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>plasma_binding</td>
          <td>None</td>
          <td>midazolam</td>
          <td>95.00</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>percent</td>
        </tr>
        <tr>
          <th>...</th>
          <th>...</th>
          <th>...</th>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2604</th>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>True</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>thalf</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>NaN</td>
          <td>9.36</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>hour</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">2605</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>True</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>vd</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>NaN</td>
          <td>90.30</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>liter</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>True</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>vd</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>NaN</td>
          <td>90.30</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>liter</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">2606</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>True</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>tmax</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>NaN</td>
          <td>6.00</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>hour</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>True</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>None</td>
          <td>tmax</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>NaN</td>
          <td>6.00</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>hour</td>
        </tr>
      </tbody>
    </table>
    <p>1106 rows × 19 columns</p>
    </div>



.. code:: ipython3

    data.timecourses_mi




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
          <th></th>
          <th></th>
          <th></th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>normed</th>
          <th>tissue</th>
          <th>time</th>
          <th>time_unit</th>
          <th>measurement_type</th>
          <th>choice</th>
          <th>substance</th>
          <th>value</th>
          <th>mean</th>
          <th>median</th>
          <th>min</th>
          <th>max</th>
          <th>sd</th>
          <th>se</th>
          <th>cv</th>
          <th>unit</th>
        </tr>
        <tr>
          <th>timecourse_pk</th>
          <th>intervention_pk</th>
          <th>group_pk</th>
          <th>individual_pk</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>67</th>
          <th>96</th>
          <th>20</th>
          <th>-1</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.17, 0.33, 0.5, 0.75, 1.0, 1.5, 2.0, 3....</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>midazolam</td>
          <td>None</td>
          <td>[185.0, 144.0, 121.0, 106.0, 83.8, 76.7, 58.3,...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[23.3, 18.2, 20.6, 26.8, 10.3, 19.9, 9.37, 13....</td>
          <td>None</td>
          <td>None</td>
          <td>ng/ml</td>
        </tr>
        <tr>
          <th>68</th>
          <th>94</th>
          <th>20</th>
          <th>-1</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.17, 0.33, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4....</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>midazolam</td>
          <td>None</td>
          <td>[10.1, 132.0, 134.0, 96.7, 96.6, 67.7, 57.5, 4...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[4.76, 74.8, 30.1, 42.3, 52.9, 25.1, 11.8, 10....</td>
          <td>None</td>
          <td>None</td>
          <td>ng/ml</td>
        </tr>
        <tr>
          <th>69</th>
          <th>96</th>
          <th>20</th>
          <th>-1</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.17, 0.33, 0.5, 0.75, 1.0, 1.5, 2.0, 3....</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>midazolam</td>
          <td>None</td>
          <td>[0.000185, 0.000144, 0.000121, 0.000106, 8.38e...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[2.33e-05, 1.82e-05, 2.06e-05, 2.68e-05, 1.03e...</td>
          <td>[9.52e-06, 7.42e-06, 8.4e-06, 1.09e-05, 4.19e-...</td>
          <td>[0.126, 0.126, 0.171, 0.253, 0.123, 0.259, 0.1...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>70</th>
          <th>94</th>
          <th>20</th>
          <th>-1</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.17, 0.33, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4....</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>midazolam</td>
          <td>None</td>
          <td>[1.01e-05, 0.000132, 0.000134, 9.67e-05, 9.66e...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[4.76e-06, 7.49e-05, 3.01e-05, 4.23e-05, 5.29e...</td>
          <td>[1.94e-06, 3.06e-05, 1.23e-05, 1.73e-05, 2.16e...</td>
          <td>[0.471, 0.566, 0.224, 0.437, 0.548, 0.37, 0.20...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>71</th>
          <th>98</th>
          <th>22</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[0.0, 7.92, 15.1, 15.2, 14.4, 13.7, 12.3, 11.4...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.872, 1.48, 1.95, 1.81, 2.15, 1.61, 13....</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>72</th>
          <th>98</th>
          <th>22</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.482, 1.1, 2.27, 2.75, 3.99, 5.92, 9.63...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.894, 0.688, 0.55, 0.894, 0.619, 1.17, ...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>73</th>
          <th>98</th>
          <th>22</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.547, 1.09, 1.55, 2.44, 3.3, 3.9, 4.12,...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.0911, 0.228, 0.205, 0.592, 0.592, 0.6,...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>74</th>
          <th>98</th>
          <th>23</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[0.0, 9.64, 14.6, 15.4, 15.5, 13.9, 13.5, 12.7...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.357, 0.57, 0.5, 1.2, 1.57, 0.97, 1.1, ...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>75</th>
          <th>98</th>
          <th>23</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.138, 1.03, 1.79, 2.48, 3.37, 4.61, 8.6...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 1.03, 0.55, 1.03, 1.24, 1.44, 1.38, 1.03...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>76</th>
          <th>98</th>
          <th>23</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.501, 0.934, 1.62, 2.07, 2.64, 3.23, 4....</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.137, 0.342, 0.183, 0.364, 0.501, 0.592...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>77</th>
          <th>98</th>
          <th>24</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[0.0, 8.39, 14.5, 15.2, 15.2, 15.2, 14.2, 13.1...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 1.21, 1.07, 1.41, 1.88, 0.537, 0.604, 1....</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>78</th>
          <th>98</th>
          <th>24</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.206, 0.688, 1.31, 2.06, 3.1, 3.72, 7.7...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.482, 0.482, 0.344, 0.688, 0.206, 0.826...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>79</th>
          <th>98</th>
          <th>24</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.205, 1.12, 1.53, 2.14, 2.87, 3.55, 4.8...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.251, 0.114, 0.0738, 0.2, 0.387, 0.319,...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>80</th>
          <th>98</th>
          <th>25</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[0.0671, 18.3, 25.1, 21.9, 21.0, 20.1, 18.9, 1...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 4.16, 2.95, 1.61, 1.61, 0.671, 1.01, 17....</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>81</th>
          <th>98</th>
          <th>25</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.619, 1.17, 2.06, 3.03, 3.99, 5.3, 8.74...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 1.1, 0.757, 1.03, 1.03, 0.963, 2.0, 1.44...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>82</th>
          <th>98</th>
          <th>25</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.501, 2.21, 2.96, 3.6, 3.9, 4.56, 5.92,...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.251, 0.319, 0.364, 0.524, 0.41, 0.478,...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/L</td>
        </tr>
        <tr>
          <th>83</th>
          <th>98</th>
          <th>22</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[0.0, 0.00792, 0.0151, 0.0152, 0.0144, 0.0137,...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.000872, 0.00148, 0.00195, 0.00181, 0.0...</td>
          <td>[nan, 0.000276, 0.000467, 0.000615, 0.000573, ...</td>
          <td>[nan, 0.11, 0.0978, 0.128, 0.126, 0.157, 0.13,...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>84</th>
          <th>98</th>
          <th>22</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.000482, 0.0011, 0.00227, 0.00275, 0.00...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.000894, 0.000688, 0.00055, 0.000894, 0...</td>
          <td>[nan, 0.000283, 0.000218, 0.000174, 0.000283, ...</td>
          <td>[nan, 1.86, 0.625, 0.242, 0.325, 0.155, 0.198,...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>85</th>
          <th>98</th>
          <th>22</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.000547, 0.00109, 0.00155, 0.00244, 0.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 9.11e-05, 0.000228, 0.000205, 0.000592, ...</td>
          <td>[nan, 2.88e-05, 7.2e-05, 6.48e-05, 0.000187, 0...</td>
          <td>[nan, 0.167, 0.208, 0.132, 0.243, 0.179, 0.154...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>86</th>
          <th>98</th>
          <th>23</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[0.0, 0.00964, 0.0146, 0.0154, 0.0155, 0.0139,...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.000357, 0.00057, 0.0005, 0.0012, 0.001...</td>
          <td>[nan, 0.000113, 0.00018, 0.000158, 0.000379, 0...</td>
          <td>[nan, 0.037, 0.039, 0.0325, 0.0772, 0.113, 0.0...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>87</th>
          <th>98</th>
          <th>23</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.000138, 0.00103, 0.00179, 0.00248, 0.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.00103, 0.00055, 0.00103, 0.00124, 0.00...</td>
          <td>[nan, 0.000326, 0.000174, 0.000326, 0.000392, ...</td>
          <td>[nan, 7.5, 0.533, 0.577, 0.5, 0.429, 0.299, 0....</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>88</th>
          <th>98</th>
          <th>23</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.000501, 0.000934, 0.00162, 0.00207, 0....</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.000137, 0.000342, 0.000183, 0.000364, ...</td>
          <td>[nan, 4.32e-05, 0.000108, 5.78e-05, 0.000115, ...</td>
          <td>[nan, 0.273, 0.366, 0.113, 0.176, 0.19, 0.183,...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>89</th>
          <th>98</th>
          <th>24</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[0.0, 0.00839, 0.0145, 0.0152, 0.0152, 0.0152,...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.00121, 0.00107, 0.00141, 0.00188, 0.00...</td>
          <td>[nan, 0.000382, 0.00034, 0.000446, 0.000594, 0...</td>
          <td>[nan, 0.144, 0.0741, 0.0925, 0.123, 0.0352, 0....</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>90</th>
          <th>98</th>
          <th>24</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.000206, 0.000688, 0.00131, 0.00206, 0....</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.000482, 0.000482, 0.000344, 0.000688, ...</td>
          <td>[nan, 0.000152, 0.000152, 0.000109, 0.000218, ...</td>
          <td>[nan, 2.33, 0.7, 0.263, 0.333, 0.0667, 0.222, ...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>91</th>
          <th>98</th>
          <th>24</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.000205, 0.00112, 0.00153, 0.00214, 0.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.000251, 0.000114, 7.38e-05, 0.0002, 0....</td>
          <td>[nan, 7.92e-05, 3.6e-05, 2.33e-05, 6.32e-05, 0...</td>
          <td>[nan, 1.22, 0.102, 0.0484, 0.0934, 0.135, 0.08...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>92</th>
          <th>98</th>
          <th>25</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol</td>
          <td>None</td>
          <td>[6.71e-05, 0.0183, 0.0251, 0.0219, 0.021, 0.02...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.00416, 0.00295, 0.00161, 0.00161, 0.00...</td>
          <td>[nan, 0.00132, 0.000934, 0.000509, 0.000509, 0...</td>
          <td>[nan, 0.228, 0.118, 0.0734, 0.0767, 0.0334, 0....</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>93</th>
          <th>98</th>
          <th>25</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol glucuronide</td>
          <td>None</td>
          <td>[0.0, 0.000619, 0.00117, 0.00206, 0.00303, 0.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.0011, 0.000757, 0.00103, 0.00103, 0.00...</td>
          <td>[nan, 0.000348, 0.000239, 0.000326, 0.000326, ...</td>
          <td>[nan, 1.78, 0.647, 0.5, 0.341, 0.241, 0.377, 0...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>94</th>
          <th>98</th>
          <th>25</th>
          <th>-1</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.125, 0.25, 0.292, 0.333, 0.417, 0.5, 0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paracetamol sulfate</td>
          <td>None</td>
          <td>[0.0, 0.000501, 0.00221, 0.00296, 0.0036, 0.00...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[nan, 0.000251, 0.000319, 0.000364, 0.000524, ...</td>
          <td>[nan, 7.92e-05, 0.000101, 0.000115, 0.000166, ...</td>
          <td>[nan, 0.5, 0.144, 0.123, 0.146, 0.105, 0.105, ...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>95</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>caffeine</td>
          <td>None</td>
          <td>[0.155, 1.07, 3.16, 4.13, 3.95, 3.54, 3.37, 3....</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.169, 0.667, 1.35, 0.469, 0.343, 0.367, 0.38...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/l</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">96</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>caffeine</td>
          <td>None</td>
          <td>[0.15, 0.817, 2.6, 3.48, 3.81, 3.68, 3.38, 3.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.189, 0.329, 1.15, 0.759, 0.522, 0.305, 0.33...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/l</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>caffeine</td>
          <td>None</td>
          <td>[0.15, 0.817, 2.6, 3.48, 3.81, 3.68, 3.38, 3.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.189, 0.329, 1.15, 0.759, 0.522, 0.305, 0.33...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/l</td>
        </tr>
        <tr>
          <th>97</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>caffeine</td>
          <td>None</td>
          <td>[0.000155, 0.00107, 0.00316, 0.00413, 0.00395,...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.000169, 0.000667, 0.00135, 0.000469, 0.0003...</td>
          <td>[4.23e-05, 0.000167, 0.000337, 0.000117, 8.58e...</td>
          <td>[1.09, 0.622, 0.427, 0.114, 0.087, 0.104, 0.11...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">98</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>caffeine</td>
          <td>None</td>
          <td>[0.00015, 0.000817, 0.0026, 0.00348, 0.00381, ...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.000189, 0.000329, 0.00115, 0.000759, 0.0005...</td>
          <td>[4.71e-05, 8.22e-05, 0.000287, 0.00019, 0.0001...</td>
          <td>[1.26, 0.402, 0.441, 0.218, 0.137, 0.0828, 0.0...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>caffeine</td>
          <td>None</td>
          <td>[0.00015, 0.000817, 0.0026, 0.00348, 0.00381, ...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.000189, 0.000329, 0.00115, 0.000759, 0.0005...</td>
          <td>[4.71e-05, 8.22e-05, 0.000287, 0.00019, 0.0001...</td>
          <td>[1.26, 0.402, 0.441, 0.218, 0.137, 0.0828, 0.0...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>99</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>None</td>
          <td>[0.361, 0.462, 0.637, 0.807, 0.854, 0.973, 1.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.2, 0.206, 0.262, 0.316, 0.167, 0.17, 0.199,...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/l</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">100</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>None</td>
          <td>[0.383, 0.446, 0.591, 0.731, 0.831, 0.935, 1.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.13, 0.193, 0.216, 0.236, 0.246, 0.19, 0.195...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/l</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>None</td>
          <td>[0.383, 0.446, 0.591, 0.731, 0.831, 0.935, 1.0...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.13, 0.193, 0.216, 0.236, 0.246, 0.19, 0.195...</td>
          <td>None</td>
          <td>None</td>
          <td>mg/l</td>
        </tr>
        <tr>
          <th>101</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>None</td>
          <td>[0.000361, 0.000462, 0.000637, 0.000807, 0.000...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.0002, 0.000206, 0.000262, 0.000316, 0.00016...</td>
          <td>[5.01e-05, 5.15e-05, 6.54e-05, 7.9e-05, 4.18e-...</td>
          <td>[0.556, 0.446, 0.411, 0.392, 0.196, 0.175, 0.1...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">102</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>None</td>
          <td>[0.000383, 0.000446, 0.000591, 0.000731, 0.000...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.00013, 0.000193, 0.000216, 0.000236, 0.0002...</td>
          <td>[3.25e-05, 4.83e-05, 5.4e-05, 5.9e-05, 6.15e-0...</td>
          <td>[0.34, 0.433, 0.366, 0.323, 0.296, 0.204, 0.18...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>concentration</td>
          <td>None</td>
          <td>paraxanthine</td>
          <td>None</td>
          <td>[0.000383, 0.000446, 0.000591, 0.000731, 0.000...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.00013, 0.000193, 0.000216, 0.000236, 0.0002...</td>
          <td>[3.25e-05, 4.83e-05, 5.4e-05, 5.9e-05, 6.15e-0...</td>
          <td>[0.34, 0.433, 0.366, 0.323, 0.296, 0.204, 0.18...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>103</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>metabolic ratio</td>
          <td>None</td>
          <td>px/caf</td>
          <td>None</td>
          <td>[2.33, 0.431, 0.201, 0.195, 0.217, 0.275, 0.32...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.611, 0.301, 0.277, 0.111, 0.0827, 0.111, 0....</td>
          <td>None</td>
          <td>None</td>
          <td>none</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">104</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>metabolic ratio</td>
          <td>None</td>
          <td>px/caf</td>
          <td>None</td>
          <td>[2.56, 0.546, 0.227, 0.21, 0.218, 0.254, 0.308...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.586, 0.208, 0.265, 0.167, 0.126, 0.0912, 0....</td>
          <td>None</td>
          <td>None</td>
          <td>none</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>False</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>metabolic ratio</td>
          <td>None</td>
          <td>px/caf</td>
          <td>None</td>
          <td>[2.56, 0.546, 0.227, 0.21, 0.218, 0.254, 0.308...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.586, 0.208, 0.265, 0.167, 0.126, 0.0912, 0....</td>
          <td>None</td>
          <td>None</td>
          <td>none</td>
        </tr>
        <tr>
          <th>105</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>metabolic ratio</td>
          <td>None</td>
          <td>px/caf</td>
          <td>None</td>
          <td>[2.33, 0.431, 0.201, 0.195, 0.217, 0.275, 0.32...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.611, 0.301, 0.277, 0.111, 0.0827, 0.111, 0....</td>
          <td>[0.153, 0.0752, 0.0692, 0.0276, 0.0207, 0.0278...</td>
          <td>[0.262, 0.698, 1.37, 0.566, 0.382, 0.405, 0.43...</td>
          <td>none</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">106</th>
          <th>106</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>metabolic ratio</td>
          <td>None</td>
          <td>px/caf</td>
          <td>None</td>
          <td>[2.56, 0.546, 0.227, 0.21, 0.218, 0.254, 0.308...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.586, 0.208, 0.265, 0.167, 0.126, 0.0912, 0....</td>
          <td>[0.147, 0.0521, 0.0662, 0.0418, 0.0315, 0.0228...</td>
          <td>[0.229, 0.381, 1.17, 0.795, 0.577, 0.359, 0.38...</td>
          <td>none</td>
        </tr>
        <tr>
          <th>108</th>
          <th>27</th>
          <th>-1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>True</td>
          <td>plasma</td>
          <td>[0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0...</td>
          <td>hr</td>
          <td>metabolic ratio</td>
          <td>None</td>
          <td>px/caf</td>
          <td>None</td>
          <td>[2.56, 0.546, 0.227, 0.21, 0.218, 0.254, 0.308...</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>[0.586, 0.208, 0.265, 0.167, 0.126, 0.0912, 0....</td>
          <td>[0.147, 0.0521, 0.0662, 0.0418, 0.0315, 0.0228...</td>
          <td>[0.229, 0.381, 1.17, 0.795, 0.577, 0.359, 0.38...</td>
          <td>none</td>
        </tr>
      </tbody>
    </table>
    </div>


