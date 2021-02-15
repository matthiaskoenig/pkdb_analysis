.. code:: ipython3

    
    import pandas as pd
    from IPython.display import display
    
    from pkdb_analysis import PKData, PKFilter
    from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP


Filter data
===========

A recurring task is to filter data for a certain question. E.g. to
compare two groups, or get the subset of data for all healthy smokers.

We work again with our test data set and will filter various subsets
from it.

.. code:: ipython3

    test_data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)
    print(test_data)


.. parsed-literal::

    ------------------------------
    PKData (139890849755408)
    ------------------------------
    studies           127  (  127)
    groups            429  ( 3733)
    individuals      3163  (28219)
    interventions     409  (  409)
    outputs         19407  (29053)
    timecourses       722  (  722)
    scatters           80  (   80)
    ------------------------------


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

.. code:: ipython3

    test_data.study_sids




.. parsed-literal::

    {'1033273',
     '10634135',
     '11839447',
     '13053413',
     '15022032',
     '16158445',
     '16261361',
     '18703023',
     '2060878',
     '20853468',
     '21591074',
     '2185297',
     '22673010',
     '25853045',
     '25891161',
     '26862045',
     '28929443',
     '2921843',
     '29230348',
     '30387917',
     '32071850',
     '3356110',
     '3557314',
     '3741730',
     '4027137',
     '6135578',
     '6712142',
     '6734698',
     '7371463',
     '7371698',
     '7742721',
     '7775610',
     '8445222',
     'Arnaud1981',
     'Arold2005',
     'Bchir2006',
     'Becker1984',
     'Bozikas2004',
     'Broughton1981',
     'Callahan1982',
     'Cattarossi1988',
     'Christensen2002',
     'Cysneiros2007',
     'Djordjevic2008',
     'He2017',
     'Kamimori1999',
     'Laizure2017',
     'Lane1992',
     'Lennard1982',
     'Matthaei2016',
     'Nakazawa1988',
     'PKDB00001',
     'PKDB00002',
     'PKDB00003',
     'PKDB00004',
     'PKDB00005',
     'PKDB00006',
     'PKDB00007',
     'PKDB00008',
     'PKDB00009',
     'PKDB00010',
     'PKDB00011',
     'PKDB00012',
     'PKDB00013',
     'PKDB00014',
     'PKDB00015',
     'PKDB00016',
     'PKDB00017',
     'PKDB00018',
     'PKDB00019',
     'PKDB00032',
     'PKDB00033',
     'PKDB00034',
     'PKDB00035',
     'PKDB00036',
     'PKDB00037',
     'PKDB00038',
     'PKDB00039',
     'PKDB00040',
     'PKDB00041',
     'PKDB00042',
     'PKDB00043',
     'PKDB00044',
     'PKDB00045',
     'PKDB00046',
     'PKDB00047',
     'PKDB00048',
     'PKDB00049',
     'PKDB00050',
     'PKDB00051',
     'PKDB00052',
     'PKDB00053',
     'PKDB00054',
     'PKDB00055',
     'PKDB00056',
     'PKDB00057',
     'PKDB00058',
     'PKDB00059',
     'PKDB00060',
     'PKDB00061',
     'PKDB00062',
     'PKDB00063',
     'PKDB00065',
     'PKDB00126',
     'PKDB00127',
     'PKDB00128',
     'PKDB00129',
     'PKDB00136',
     'PKDB00137',
     'PKDB00138',
     'PKDB00210',
     'PKDB00328',
     'PKDB00338',
     'PKDB00339',
     'PKDB00341',
     'PKDB00378',
     'PKDB00380',
     'PKDB00381',
     'PKDB00382',
     'PKDB00383',
     'Sandberg1988',
     'Scott1989',
     'Tanaka1993',
     'Trang1985'}



Filtering a subset of data works by providing filter/selection functions
which select a subset of the data. The filters are written on the
``groups``, ``individuals``

.. code:: ipython3

    def is_PKDB99999(d):
        """Filter for specific study_sid. """
        return d.study_sid == "PKDB99999"
    
    data = test_data.filter_intervention(is_PKDB99999)
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (139891787702672)
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

    {'Lennard1982', '25853045', 'PKDB00002', '25891161', '6712142', 'PKDB00045', 'Trang1985', 'PKDB00210', 'PKDB00012', '1033273', '4027137', 'PKDB00126', '7371463', '15022032', 'Sandberg1988', '3557314', 'Nakazawa1988', '2921843', '2185297', '28929443', 'PKDB00015', '26862045'}


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

    data = test_data.filter_intervention(lambda d: d.study_sid == "PKDB99999")
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (139891787682832)
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
    PKData (139890839716880)
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
    PKData (139890839717712)
    ------------------------------
    studies           127  (  127)
    groups            429  ( 3733)
    individuals      3163  (28219)
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
    PKData (139890849157456)
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
    PKData (139890842843216)
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
    PKData (139890842843920)
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
    PKData (139890839534800)
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
    PKData (139890849160720)
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

3.2 Get outputs/timecourses where multiple interventions were given
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)

.. code:: ipython3

    caffeine_data = test_data.filter_intervention(dosing_and_caffeine)

.. code:: ipython3

    print(caffeine_data)


.. parsed-literal::

    ------------------------------
    PKData (139890848739472)
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
    PKData (139890841988752)
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
    PKData (139890848654736)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    scatters           80  (   80)
    ------------------------------


6 Pitfalls
----------

.. code:: ipython3

    test_data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)
    # Wrong 
    def is_healthy_smoker(d): 
        """ This will yield zero subjects. No characteristica satisfy measurement_type == 'healthy' and measurement_type == 'disease'. 
        """
        return ((d["measurement_type"]=="healthy") & (d["choice"]=="Y")) & ((d["measurement_type"]=="smoking") & (d["choice"]=="Y"))
             
    # Correct 
    def is_healthy_smoker(d): 
        """ """
        return [(d["measurement_type"]=="healthy") & (d["choice"]=="Y"), (d["measurement_type"]=="smoking") & (d["choice"]=="Y")]
    
       
    # Wrong 
    def not_smoker_y(d):
        """ Be care this might not do what you expect. Excluding a specific characteristica will not eliminate any subject unless it is the only characteristica.
        """
        return ~((d["measurement_type"]=="smoking") & (d["choice"]=="Y")) 
    not_smoker_y_data = test_data.filter_subject(not_smoker_y)
    
    #Correct
    # exlcude smoker
    def smoker_y(d):
        return (d["measurement_type"]=="smoking") & (d["choice"]=="Y")
    healthy_data = test_data.exclude_subject(smoker_y)
    
    
    # Wrong 
    def not_disease(d):
        """ Be care this might not do what you expect. Excluding a specific characteristica will not eliminate any subject unless it is the only characteristica
        """
        return  ~(d["measurement_type"]=="disease")
    healthy_data = test_data.filter_subject(not_disease)
    
    # Correct 
    # exlcude the disease
    def disease(d):
        return  d["measurement_type"]=="disease"
    healthy_data = test_data.exclude_subject(disease)


