.. code:: ipython3

    
    import pandas as pd
    from IPython.display import display
    
    # install pkdb_analysis via:
    #     git clone https://github.com/matthiaskoenig/pkdb_analysis (private)
    #     cd pkdb_analysis
    #     pip install -e .
    # in future:
    #     pip install pkdb_analsis
    
    from pkdb_analysis import PKDB, PKData, PKFilter
    from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP


.. code:: ipython3

     import sys
     print(sys.executable)
     print(sys.version)
     print(sys.version_info)



.. parsed-literal::

    /home/janek/.virtualenvs/pkdb_analysis/bin/python
    3.7.9 (default, Aug 18 2020, 02:07:21) 
    [GCC 9.3.0]
    sys.version_info(major=3, minor=7, micro=9, releaselevel='final', serial=0)


Filter data
===========

A recurring task is to filter data for a certain question. E.g. to
compare two groups, or get the subset of data for all healthy smokers.

We work again with our test data set and will filter various subsets
from it.

.. code:: ipython3

    #test_data = PKDB.query()
    #TEST_HDF5 ="./test_data.hdf5"
    
    test_data = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)

.. code:: ipython3

    test_data._concise()
    print(test_data)


.. parsed-literal::

    ------------------------------
    PKData (140200057729936)
    ------------------------------
    studies           124  (  124)
    groups            284  ( 2613)
    individuals      3082  (27405)
    interventions     366  (  366)
    outputs         19407  (29053)
    timecourses       722  (  722)
    scatters           80  (   80)
    ------------------------------


.. code:: ipython3

    test_data1 =  test_data.filter_study(lambda x: x["licence"] == "open")

.. code:: ipython3

    print(test_data1)


.. parsed-literal::

    ------------------------------
    PKData (140200057063312)
    ------------------------------
    studies            12  (   12)
    groups            284  ( 2613)
    individuals      3082  (27405)
    interventions     366  (  366)
    outputs         19407  (29053)
    timecourses       722  (  722)
    scatters           80  (   80)
    ------------------------------


.. code:: ipython3

    list(test_data.study_sids)[:10]




.. parsed-literal::

    ['PKDB00013',
     '26862045',
     '10634135',
     '4027137',
     'PKDB00011',
     'PKDB00042',
     'PKDB00045',
     '13053413',
     'PKDB00008',
     'PKDB00036']



Filter functions
----------------

The main principle for filtering ``PKData`` is by using the ``filter_*``
and ``exclude_*`` functionality.

A key principle are hereby filter functions which for a given DataFrame
return a logical index.

Depending on which subset of information this should be applied the
``groups``, ``individuals``, ``subjects`` (groups and individuals),
``outputs`` and ``timecourses``.

Filter by ``study_sid``
-----------------------

A first example is filtering by ``study_sid``, i.e. we only want the
subset of data from a single study. An overview over the existing study
sids in the dataset is available via

Filtering a subset of data works by providing filter/selection functions
which select a subset of the data. The filters are written on the
``groups``, ``individuals``

.. code:: ipython3

    def is_PKDB99999(d):
        """Filter for specific study_sid. """
        return d.study_sid == "PKDB00198"
    
    data = test_data.filter_intervention(is_PKDB99999)
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (140200051078672)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    scatters           80  (   80)
    ------------------------------


The PKData now only contains data for the given study_sid:

.. code:: ipython3

    print(data.study_sids)


.. parsed-literal::

    {'7371463', '26862045', '4027137', '3557314', '2921843', 'PKDB00045', '25891161', '2185297', 'Sandberg1988', '25853045', 'PKDB00126', 'Nakazawa1988', 'PKDB00012', 'Lennard1982', '15022032', '6712142', '28929443', '1033273', 'PKDB00015', 'PKDB00210', 'PKDB00002', 'Trang1985'}


.. code:: ipython3

    # for instance interventions
    display(data.interventions)



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
          <th>Unnamed: 0</th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>intervention_pk</th>
          <th>raw_pk</th>
          <th>normed</th>
          <th>name</th>
          <th>route</th>
          <th>route_label</th>
          <th>form</th>
          <th>...</th>
          <th>substance_label</th>
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
      </tbody>
    </table>
    <p>0 rows × 31 columns</p>
    </div>



.. parsed-literal::

    Empty DataFrame
    Columns: [Unnamed: 0, study_sid, study_name, intervention_pk, raw_pk, normed, name, route, route_label, form, form_label, application, application_label, time, time_end, time_unit, measurement_type, measurement_type_label, choice, choice_label, substance, substance_label, value, mean, median, min, max, sd, se, cv, unit]
    Index: []
    
    [0 rows x 31 columns]


One could also define this as a simple lambda function

.. code:: ipython3

    data = test_data.filter_intervention(lambda d: d.study_sid == "PKDB00198")
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (140200047715280)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    scatters           80  (   80)
    ------------------------------


Concise data
------------

All operations on ``PKData`` leave the data in a consistent manner. E.g.
if an intervention is filtered out also all the outputs using this
intervention are filtered out. This behavior is controlled by the
``concise`` flag on most operations.

.. code:: ipython3

    t1 = test_data.filter_intervention(is_PKDB99999)
    t2 = test_data.filter_intervention(is_PKDB99999, concise=False)
    print(t1)
    print(t2)


.. parsed-literal::

    ------------------------------
    PKData (140200067512720)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    scatters           80  (   80)
    ------------------------------
    ------------------------------
    PKData (140200047779152)
    ------------------------------
    studies           124  (  124)
    groups            284  ( 2613)
    individuals      3082  (27405)
    interventions       0  (    0)
    outputs         19407  (29053)
    timecourses       722  (  722)
    scatters           80  (   80)
    ------------------------------


.. code:: ipython3

    # FIXME: only normed data
    t1.interventions_mi




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

    t2.interventions_mi




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

    t2.outputs



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
          <th>Unnamed: 0</th>
          <th>study_name</th>
          <th>measurement_type</th>
          <th>tissue</th>
          <th>sd</th>
          <th>se</th>
          <th>min</th>
          <th>group_pk</th>
          <th>output_pk</th>
          <th>time_unit</th>
          <th>...</th>
          <th>max</th>
          <th>substance</th>
          <th>label</th>
          <th>individual_pk</th>
          <th>unit</th>
          <th>cv</th>
          <th>median</th>
          <th>mean</th>
          <th>time</th>
          <th>choice</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0</td>
          <td>Abernethy1985</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>210625</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>23952</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>Abernethy1985</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>210628</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>23955</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>Abernethy1985</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>210631</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>23958</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>Abernethy1985</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>210635</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>23962</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>4</td>
          <td>Abernethy1985</td>
          <td>clearance</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>210640</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>23967</td>
          <td>liter / hour / kilogram</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
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
          <td>...</td>
        </tr>
        <tr>
          <th>29048</th>
          <td>29048</td>
          <td>Barnett1990</td>
          <td>cmax</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>263142</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>30567</td>
          <td>gram / liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>29049</th>
          <td>29049</td>
          <td>Barnett1990</td>
          <td>vd-ss</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>263146</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>30567</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>29050</th>
          <td>29050</td>
          <td>Barnett1990</td>
          <td>cmax</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>263159</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>30567</td>
          <td>gram / liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>29051</th>
          <td>29051</td>
          <td>Barnett1990</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>263163</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>30567</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>29052</th>
          <td>29052</td>
          <td>Barnett1990</td>
          <td>vd-ss</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>-1</td>
          <td>263164</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>30567</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>29053 rows × 27 columns</p>
    </div>




.. parsed-literal::

           Unnamed: 0     study_name measurement_type  tissue  sd  se  min  \
    0               0  Abernethy1985            thalf  plasma NaN NaN  NaN   
    1               1  Abernethy1985            thalf  plasma NaN NaN  NaN   
    2               2  Abernethy1985            thalf  plasma NaN NaN  NaN   
    3               3  Abernethy1985            thalf  plasma NaN NaN  NaN   
    4               4  Abernethy1985        clearance  plasma NaN NaN  NaN   
    ...           ...            ...              ...     ...  ..  ..  ...   
    29048       29048    Barnett1990             cmax  plasma NaN NaN  NaN   
    29049       29049    Barnett1990            vd-ss  plasma NaN NaN  NaN   
    29050       29050    Barnett1990             cmax  plasma NaN NaN  NaN   
    29051       29051    Barnett1990               vd  plasma NaN NaN  NaN   
    29052       29052    Barnett1990            vd-ss  plasma NaN NaN  NaN   
    
           group_pk  output_pk time_unit  ...  max  substance  label  \
    0            -1     210625       NaN  ...  NaN        caf    NaN   
    1            -1     210628       NaN  ...  NaN        caf    NaN   
    2            -1     210631       NaN  ...  NaN        caf    NaN   
    3            -1     210635       NaN  ...  NaN        caf    NaN   
    4            -1     210640       NaN  ...  NaN        caf    NaN   
    ...         ...        ...       ...  ...  ...        ...    ...   
    29048        -1     263142       NaN  ...  NaN        caf    NaN   
    29049        -1     263146       NaN  ...  NaN        caf    NaN   
    29050        -1     263159       NaN  ...  NaN        caf    NaN   
    29051        -1     263163       NaN  ...  NaN        caf    NaN   
    29052        -1     263164       NaN  ...  NaN        caf    NaN   
    
          individual_pk                     unit  cv median  mean time choice  
    0             23952                     hour NaN    NaN   NaN  NaN    NaN  
    1             23955                     hour NaN    NaN   NaN  NaN    NaN  
    2             23958                     hour NaN    NaN   NaN  NaN    NaN  
    3             23962                     hour NaN    NaN   NaN  NaN    NaN  
    4             23967  liter / hour / kilogram NaN    NaN   NaN  NaN    NaN  
    ...             ...                      ...  ..    ...   ...  ...    ...  
    29048         30567             gram / liter NaN    NaN   NaN  NaN    NaN  
    29049         30567                    liter NaN    NaN   NaN  NaN    NaN  
    29050         30567             gram / liter NaN    NaN   NaN  NaN    NaN  
    29051         30567                    liter NaN    NaN   NaN  NaN    NaN  
    29052         30567                    liter NaN    NaN   NaN  NaN    NaN  
    
    [29053 rows x 27 columns]



Query groups and individuals
----------------------------

2.1 Get data for groups with characteristica/keywords X
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

healthy=True, smoking=N, disease=None, individual queries and
combinations.

.. code:: ipython3

    def is_healthy(d): 
        # healthy is reported and True
        return (d.measurement_type == "healthy") & (d.choice == "Y")
    
    def disease(d):
        # any disease is reported
        return  d.measurement_type == "disease"
    
    def smoking(d):
        # smoking status is curated for study (this could by Y/N/NR)
        return  d.measurement_type == "smoking"
    
    def nonsmoker(d):
        # smoking is reported and no
        return smoking(d) & (d.choice == "N")
    
    def smoker(d):
        # smoking is reported and yes
        return smoking(d) & (d.choice == "Y")

.. code:: ipython3

    test_data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)

``f_idx`` can be a single function, or a list of functions. A list of
functions are applied successively and is equivalent to “AND logic”. “OR
logic” can be directly applied on the index.

.. code:: ipython3

    healthy_nonsmoker = test_data.filter_subject(f_idx=[is_healthy, nonsmoker])
    print(healthy_nonsmoker)
    healthy_nonsmoker.groups_mi


.. parsed-literal::

    ------------------------------
    PKData (140200056602832)
    ------------------------------
    studies            81  (   81)
    groups            143  ( 1396)
    individuals      1150  (10810)
    interventions     238  (  238)
    outputs         10578  (14843)
    timecourses       438  (  438)
    scatters           80  (   80)
    ------------------------------



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
          <th>Unnamed: 0</th>
          <th>study_name</th>
          <th>study_sid</th>
          <th>measurement_type</th>
          <th>group_count</th>
          <th>group_name</th>
          <th>max</th>
          <th>substance</th>
          <th>count</th>
          <th>group_parent_pk</th>
          <th>sd</th>
          <th>unit</th>
          <th>se</th>
          <th>min</th>
          <th>cv</th>
          <th>median</th>
          <th>mean</th>
          <th>choice</th>
          <th>value</th>
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
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">3463</th>
          <th>67383</th>
          <td>10</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>smoking</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>N</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67384</th>
          <td>11</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>age</td>
          <td>9</td>
          <td>OCS</td>
          <td>30.0</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>year</td>
          <td>1.0</td>
          <td>23.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>26.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67385</th>
          <td>12</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>species</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>homo sapiens</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67386</th>
          <td>13</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>healthy</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>Y</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67387</th>
          <td>14</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>sex</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>F</td>
          <td>NaN</td>
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
          <td>...</td>
        </tr>
        <tr>
          <th rowspan="5" valign="top">4001</th>
          <th>80932</th>
          <td>3677</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1a/*1a</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80933</th>
          <td>3678</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1c/*1f</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80934</th>
          <td>3681</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>2</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1c*1f/*1c*1f</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80935</th>
          <td>3682</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>6</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1a/*1f</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80936</th>
          <td>3683</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>2</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1f/*1f</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>1396 rows × 19 columns</p>
    </div>




.. parsed-literal::

                                 Unnamed: 0     study_name  study_sid  \
    group_pk characteristica_pk                                         
    3463     67383                       10  Abernethy1985  PKDB00001   
             67384                       11  Abernethy1985  PKDB00001   
             67385                       12  Abernethy1985  PKDB00001   
             67386                       13  Abernethy1985  PKDB00001   
             67387                       14  Abernethy1985  PKDB00001   
    ...                                 ...            ...        ...   
    4001     80932                     3677       Tian2019   30387917   
             80933                     3678       Tian2019   30387917   
             80934                     3681       Tian2019   30387917   
             80935                     3682       Tian2019   30387917   
             80936                     3683       Tian2019   30387917   
    
                                measurement_type  group_count group_name   max  \
    group_pk characteristica_pk                                                  
    3463     67383                       smoking            9        OCS   NaN   
             67384                           age            9        OCS  30.0   
             67385                       species            9        OCS   NaN   
             67386                       healthy            9        OCS   NaN   
             67387                           sex            9        OCS   NaN   
    ...                                      ...          ...        ...   ...   
    4001     80932               CYP1A2 genotype           12        men   NaN   
             80933               CYP1A2 genotype           12        men   NaN   
             80934               CYP1A2 genotype           12        men   NaN   
             80935               CYP1A2 genotype           12        men   NaN   
             80936               CYP1A2 genotype           12        men   NaN   
    
                                substance  count  group_parent_pk  sd  unit   se  \
    group_pk characteristica_pk                                                    
    3463     67383                    nan     18             3462 NaN   NaN  NaN   
             67384                    nan     18             3462 NaN  year  1.0   
             67385                    nan     18             3462 NaN   NaN  NaN   
             67386                    nan     18             3462 NaN   NaN  NaN   
             67387                    nan     18             3462 NaN   NaN  NaN   
    ...                               ...    ...              ...  ..   ...  ...   
    4001     80932                    nan      1             3999 NaN   NaN  NaN   
             80933                    nan      1             3999 NaN   NaN  NaN   
             80934                    nan      2             3999 NaN   NaN  NaN   
             80935                    nan      6             3999 NaN   NaN  NaN   
             80936                    nan      2             3999 NaN   NaN  NaN   
    
                                  min  cv  median  mean         choice  value  
    group_pk characteristica_pk                                                
    3463     67383                NaN NaN     NaN   NaN              N    NaN  
             67384               23.0 NaN     NaN  26.0            NaN    NaN  
             67385                NaN NaN     NaN   NaN   homo sapiens    NaN  
             67386                NaN NaN     NaN   NaN              Y    NaN  
             67387                NaN NaN     NaN   NaN              F    NaN  
    ...                           ...  ..     ...   ...            ...    ...  
    4001     80932                NaN NaN     NaN   NaN        *1a/*1a    NaN  
             80933                NaN NaN     NaN   NaN        *1c/*1f    NaN  
             80934                NaN NaN     NaN   NaN  *1c*1f/*1c*1f    NaN  
             80935                NaN NaN     NaN   NaN        *1a/*1f    NaN  
             80936                NaN NaN     NaN   NaN        *1f/*1f    NaN  
    
    [1396 rows x 19 columns]



Often attributes are mixed for groups so we have to exclude the
opposites. In the example, the group ``20`` consists of 5 smokers and 1
nonsmoker. So for a subset of the group smoking is No. We can exclude
groups via

.. code:: ipython3

    healthy_nonsmoker = test_data.filter_subject([is_healthy, nonsmoker]).exclude_subject([smoker])
    print(healthy_nonsmoker)
    display(healthy_nonsmoker.groups_mi)


.. parsed-literal::

    ------------------------------
    PKData (140200051032848)
    ------------------------------
    studies            74  (   74)
    groups            124  ( 1144)
    individuals       927  ( 8619)
    interventions     221  (  221)
    outputs          9539  (13730)
    timecourses       397  (  397)
    scatters           80  (   80)
    ------------------------------



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
          <th>Unnamed: 0</th>
          <th>study_name</th>
          <th>study_sid</th>
          <th>measurement_type</th>
          <th>group_count</th>
          <th>group_name</th>
          <th>max</th>
          <th>substance</th>
          <th>count</th>
          <th>group_parent_pk</th>
          <th>sd</th>
          <th>unit</th>
          <th>se</th>
          <th>min</th>
          <th>cv</th>
          <th>median</th>
          <th>mean</th>
          <th>choice</th>
          <th>value</th>
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
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">3463</th>
          <th>67383</th>
          <td>10</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>smoking</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>N</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67384</th>
          <td>11</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>age</td>
          <td>9</td>
          <td>OCS</td>
          <td>30.0</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>year</td>
          <td>1.0</td>
          <td>23.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>26.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67385</th>
          <td>12</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>species</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>homo sapiens</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67386</th>
          <td>13</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>healthy</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>Y</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>67387</th>
          <td>14</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>sex</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>18</td>
          <td>3462</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>F</td>
          <td>NaN</td>
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
          <td>...</td>
        </tr>
        <tr>
          <th rowspan="5" valign="top">4001</th>
          <th>80932</th>
          <td>3677</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1a/*1a</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80933</th>
          <td>3678</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1c/*1f</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80934</th>
          <td>3681</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>2</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1c*1f/*1c*1f</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80935</th>
          <td>3682</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>6</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1a/*1f</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>80936</th>
          <td>3683</td>
          <td>Tian2019</td>
          <td>30387917</td>
          <td>CYP1A2 genotype</td>
          <td>12</td>
          <td>men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>2</td>
          <td>3999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>*1f/*1f</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>1144 rows × 19 columns</p>
    </div>



.. parsed-literal::

                                 Unnamed: 0     study_name  study_sid  \
    group_pk characteristica_pk                                         
    3463     67383                       10  Abernethy1985  PKDB00001   
             67384                       11  Abernethy1985  PKDB00001   
             67385                       12  Abernethy1985  PKDB00001   
             67386                       13  Abernethy1985  PKDB00001   
             67387                       14  Abernethy1985  PKDB00001   
    ...                                 ...            ...        ...   
    4001     80932                     3677       Tian2019   30387917   
             80933                     3678       Tian2019   30387917   
             80934                     3681       Tian2019   30387917   
             80935                     3682       Tian2019   30387917   
             80936                     3683       Tian2019   30387917   
    
                                measurement_type  group_count group_name   max  \
    group_pk characteristica_pk                                                  
    3463     67383                       smoking            9        OCS   NaN   
             67384                           age            9        OCS  30.0   
             67385                       species            9        OCS   NaN   
             67386                       healthy            9        OCS   NaN   
             67387                           sex            9        OCS   NaN   
    ...                                      ...          ...        ...   ...   
    4001     80932               CYP1A2 genotype           12        men   NaN   
             80933               CYP1A2 genotype           12        men   NaN   
             80934               CYP1A2 genotype           12        men   NaN   
             80935               CYP1A2 genotype           12        men   NaN   
             80936               CYP1A2 genotype           12        men   NaN   
    
                                substance  count  group_parent_pk  sd  unit   se  \
    group_pk characteristica_pk                                                    
    3463     67383                    nan     18             3462 NaN   NaN  NaN   
             67384                    nan     18             3462 NaN  year  1.0   
             67385                    nan     18             3462 NaN   NaN  NaN   
             67386                    nan     18             3462 NaN   NaN  NaN   
             67387                    nan     18             3462 NaN   NaN  NaN   
    ...                               ...    ...              ...  ..   ...  ...   
    4001     80932                    nan      1             3999 NaN   NaN  NaN   
             80933                    nan      1             3999 NaN   NaN  NaN   
             80934                    nan      2             3999 NaN   NaN  NaN   
             80935                    nan      6             3999 NaN   NaN  NaN   
             80936                    nan      2             3999 NaN   NaN  NaN   
    
                                  min  cv  median  mean         choice  value  
    group_pk characteristica_pk                                                
    3463     67383                NaN NaN     NaN   NaN              N    NaN  
             67384               23.0 NaN     NaN  26.0            NaN    NaN  
             67385                NaN NaN     NaN   NaN   homo sapiens    NaN  
             67386                NaN NaN     NaN   NaN              Y    NaN  
             67387                NaN NaN     NaN   NaN              F    NaN  
    ...                           ...  ..     ...   ...            ...    ...  
    4001     80932                NaN NaN     NaN   NaN        *1a/*1a    NaN  
             80933                NaN NaN     NaN   NaN        *1c/*1f    NaN  
             80934                NaN NaN     NaN   NaN  *1c*1f/*1c*1f    NaN  
             80935                NaN NaN     NaN   NaN        *1a/*1f    NaN  
             80936                NaN NaN     NaN   NaN        *1f/*1f    NaN  
    
    [1144 rows x 19 columns]


In addition often combinations of attributes have to be used to find the
correct subjects. For instance a combination of ``healthy`` and reported
``disease``

.. code:: ipython3

    def is_healthy(d): 
        # healthy is reported and True
        return (d.measurement_type == "healthy") & (d.choice == "Y")
    
    def disease(d):
        # any disease is reported
        return  d.measurement_type == "disease"
    
    healthy1 = test_data.filter_subject(is_healthy)
    healthy2 = test_data.exclude_subject(disease)
    healthy3 = test_data.filter_subject(is_healthy).exclude_subject(disease)
    
    print(healthy1)
    print(healthy2)
    print(healthy3)


.. parsed-literal::

    ------------------------------
    PKData (140200050707600)
    ------------------------------
    studies           111  (  111)
    groups            228  ( 2093)
    individuals      2165  (17531)
    interventions     345  (  345)
    outputs         15746  (25008)
    timecourses       607  (  607)
    scatters           80  (   80)
    ------------------------------
    ------------------------------
    PKData (140200056622672)
    ------------------------------
    studies           119  (  119)
    groups            234  ( 2107)
    individuals      2259  (17906)
    interventions     349  (  349)
    outputs         16367  (25485)
    timecourses       620  (  620)
    scatters           80  (   80)
    ------------------------------
    ------------------------------
    PKData (140200050706000)
    ------------------------------
    studies           110  (  110)
    groups            222  ( 2028)
    individuals      2058  (16812)
    interventions     337  (  337)
    outputs         15472  (24590)
    timecourses       603  (  603)
    scatters           80  (   80)
    ------------------------------


3 Query interventions
---------------------

3.1 Get outputs/timecourses for intervention with substance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

intervention with measurement_type “dosing” and substance “caffeine”

.. code:: ipython3

    def dosing_and_caffeine(d):
        return ((d["measurement_type"]=="dosing") & (d["substance"]=="caffeine"))

.. code:: ipython3

    test_data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)

.. code:: ipython3

    caffeine_data = test_data.filter_intervention(dosing_and_caffeine)

.. code:: ipython3

    print(caffeine_data)


.. parsed-literal::

    ------------------------------
    PKData (140200056614544)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    scatters           80  (   80)
    ------------------------------


4 Query outputs/timecourses
---------------------------

4.1 query by measurement_type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

filter all outputs with measurement_type auc_inf

.. code:: ipython3

    def is_auc_inf(d):
        return (d["measurement_type"]=="auc_inf")  
    
    test_data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)
    
    test_data = test_data.filter_output(is_auc_inf).delete_timecourses()
    print(test_data)


.. parsed-literal::

    ------------------------------
    PKData (140200056576144)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    scatters           80  (   80)
    ------------------------------


5 Other Query others
--------------------

5.1 Complex
~~~~~~~~~~~

get clearance of codeine for all.h5 subjects, which have been phenotyped
for cyp2d6.

.. code:: ipython3

    def is_cyp2d6_phenotyped(d):
        cyp2d6_phenotype_substances = ['spar/(2hspar+5hspar)', 'deb/4hdeb', 'dtf/dmt']
        return d["measurement_type"].isin(["metabolic phenotype", "metabolic ratio"]) & d["substance"].isin(cyp2d6_phenotype_substances)
    
    def codeine_clearance(d):
        return (d["measurement_type"]=="clearance") & (d["substance"]=="codeine")                                                        

.. code:: ipython3

    test_data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)
    
    phenotyped_data = test_data.filter_output(is_cyp2d6_phenotyped)

.. code:: ipython3

    test_data.groups = phenotyped_data.groups
    test_data.individuals = phenotyped_data.individuals
    test_data = test_data.filter_output(codeine_clearance).delete_timecourses()

.. code:: ipython3

    print(test_data)


.. parsed-literal::

    ------------------------------
    PKData (140200045658512)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    scatters           80  (   80)
    ------------------------------

