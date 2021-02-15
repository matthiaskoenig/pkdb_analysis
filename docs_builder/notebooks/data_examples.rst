.. code:: ipython3

    
    import pandas as pd
    from IPython.display import display
    


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
    from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP
    
    data = PKData.from_archive(TESTDATA_CONCISE_FALSE_ZIP)
    print(data)
    data._concise()
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (139739272011664)
    ------------------------------
    studies           127  (  127)
    groups            429  ( 3733)
    individuals      3163  (28219)
    interventions     409  (  409)
    outputs         19407  (29053)
    timecourses       722  (  722)
    scatters           80  (   80)
    ------------------------------
    ------------------------------
    PKData (139739272011664)
    ------------------------------
    studies           124  (  124)
    groups            284  ( 2613)
    individuals      3082  (27405)
    interventions     366  (  366)
    outputs         19407  (29053)
    timecourses       722  (  722)
    scatters           80  (   80)
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
``timecourses``: timecourses, uniquely identified via ``subset_pk`` -
``scatters``: scatters, uniquely identified via ``subset_pk``

The ``print`` function provides a simple overview over the content

.. code:: ipython3

    print(data)


.. parsed-literal::

    ------------------------------
    PKData (139739272011664)
    ------------------------------
    studies           124  (  124)
    groups            284  ( 2613)
    individuals      3082  (27405)
    interventions     366  (  366)
    outputs         19407  (29053)
    timecourses       722  (  722)
    scatters           80  (   80)
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
          <th>...</th>
          <th>unit</th>
          <th>se</th>
          <th>min</th>
          <th>cv</th>
          <th>median</th>
          <th>group_pk</th>
          <th>characteristica_pk</th>
          <th>mean</th>
          <th>choice</th>
          <th>value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>6</th>
          <td>6</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>ethnicity</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>8</td>
          <td>3462</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3463</td>
          <td>67393</td>
          <td>NaN</td>
          <td>caucasian</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>7</th>
          <td>7</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>ethnicity</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>3462</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3463</td>
          <td>67394</td>
          <td>NaN</td>
          <td>african</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>8</th>
          <td>8</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>weight</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>9</td>
          <td>3462</td>
          <td>...</td>
          <td>kilogram</td>
          <td>2.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3463</td>
          <td>67395</td>
          <td>59.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>9</th>
          <td>9</td>
          <td>Abernethy1985</td>
          <td>PKDB00001</td>
          <td>oral contraceptives</td>
          <td>9</td>
          <td>OCS</td>
          <td>NaN</td>
          <td>nan</td>
          <td>9</td>
          <td>3462</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3463</td>
          <td>67396</td>
          <td>NaN</td>
          <td>Y</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>10</th>
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
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3463</td>
          <td>67383</td>
          <td>NaN</td>
          <td>N</td>
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
          <th>3718</th>
          <td>3718</td>
          <td>Scott1989</td>
          <td>Scott1989</td>
          <td>sex</td>
          <td>9</td>
          <td>Decomp</td>
          <td>NaN</td>
          <td>nan</td>
          <td>8</td>
          <td>3954</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3957</td>
          <td>79908</td>
          <td>NaN</td>
          <td>M</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3719</th>
          <td>3719</td>
          <td>Scott1989</td>
          <td>Scott1989</td>
          <td>sex</td>
          <td>9</td>
          <td>Decomp</td>
          <td>NaN</td>
          <td>nan</td>
          <td>11</td>
          <td>3954</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3957</td>
          <td>79909</td>
          <td>NaN</td>
          <td>F</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3720</th>
          <td>3720</td>
          <td>Scott1989</td>
          <td>Scott1989</td>
          <td>medication</td>
          <td>9</td>
          <td>Decomp</td>
          <td>NaN</td>
          <td>nan</td>
          <td>19</td>
          <td>3954</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3957</td>
          <td>79910</td>
          <td>NaN</td>
          <td>Y</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3721</th>
          <td>3721</td>
          <td>Scott1989</td>
          <td>Scott1989</td>
          <td>disease</td>
          <td>9</td>
          <td>Decomp</td>
          <td>NaN</td>
          <td>nan</td>
          <td>19</td>
          <td>3954</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3957</td>
          <td>79912</td>
          <td>NaN</td>
          <td>liver cirrhosis</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3722</th>
          <td>3722</td>
          <td>Scott1989</td>
          <td>Scott1989</td>
          <td>species</td>
          <td>9</td>
          <td>Decomp</td>
          <td>NaN</td>
          <td>nan</td>
          <td>29</td>
          <td>3954</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3957</td>
          <td>79898</td>
          <td>NaN</td>
          <td>homo sapiens</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>2613 rows × 21 columns</p>
    </div>




.. parsed-literal::

          Unnamed: 0     study_name  study_sid     measurement_type  group_count  \
    6              6  Abernethy1985  PKDB00001            ethnicity            9   
    7              7  Abernethy1985  PKDB00001            ethnicity            9   
    8              8  Abernethy1985  PKDB00001               weight            9   
    9              9  Abernethy1985  PKDB00001  oral contraceptives            9   
    10            10  Abernethy1985  PKDB00001              smoking            9   
    ...          ...            ...        ...                  ...          ...   
    3718        3718      Scott1989  Scott1989                  sex            9   
    3719        3719      Scott1989  Scott1989                  sex            9   
    3720        3720      Scott1989  Scott1989           medication            9   
    3721        3721      Scott1989  Scott1989              disease            9   
    3722        3722      Scott1989  Scott1989              species            9   
    
         group_name  max substance  count  group_parent_pk  ...      unit   se  \
    6           OCS  NaN       nan      8             3462  ...       NaN  NaN   
    7           OCS  NaN       nan      1             3462  ...       NaN  NaN   
    8           OCS  NaN       nan      9             3462  ...  kilogram  2.0   
    9           OCS  NaN       nan      9             3462  ...       NaN  NaN   
    10          OCS  NaN       nan     18             3462  ...       NaN  NaN   
    ...         ...  ...       ...    ...              ...  ...       ...  ...   
    3718     Decomp  NaN       nan      8             3954  ...       NaN  NaN   
    3719     Decomp  NaN       nan     11             3954  ...       NaN  NaN   
    3720     Decomp  NaN       nan     19             3954  ...       NaN  NaN   
    3721     Decomp  NaN       nan     19             3954  ...       NaN  NaN   
    3722     Decomp  NaN       nan     29             3954  ...       NaN  NaN   
    
          min  cv  median  group_pk  characteristica_pk  mean           choice  \
    6     NaN NaN     NaN      3463               67393   NaN        caucasian   
    7     NaN NaN     NaN      3463               67394   NaN          african   
    8     NaN NaN     NaN      3463               67395  59.0              NaN   
    9     NaN NaN     NaN      3463               67396   NaN                Y   
    10    NaN NaN     NaN      3463               67383   NaN                N   
    ...   ...  ..     ...       ...                 ...   ...              ...   
    3718  NaN NaN     NaN      3957               79908   NaN                M   
    3719  NaN NaN     NaN      3957               79909   NaN                F   
    3720  NaN NaN     NaN      3957               79910   NaN                Y   
    3721  NaN NaN     NaN      3957               79912   NaN  liver cirrhosis   
    3722  NaN NaN     NaN      3957               79898   NaN     homo sapiens   
    
         value  
    6      NaN  
    7      NaN  
    8      NaN  
    9      NaN  
    10     NaN  
    ...    ...  
    3718   NaN  
    3719   NaN  
    3720   NaN  
    3721   NaN  
    3722   NaN  
    
    [2613 rows x 21 columns]



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
          <th rowspan="5" valign="top">2799</th>
          <th>56053</th>
          <td>3281</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>species</td>
          <td>12</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>-1</td>
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
          <th>56054</th>
          <td>3282</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>fasting</td>
          <td>12</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>-1</td>
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
          <th>56055</th>
          <td>3283</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>sex</td>
          <td>12</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>-1</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>M</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>56056</th>
          <td>3284</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>healthy</td>
          <td>12</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>-1</td>
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
          <th>56057</th>
          <td>3285</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>age</td>
          <td>12</td>
          <td>all</td>
          <td>34.0</td>
          <td>nan</td>
          <td>12</td>
          <td>-1</td>
          <td>NaN</td>
          <td>year</td>
          <td>NaN</td>
          <td>21.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>27.0</td>
          <td>NaN</td>
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
    <p>2613 rows × 19 columns</p>
    </div>




.. parsed-literal::

                                 Unnamed: 0    study_name     study_sid  \
    group_pk characteristica_pk                                           
    2799     56053                     3281  Sandberg1988  Sandberg1988   
             56054                     3282  Sandberg1988  Sandberg1988   
             56055                     3283  Sandberg1988  Sandberg1988   
             56056                     3284  Sandberg1988  Sandberg1988   
             56057                     3285  Sandberg1988  Sandberg1988   
    ...                                 ...           ...           ...   
    4001     80932                     3677      Tian2019      30387917   
             80933                     3678      Tian2019      30387917   
             80934                     3681      Tian2019      30387917   
             80935                     3682      Tian2019      30387917   
             80936                     3683      Tian2019      30387917   
    
                                measurement_type  group_count group_name   max  \
    group_pk characteristica_pk                                                  
    2799     56053                       species           12        all   NaN   
             56054                       fasting           12        all   NaN   
             56055                           sex           12        all   NaN   
             56056                       healthy           12        all   NaN   
             56057                           age           12        all  34.0   
    ...                                      ...          ...        ...   ...   
    4001     80932               CYP1A2 genotype           12        men   NaN   
             80933               CYP1A2 genotype           12        men   NaN   
             80934               CYP1A2 genotype           12        men   NaN   
             80935               CYP1A2 genotype           12        men   NaN   
             80936               CYP1A2 genotype           12        men   NaN   
    
                                substance  count  group_parent_pk  sd  unit  se  \
    group_pk characteristica_pk                                                   
    2799     56053                    nan     12               -1 NaN   NaN NaN   
             56054                    nan     12               -1 NaN   NaN NaN   
             56055                    nan     12               -1 NaN   NaN NaN   
             56056                    nan     12               -1 NaN   NaN NaN   
             56057                    nan     12               -1 NaN  year NaN   
    ...                               ...    ...              ...  ..   ...  ..   
    4001     80932                    nan      1             3999 NaN   NaN NaN   
             80933                    nan      1             3999 NaN   NaN NaN   
             80934                    nan      2             3999 NaN   NaN NaN   
             80935                    nan      6             3999 NaN   NaN NaN   
             80936                    nan      2             3999 NaN   NaN NaN   
    
                                  min  cv  median  mean         choice  value  
    group_pk characteristica_pk                                                
    2799     56053                NaN NaN     NaN   NaN   homo sapiens    NaN  
             56054                NaN NaN     NaN   NaN              Y    NaN  
             56055                NaN NaN     NaN   NaN              M    NaN  
             56056                NaN NaN     NaN   NaN              Y    NaN  
             56057               21.0 NaN     NaN  27.0            NaN    NaN  
    ...                           ...  ..     ...   ...            ...    ...  
    4001     80932                NaN NaN     NaN   NaN        *1a/*1a    NaN  
             80933                NaN NaN     NaN   NaN        *1c/*1f    NaN  
             80934                NaN NaN     NaN   NaN  *1c*1f/*1c*1f    NaN  
             80935                NaN NaN     NaN   NaN        *1a/*1f    NaN  
             80936                NaN NaN     NaN   NaN        *1f/*1f    NaN  
    
    [2613 rows x 19 columns]



To access the number of items use the ``*_count``.

.. code:: ipython3

    print(f"Number of groups: {data.groups_count}")


.. parsed-literal::

    Number of groups: 284


The ``groups``, ``individuals``, ``interventions``, ``outputs`` and
``timecourses`` are ``pandas.DataFrame`` instances, so all the classical
pandas operations can be applied on the data. For instance to access a
single ``group`` use logical indexing by the ``group_pk`` field. E.g. to
get the group ``20`` use

.. code:: ipython3

    data.groups[data.groups.group_pk==312]


.. parsed-literal::

    INFO NumExpr defaulting to 8 threads.



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
          <th>study_sid</th>
          <th>measurement_type</th>
          <th>group_count</th>
          <th>group_name</th>
          <th>max</th>
          <th>substance</th>
          <th>count</th>
          <th>group_parent_pk</th>
          <th>...</th>
          <th>unit</th>
          <th>se</th>
          <th>min</th>
          <th>cv</th>
          <th>median</th>
          <th>group_pk</th>
          <th>characteristica_pk</th>
          <th>mean</th>
          <th>choice</th>
          <th>value</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    <p>0 rows × 21 columns</p>
    </div>




.. parsed-literal::

    Empty DataFrame
    Columns: [Unnamed: 0, study_name, study_sid, measurement_type, group_count, group_name, max, substance, count, group_parent_pk, sd, unit, se, min, cv, median, group_pk, characteristica_pk, mean, choice, value]
    Index: []
    
    [0 rows x 21 columns]



In the group tables multiple rows exist which belong to a single group!
This is important to understand filtering of the data later on. For
instance in this example the information on ``species``, ``healthy``,
``smoking``, ``age`` and ``overnight_fast`` are all separate rows in the
``groups`` table, but belong to a single row.

When looking at the multi-index table this becomes more clear. We now
get the group 20 form the ``groups_mi``. We can simply use the ``.loc``
to lookup the group by ``pk``

.. code:: ipython3

    data.groups_mi.loc[312]


::


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexes/base.py in get_loc(self, key, method, tolerance)
       2894             try:
    -> 2895                 return self._engine.get_loc(casted_key)
       2896             except KeyError as err:


    pandas/_libs/index.pyx in pandas._libs.index.IndexEngine.get_loc()


    pandas/_libs/index.pyx in pandas._libs.index.IndexEngine.get_loc()


    pandas/_libs/hashtable_class_helper.pxi in pandas._libs.hashtable.Int64HashTable.get_item()


    pandas/_libs/hashtable_class_helper.pxi in pandas._libs.hashtable.Int64HashTable.get_item()


    KeyError: 312

    
    The above exception was the direct cause of the following exception:


    KeyError                                  Traceback (most recent call last)

    <ipython-input-1-dfe7f445dbe5> in <module>
    ----> 1 data.groups_mi.loc[312]
    

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexing.py in __getitem__(self, key)
        877 
        878             maybe_callable = com.apply_if_callable(key, self.obj)
    --> 879             return self._getitem_axis(maybe_callable, axis=axis)
        880 
        881     def _is_scalar_access(self, key: Tuple):


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexing.py in _getitem_axis(self, key, axis)
       1108         # fall thru to straight lookup
       1109         self._validate_key(key, axis)
    -> 1110         return self._get_label(key, axis=axis)
       1111 
       1112     def _get_slice_axis(self, slice_obj: slice, axis: int):


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexing.py in _get_label(self, label, axis)
       1057     def _get_label(self, label, axis: int):
       1058         # GH#5667 this will fail if the label is not present in the axis.
    -> 1059         return self.obj.xs(label, axis=axis)
       1060 
       1061     def _handle_lowerdim_multi_index_axis0(self, tup: Tuple):


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/generic.py in xs(self, key, axis, level, drop_level)
       3487         index = self.index
       3488         if isinstance(index, MultiIndex):
    -> 3489             loc, new_index = self.index.get_loc_level(key, drop_level=drop_level)
       3490         else:
       3491             loc = self.index.get_loc(key)


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexes/multi.py in get_loc_level(self, key, level, drop_level)
       2880                 return indexer, maybe_mi_droplevels(indexer, ilevels, drop_level)
       2881         else:
    -> 2882             indexer = self._get_level_indexer(key, level=level)
       2883             return indexer, maybe_mi_droplevels(indexer, [level], drop_level)
       2884 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexes/multi.py in _get_level_indexer(self, key, level, indexer)
       2964         else:
       2965 
    -> 2966             code = self._get_loc_single_level_index(level_index, key)
       2967 
       2968             if level > 0 or self.lexsort_depth == 0:


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexes/multi.py in _get_loc_single_level_index(self, level_index, key)
       2632             return -1
       2633         else:
    -> 2634             return level_index.get_loc(key)
       2635 
       2636     def get_loc(self, key, method=None):


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/pandas/core/indexes/base.py in get_loc(self, key, method, tolerance)
       2895                 return self._engine.get_loc(casted_key)
       2896             except KeyError as err:
    -> 2897                 raise KeyError(key) from err
       2898 
       2899         if tolerance is not None:


    KeyError: 312


In a similar manner we can explore the other information,
i.e. ``individuals``, ``interventions``, ``outputs`` and
``timecourses``.

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
          <th></th>
          <th>Unnamed: 0</th>
          <th>study_name</th>
          <th>study_sid</th>
          <th>measurement_type</th>
          <th>max</th>
          <th>substance</th>
          <th>count</th>
          <th>individual_group_pk</th>
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
          <th>individual_pk</th>
          <th>individual_name</th>
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
          <th rowspan="5" valign="top">19513</th>
          <th rowspan="5" valign="top">CR_1</th>
          <th>56053</th>
          <td>17793</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>species</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>2799</td>
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
          <th>56054</th>
          <td>17794</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>fasting</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>2799</td>
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
          <th>56055</th>
          <td>17795</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>sex</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>2799</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>M</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>56056</th>
          <td>17796</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>healthy</td>
          <td>NaN</td>
          <td>nan</td>
          <td>12</td>
          <td>2799</td>
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
          <th>56057</th>
          <td>17797</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>age</td>
          <td>34.0</td>
          <td>nan</td>
          <td>12</td>
          <td>2799</td>
          <td>NaN</td>
          <td>year</td>
          <td>NaN</td>
          <td>21.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>27.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
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
        </tr>
        <tr>
          <th rowspan="5" valign="top">30567</th>
          <th rowspan="5" valign="top">5</th>
          <th>84820</th>
          <td>28204</td>
          <td>Barnett1990</td>
          <td>PKDB00007</td>
          <td>abstinence</td>
          <td>NaN</td>
          <td>caffeine</td>
          <td>6</td>
          <td>4062</td>
          <td>NaN</td>
          <td>day</td>
          <td>NaN</td>
          <td>2.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>84821</th>
          <td>28205</td>
          <td>Barnett1990</td>
          <td>PKDB00007</td>
          <td>abstinence</td>
          <td>NaN</td>
          <td>methylxanthine</td>
          <td>6</td>
          <td>4062</td>
          <td>NaN</td>
          <td>day</td>
          <td>NaN</td>
          <td>2.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>84822</th>
          <td>28206</td>
          <td>Barnett1990</td>
          <td>PKDB00007</td>
          <td>abstinence alcohol</td>
          <td>NaN</td>
          <td>nan</td>
          <td>6</td>
          <td>4062</td>
          <td>NaN</td>
          <td>day</td>
          <td>NaN</td>
          <td>2.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>84841</th>
          <td>28195</td>
          <td>Barnett1990</td>
          <td>PKDB00007</td>
          <td>age</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>4062</td>
          <td>NaN</td>
          <td>year</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>21.0</td>
        </tr>
        <tr>
          <th>84842</th>
          <td>28196</td>
          <td>Barnett1990</td>
          <td>PKDB00007</td>
          <td>weight</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>4062</td>
          <td>NaN</td>
          <td>kilogram</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>60.5</td>
        </tr>
      </tbody>
    </table>
    <p>27405 rows × 17 columns</p>
    </div>




.. parsed-literal::

                                                      Unnamed: 0    study_name  \
    individual_pk individual_name characteristica_pk                             
    19513         CR_1            56053                    17793  Sandberg1988   
                                  56054                    17794  Sandberg1988   
                                  56055                    17795  Sandberg1988   
                                  56056                    17796  Sandberg1988   
                                  56057                    17797  Sandberg1988   
    ...                                                      ...           ...   
    30567         5               84820                    28204   Barnett1990   
                                  84821                    28205   Barnett1990   
                                  84822                    28206   Barnett1990   
                                  84841                    28195   Barnett1990   
                                  84842                    28196   Barnett1990   
    
                                                         study_sid  \
    individual_pk individual_name characteristica_pk                 
    19513         CR_1            56053               Sandberg1988   
                                  56054               Sandberg1988   
                                  56055               Sandberg1988   
                                  56056               Sandberg1988   
                                  56057               Sandberg1988   
    ...                                                        ...   
    30567         5               84820                  PKDB00007   
                                  84821                  PKDB00007   
                                  84822                  PKDB00007   
                                  84841                  PKDB00007   
                                  84842                  PKDB00007   
    
                                                        measurement_type   max  \
    individual_pk individual_name characteristica_pk                             
    19513         CR_1            56053                          species   NaN   
                                  56054                          fasting   NaN   
                                  56055                              sex   NaN   
                                  56056                          healthy   NaN   
                                  56057                              age  34.0   
    ...                                                              ...   ...   
    30567         5               84820                       abstinence   NaN   
                                  84821                       abstinence   NaN   
                                  84822               abstinence alcohol   NaN   
                                  84841                              age   NaN   
                                  84842                           weight   NaN   
    
                                                           substance  count  \
    individual_pk individual_name characteristica_pk                          
    19513         CR_1            56053                          nan     12   
                                  56054                          nan     12   
                                  56055                          nan     12   
                                  56056                          nan     12   
                                  56057                          nan     12   
    ...                                                          ...    ...   
    30567         5               84820                     caffeine      6   
                                  84821               methylxanthine      6   
                                  84822                          nan      6   
                                  84841                          nan      1   
                                  84842                          nan      1   
    
                                                      individual_group_pk  sd  \
    individual_pk individual_name characteristica_pk                            
    19513         CR_1            56053                              2799 NaN   
                                  56054                              2799 NaN   
                                  56055                              2799 NaN   
                                  56056                              2799 NaN   
                                  56057                              2799 NaN   
    ...                                                               ...  ..   
    30567         5               84820                              4062 NaN   
                                  84821                              4062 NaN   
                                  84822                              4062 NaN   
                                  84841                              4062 NaN   
                                  84842                              4062 NaN   
    
                                                          unit  se   min  cv  \
    individual_pk individual_name characteristica_pk                           
    19513         CR_1            56053                    NaN NaN   NaN NaN   
                                  56054                    NaN NaN   NaN NaN   
                                  56055                    NaN NaN   NaN NaN   
                                  56056                    NaN NaN   NaN NaN   
                                  56057                   year NaN  21.0 NaN   
    ...                                                    ...  ..   ...  ..   
    30567         5               84820                    day NaN   2.0 NaN   
                                  84821                    day NaN   2.0 NaN   
                                  84822                    day NaN   2.0 NaN   
                                  84841                   year NaN   NaN NaN   
                                  84842               kilogram NaN   NaN NaN   
    
                                                      median  mean        choice  \
    individual_pk individual_name characteristica_pk                               
    19513         CR_1            56053                  NaN   NaN  homo sapiens   
                                  56054                  NaN   NaN             Y   
                                  56055                  NaN   NaN             M   
                                  56056                  NaN   NaN             Y   
                                  56057                  NaN  27.0           NaN   
    ...                                                  ...   ...           ...   
    30567         5               84820                  NaN   NaN           NaN   
                                  84821                  NaN   NaN           NaN   
                                  84822                  NaN   NaN           NaN   
                                  84841                  NaN   NaN           NaN   
                                  84842                  NaN   NaN           NaN   
    
                                                      value  
    individual_pk individual_name characteristica_pk         
    19513         CR_1            56053                 NaN  
                                  56054                 NaN  
                                  56055                 NaN  
                                  56056                 NaN  
                                  56057                 NaN  
    ...                                                 ...  
    30567         5               84820                 NaN  
                                  84821                 NaN  
                                  84822                 NaN  
                                  84841                21.0  
                                  84842                60.5  
    
    [27405 rows x 17 columns]



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
          <th>Unnamed: 0</th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>raw_pk</th>
          <th>normed</th>
          <th>name</th>
          <th>route</th>
          <th>route_label</th>
          <th>form</th>
          <th>form_label</th>
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
          <th>4443</th>
          <td>356</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>4423</td>
          <td>True</td>
          <td>METO_CR_1</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>tablet</td>
          <td>tablet</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>0.1</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>4444</th>
          <td>357</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>4424</td>
          <td>True</td>
          <td>METO_CR_2</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>tablet</td>
          <td>tablet</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>0.1</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>4445</th>
          <td>358</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>4425</td>
          <td>True</td>
          <td>METO_CR_3</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>tablet</td>
          <td>tablet</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>0.1</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>4446</th>
          <td>359</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>4426</td>
          <td>True</td>
          <td>METO_CR_4</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>tablet</td>
          <td>tablet</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>0.1</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>4447</th>
          <td>360</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>4427</td>
          <td>True</td>
          <td>METO_CR_5</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>tablet</td>
          <td>tablet</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>0.1</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
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
          <th>6371</th>
          <td>389</td>
          <td>3557314</td>
          <td>Jost1987</td>
          <td>6367</td>
          <td>True</td>
          <td>icg</td>
          <td>iv</td>
          <td>intravenous (iv)</td>
          <td>solution</td>
          <td>solution</td>
          <td>...</td>
          <td>indocyanine green</td>
          <td>0.0005</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram / kilogram</td>
        </tr>
        <tr>
          <th>6372</th>
          <td>390</td>
          <td>3557314</td>
          <td>Jost1987</td>
          <td>6368</td>
          <td>True</td>
          <td>gala</td>
          <td>iv</td>
          <td>intravenous (iv)</td>
          <td>solution</td>
          <td>solution</td>
          <td>...</td>
          <td>galactose</td>
          <td>0.0005</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram / kilogram</td>
        </tr>
        <tr>
          <th>6473</th>
          <td>406</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>6472</td>
          <td>True</td>
          <td>Dcaf</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>nr-form</td>
          <td>Not reported (administration form)</td>
          <td>...</td>
          <td>caffeine (137X)</td>
          <td>0.35</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>6475</th>
          <td>407</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>6474</td>
          <td>True</td>
          <td>Dppa</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>pipemidic acid</td>
          <td>0.8</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>6477</th>
          <td>408</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>6476</td>
          <td>True</td>
          <td>Dnfc</td>
          <td>oral</td>
          <td>oral (po)</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>norfloxacin</td>
          <td>0.8</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>gram</td>
        </tr>
      </tbody>
    </table>
    <p>366 rows × 30 columns</p>
    </div>




.. parsed-literal::

                     Unnamed: 0     study_sid    study_name  raw_pk  normed  \
    intervention_pk                                                           
    4443                    356  Sandberg1988  Sandberg1988    4423    True   
    4444                    357  Sandberg1988  Sandberg1988    4424    True   
    4445                    358  Sandberg1988  Sandberg1988    4425    True   
    4446                    359  Sandberg1988  Sandberg1988    4426    True   
    4447                    360  Sandberg1988  Sandberg1988    4427    True   
    ...                     ...           ...           ...     ...     ...   
    6371                    389       3557314      Jost1987    6367    True   
    6372                    390       3557314      Jost1987    6368    True   
    6473                    406     PKDB00007   Barnett1990    6472    True   
    6475                    407     PKDB00007   Barnett1990    6474    True   
    6477                    408     PKDB00007   Barnett1990    6476    True   
    
                          name route       route_label      form  \
    intervention_pk                                                
    4443             METO_CR_1  oral         oral (po)    tablet   
    4444             METO_CR_2  oral         oral (po)    tablet   
    4445             METO_CR_3  oral         oral (po)    tablet   
    4446             METO_CR_4  oral         oral (po)    tablet   
    4447             METO_CR_5  oral         oral (po)    tablet   
    ...                    ...   ...               ...       ...   
    6371                   icg    iv  intravenous (iv)  solution   
    6372                  gala    iv  intravenous (iv)  solution   
    6473                  Dcaf  oral         oral (po)   nr-form   
    6475                  Dppa  oral         oral (po)      None   
    6477                  Dnfc  oral         oral (po)      None   
    
                                             form_label  ...    substance_label  \
    intervention_pk                                      ...                      
    4443                                         tablet  ...         metoprolol   
    4444                                         tablet  ...         metoprolol   
    4445                                         tablet  ...         metoprolol   
    4446                                         tablet  ...         metoprolol   
    4447                                         tablet  ...         metoprolol   
    ...                                             ...  ...                ...   
    6371                                       solution  ...  indocyanine green   
    6372                                       solution  ...          galactose   
    6473             Not reported (administration form)  ...    caffeine (137X)   
    6475                                           None  ...     pipemidic acid   
    6477                                           None  ...        norfloxacin   
    
                      value  mean median   min   max    sd    se    cv  \
    intervention_pk                                                      
    4443                0.1  None   None  None  None  None  None  None   
    4444                0.1  None   None  None  None  None  None  None   
    4445                0.1  None   None  None  None  None  None  None   
    4446                0.1  None   None  None  None  None  None  None   
    4447                0.1  None   None  None  None  None  None  None   
    ...                 ...   ...    ...   ...   ...   ...   ...   ...   
    6371             0.0005  None   None  None  None  None  None  None   
    6372             0.0005  None   None  None  None  None  None  None   
    6473               0.35  None   None  None  None  None  None  None   
    6475                0.8  None   None  None  None  None  None  None   
    6477                0.8  None   None  None  None  None  None  None   
    
                                unit  
    intervention_pk                   
    4443                        gram  
    4444                        gram  
    4445                        gram  
    4446                        gram  
    4447                        gram  
    ...                          ...  
    6371             gram / kilogram  
    6372             gram / kilogram  
    6473                        gram  
    6475                        gram  
    6477                        gram  
    
    [366 rows x 30 columns]



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
          <th>Unnamed: 0</th>
          <th>study_name</th>
          <th>measurement_type</th>
          <th>tissue</th>
          <th>sd</th>
          <th>se</th>
          <th>min</th>
          <th>time_unit</th>
          <th>normed</th>
          <th>calculated</th>
          <th>...</th>
          <th>method</th>
          <th>max</th>
          <th>substance</th>
          <th>label</th>
          <th>unit</th>
          <th>cv</th>
          <th>median</th>
          <th>mean</th>
          <th>time</th>
          <th>choice</th>
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
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">166965</th>
          <th>4443</th>
          <th>2799</th>
          <th>-1</th>
          <td>24391</td>
          <td>Sandberg1988</td>
          <td>concentration</td>
          <td>plasma</td>
          <td>0.000015</td>
          <td>0.000004</td>
          <td>NaN</td>
          <td>hr</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>metoprolol</td>
          <td>Fig2_CR</td>
          <td>gram / liter</td>
          <td>0.68543</td>
          <td>NaN</td>
          <td>0.000022</td>
          <td>96.0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4444</th>
          <th>2799</th>
          <th>-1</th>
          <td>24443</td>
          <td>Sandberg1988</td>
          <td>concentration</td>
          <td>plasma</td>
          <td>0.000015</td>
          <td>0.000004</td>
          <td>NaN</td>
          <td>hr</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>metoprolol</td>
          <td>Fig2_CR</td>
          <td>gram / liter</td>
          <td>0.68543</td>
          <td>NaN</td>
          <td>0.000022</td>
          <td>96.0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4445</th>
          <th>2799</th>
          <th>-1</th>
          <td>24080</td>
          <td>Sandberg1988</td>
          <td>concentration</td>
          <td>plasma</td>
          <td>0.000015</td>
          <td>0.000004</td>
          <td>NaN</td>
          <td>hr</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>metoprolol</td>
          <td>Fig2_CR</td>
          <td>gram / liter</td>
          <td>0.68543</td>
          <td>NaN</td>
          <td>0.000022</td>
          <td>96.0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4446</th>
          <th>2799</th>
          <th>-1</th>
          <td>24440</td>
          <td>Sandberg1988</td>
          <td>concentration</td>
          <td>plasma</td>
          <td>0.000015</td>
          <td>0.000004</td>
          <td>NaN</td>
          <td>hr</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>metoprolol</td>
          <td>Fig2_CR</td>
          <td>gram / liter</td>
          <td>0.68543</td>
          <td>NaN</td>
          <td>0.000022</td>
          <td>96.0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4447</th>
          <th>2799</th>
          <th>-1</th>
          <td>24322</td>
          <td>Sandberg1988</td>
          <td>concentration</td>
          <td>plasma</td>
          <td>0.000015</td>
          <td>0.000004</td>
          <td>NaN</td>
          <td>hr</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>metoprolol</td>
          <td>Fig2_CR</td>
          <td>gram / liter</td>
          <td>0.68543</td>
          <td>NaN</td>
          <td>0.000022</td>
          <td>96.0</td>
          <td>NaN</td>
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
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>263162</th>
          <th>6475</th>
          <th>-1</th>
          <th>30567</th>
          <td>28915</td>
          <td>Barnett1990</td>
          <td>tmax</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>hplc</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">263163</th>
          <th>6473</th>
          <th>-1</th>
          <th>30567</th>
          <td>28918</td>
          <td>Barnett1990</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>hplc</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6475</th>
          <th>-1</th>
          <th>30567</th>
          <td>29051</td>
          <td>Barnett1990</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>hplc</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">263164</th>
          <th>6473</th>
          <th>-1</th>
          <th>30567</th>
          <td>29052</td>
          <td>Barnett1990</td>
          <td>vd-ss</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>hplc</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6475</th>
          <th>-1</th>
          <th>30567</th>
          <td>28978</td>
          <td>Barnett1990</td>
          <td>vd-ss</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>hplc</td>
          <td>NaN</td>
          <td>caf</td>
          <td>NaN</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>29053 rows × 23 columns</p>
    </div>




.. parsed-literal::

                                                      Unnamed: 0    study_name  \
    output_pk intervention_pk group_pk individual_pk                             
    166965    4443             2799    -1                  24391  Sandberg1988   
              4444             2799    -1                  24443  Sandberg1988   
              4445             2799    -1                  24080  Sandberg1988   
              4446             2799    -1                  24440  Sandberg1988   
              4447             2799    -1                  24322  Sandberg1988   
    ...                                                      ...           ...   
    263162    6475            -1        30567              28915   Barnett1990   
    263163    6473            -1        30567              28918   Barnett1990   
              6475            -1        30567              29051   Barnett1990   
    263164    6473            -1        30567              29052   Barnett1990   
              6475            -1        30567              28978   Barnett1990   
    
                                                     measurement_type  tissue  \
    output_pk intervention_pk group_pk individual_pk                            
    166965    4443             2799    -1               concentration  plasma   
              4444             2799    -1               concentration  plasma   
              4445             2799    -1               concentration  plasma   
              4446             2799    -1               concentration  plasma   
              4447             2799    -1               concentration  plasma   
    ...                                                           ...     ...   
    263162    6475            -1        30567                    tmax  plasma   
    263163    6473            -1        30567                      vd  plasma   
              6475            -1        30567                      vd  plasma   
    263164    6473            -1        30567                   vd-ss  plasma   
              6475            -1        30567                   vd-ss  plasma   
    
                                                            sd        se  min  \
    output_pk intervention_pk group_pk individual_pk                            
    166965    4443             2799    -1             0.000015  0.000004  NaN   
              4444             2799    -1             0.000015  0.000004  NaN   
              4445             2799    -1             0.000015  0.000004  NaN   
              4446             2799    -1             0.000015  0.000004  NaN   
              4447             2799    -1             0.000015  0.000004  NaN   
    ...                                                    ...       ...  ...   
    263162    6475            -1        30567              NaN       NaN  NaN   
    263163    6473            -1        30567              NaN       NaN  NaN   
              6475            -1        30567              NaN       NaN  NaN   
    263164    6473            -1        30567              NaN       NaN  NaN   
              6475            -1        30567              NaN       NaN  NaN   
    
                                                     time_unit  normed  \
    output_pk intervention_pk group_pk individual_pk                     
    166965    4443             2799    -1                   hr    True   
              4444             2799    -1                   hr    True   
              4445             2799    -1                   hr    True   
              4446             2799    -1                   hr    True   
              4447             2799    -1                   hr    True   
    ...                                                    ...     ...   
    263162    6475            -1        30567              NaN    True   
    263163    6473            -1        30567              NaN    True   
              6475            -1        30567              NaN    True   
    263164    6473            -1        30567              NaN    True   
              6475            -1        30567              NaN    True   
    
                                                      calculated  ...  method max  \
    output_pk intervention_pk group_pk individual_pk              ...               
    166965    4443             2799    -1                  False  ...     NaN NaN   
              4444             2799    -1                  False  ...     NaN NaN   
              4445             2799    -1                  False  ...     NaN NaN   
              4446             2799    -1                  False  ...     NaN NaN   
              4447             2799    -1                  False  ...     NaN NaN   
    ...                                                      ...  ...     ...  ..   
    263162    6475            -1        30567               True  ...    hplc NaN   
    263163    6473            -1        30567               True  ...    hplc NaN   
              6475            -1        30567               True  ...    hplc NaN   
    263164    6473            -1        30567               True  ...    hplc NaN   
              6475            -1        30567               True  ...    hplc NaN   
    
                                                       substance    label  \
    output_pk intervention_pk group_pk individual_pk                        
    166965    4443             2799    -1             metoprolol  Fig2_CR   
              4444             2799    -1             metoprolol  Fig2_CR   
              4445             2799    -1             metoprolol  Fig2_CR   
              4446             2799    -1             metoprolol  Fig2_CR   
              4447             2799    -1             metoprolol  Fig2_CR   
    ...                                                      ...      ...   
    263162    6475            -1        30567                caf      NaN   
    263163    6473            -1        30567                caf      NaN   
              6475            -1        30567                caf      NaN   
    263164    6473            -1        30567                caf      NaN   
              6475            -1        30567                caf      NaN   
    
                                                              unit       cv  \
    output_pk intervention_pk group_pk individual_pk                          
    166965    4443             2799    -1             gram / liter  0.68543   
              4444             2799    -1             gram / liter  0.68543   
              4445             2799    -1             gram / liter  0.68543   
              4446             2799    -1             gram / liter  0.68543   
              4447             2799    -1             gram / liter  0.68543   
    ...                                                        ...      ...   
    263162    6475            -1        30567                 hour      NaN   
    263163    6473            -1        30567                liter      NaN   
              6475            -1        30567                liter      NaN   
    263164    6473            -1        30567                liter      NaN   
              6475            -1        30567                liter      NaN   
    
                                                     median      mean  time  \
    output_pk intervention_pk group_pk individual_pk                          
    166965    4443             2799    -1               NaN  0.000022  96.0   
              4444             2799    -1               NaN  0.000022  96.0   
              4445             2799    -1               NaN  0.000022  96.0   
              4446             2799    -1               NaN  0.000022  96.0   
              4447             2799    -1               NaN  0.000022  96.0   
    ...                                                 ...       ...   ...   
    263162    6475            -1        30567           NaN       NaN   NaN   
    263163    6473            -1        30567           NaN       NaN   NaN   
              6475            -1        30567           NaN       NaN   NaN   
    263164    6473            -1        30567           NaN       NaN   NaN   
              6475            -1        30567           NaN       NaN   NaN   
    
                                                      choice  
    output_pk intervention_pk group_pk individual_pk          
    166965    4443             2799    -1                NaN  
              4444             2799    -1                NaN  
              4445             2799    -1                NaN  
              4446             2799    -1                NaN  
              4447             2799    -1                NaN  
    ...                                                  ...  
    263162    6475            -1        30567            NaN  
    263163    6473            -1        30567            NaN  
              6475            -1        30567            NaN  
    263164    6473            -1        30567            NaN  
              6475            -1        30567            NaN  
    
    [29053 rows x 23 columns]



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
          <th>Unnamed: 0</th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>output_pk</th>
          <th>subset_name</th>
          <th>normed</th>
          <th>tissue</th>
          <th>tissue_label</th>
          <th>method</th>
          <th>method_label</th>
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
        <tr>
          <th>subset_pk</th>
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
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>3307</th>
          <th>(4448, 4449, 4450, 4451, 4452)</th>
          <th>2799</th>
          <th>-1</th>
          <td>592</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>(166979, 166980, 166981, 166982, 166983, 16698...</td>
          <td>Fig2_100</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>NaN</td>
          <td>(1.3223154736189403e-05, 5.053727096804881e-05...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>(1.030063798165528e-05, 3.935558314793124e-05,...</td>
          <td>(2.97353805576678e-06, 1.1360978262286402e-05,...</td>
          <td>[0.778984908454885, 0.7787437349518345, 0.2892...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>3308</th>
          <th>(4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460, 4461, 4462)</th>
          <th>2799</th>
          <th>-1</th>
          <td>552</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>(166993, 166994, 166995, 166996, 166997, 16699...</td>
          <td>Fig2_50</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>NaN</td>
          <td>(3.6470419909156005e-05, 8.83924221952528e-05,...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>(2.1727913322049826e-05, 2.9518215551111463e-0...</td>
          <td>(6.2723083027071615e-06, 8.521174847215801e-06...</td>
          <td>[0.5957681149866599, 0.3339450918757238, 0.320...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>3309</th>
          <th>(4443, 4444, 4445, 4446, 4447)</th>
          <th>2799</th>
          <th>-1</th>
          <td>625</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>(166965, 166966, 166967, 166968, 166969, 16697...</td>
          <td>Fig2_CR</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>metoprolol</td>
          <td>NaN</td>
          <td>(2.18782508441315e-05, 1.9968919659494645e-05,...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>(1.4996018928739371e-05, 1.4993540482147688e-0...</td>
          <td>(4.3289777826402e-06, 4.32826231673676e-06, 4....</td>
          <td>[0.6854304320567665, 0.7508438482308527, 0.554...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>3310</th>
          <th>(4448, 4449, 4450, 4451, 4452)</th>
          <th>2799</th>
          <th>-1</th>
          <td>528</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>(167011, 167012, 167013, 167014, 167015, 167016)</td>
          <td>Fig3_100</td>
          <td>True</td>
          <td>heart</td>
          <td>heart</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>(5.99242, 22.291657999999998, 17.3896269999999...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>(6.793094260620936, 4.414942082867226, 4.75367...</td>
          <td>(1.9609974, 1.274484, 1.372267, 2.009764, 2.01...</td>
          <td>[1.1336145097674957, 0.19805355361486465, 0.27...</td>
          <td>percent</td>
        </tr>
        <tr>
          <th>3311</th>
          <th>(4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460, 4461, 4462)</th>
          <th>2799</th>
          <th>-1</th>
          <td>582</td>
          <td>Sandberg1988</td>
          <td>Sandberg1988</td>
          <td>(167017, 167018, 167019, 167020, 167021, 167022)</td>
          <td>Fig3_50</td>
          <td>True</td>
          <td>heart</td>
          <td>heart</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>(10.060966, 19.742437, 14.791641, 9.828696, 8....</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>(7.98085849421614, 5.432896055288376, 5.263969...</td>
          <td>(2.3038754, 1.568342, 1.519577, 1.911979, 2.45...</td>
          <td>[0.7932497231594003, 0.2751887244360145, 0.355...</td>
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
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>5285</th>
          <th>(6473, 6477)</th>
          <th>-1</th>
          <th>30565</th>
          <td>719</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>(262971, 262972, 262973, 262974, 262975, 26297...</td>
          <td>3_Dcaf, Dnfc</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>caffeine (137X)</td>
          <td>(0.005779762, 0.007342083500000001, 0.00498195...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>5286</th>
          <th>(6473, 6475)</th>
          <th>-1</th>
          <th>30565</th>
          <td>651</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>(262981, 262982, 262983, 262984, 262985, 26298...</td>
          <td>3_Dcaf, Dppa</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>caffeine (137X)</td>
          <td>(0.007626138700000001, 0.0055641580000000005, ...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>5287</th>
          <th>(6473,)</th>
          <th>-1</th>
          <th>30567</th>
          <td>654</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>(262991, 262992, 262993, 262994, 262995, 26299...</td>
          <td>5_Dcaf</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>caffeine (137X)</td>
          <td>(0.006376934, 0.005785014599999999, 0.00397134...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>5288</th>
          <th>(6473, 6477)</th>
          <th>-1</th>
          <th>30567</th>
          <td>679</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>(263001, 263002, 263003, 263004, 263005, 26300...</td>
          <td>5_Dcaf, Dnfc</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>caffeine (137X)</td>
          <td>(0.008225058, 0.008221353, 0.00629417099999999...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>5289</th>
          <th>(6473, 6475)</th>
          <th>-1</th>
          <th>30567</th>
          <td>682</td>
          <td>PKDB00007</td>
          <td>Barnett1990</td>
          <td>(263011, 263012, 263013, 263014, 263015, 26301...</td>
          <td>5_Dcaf, Dppa</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>caffeine (137X)</td>
          <td>(0.007026457000000001, 0.006938287700000001, 0...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
        </tr>
      </tbody>
    </table>
    <p>722 rows × 28 columns</p>
    </div>




.. parsed-literal::

                                                                                         Unnamed: 0  \
    subset_pk intervention_pk                                    group_pk individual_pk               
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1                    592   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                    552   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1                    625   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1                    528   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                    582   
    ...                                                                                         ...   
    5285      (6473, 6477)                                       -1        30565                719   
    5286      (6473, 6475)                                       -1        30565                651   
    5287      (6473,)                                            -1        30567                654   
    5288      (6473, 6477)                                       -1        30567                679   
    5289      (6473, 6475)                                       -1        30567                682   
    
                                                                                            study_sid  \
    subset_pk intervention_pk                                    group_pk individual_pk                 
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             Sandberg1988   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             Sandberg1988   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             Sandberg1988   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             Sandberg1988   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             Sandberg1988   
    ...                                                                                           ...   
    5285      (6473, 6477)                                       -1        30565            PKDB00007   
    5286      (6473, 6475)                                       -1        30565            PKDB00007   
    5287      (6473,)                                            -1        30567            PKDB00007   
    5288      (6473, 6477)                                       -1        30567            PKDB00007   
    5289      (6473, 6475)                                       -1        30567            PKDB00007   
    
                                                                                           study_name  \
    subset_pk intervention_pk                                    group_pk individual_pk                 
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             Sandberg1988   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             Sandberg1988   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             Sandberg1988   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             Sandberg1988   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             Sandberg1988   
    ...                                                                                           ...   
    5285      (6473, 6477)                                       -1        30565          Barnett1990   
    5286      (6473, 6475)                                       -1        30565          Barnett1990   
    5287      (6473,)                                            -1        30567          Barnett1990   
    5288      (6473, 6477)                                       -1        30567          Barnett1990   
    5289      (6473, 6475)                                       -1        30567          Barnett1990   
    
                                                                                                                                 output_pk  \
    subset_pk intervention_pk                                    group_pk individual_pk                                                      
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             (166979, 166980, 166981, 166982, 166983, 16698...   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             (166993, 166994, 166995, 166996, 166997, 16699...   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             (166965, 166966, 166967, 166968, 166969, 16697...   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1              (167011, 167012, 167013, 167014, 167015, 167016)   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1              (167017, 167018, 167019, 167020, 167021, 167022)   
    ...                                                                                                                                ...   
    5285      (6473, 6477)                                       -1        30565         (262971, 262972, 262973, 262974, 262975, 26297...   
    5286      (6473, 6475)                                       -1        30565         (262981, 262982, 262983, 262984, 262985, 26298...   
    5287      (6473,)                                            -1        30567         (262991, 262992, 262993, 262994, 262995, 26299...   
    5288      (6473, 6477)                                       -1        30567         (263001, 263002, 263003, 263004, 263005, 26300...   
    5289      (6473, 6475)                                       -1        30567         (263011, 263012, 263013, 263014, 263015, 26301...   
    
                                                                                          subset_name  \
    subset_pk intervention_pk                                    group_pk individual_pk                 
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1                 Fig2_100   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                  Fig2_50   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1                  Fig2_CR   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1                 Fig3_100   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                  Fig3_50   
    ...                                                                                           ...   
    5285      (6473, 6477)                                       -1        30565         3_Dcaf, Dnfc   
    5286      (6473, 6475)                                       -1        30565         3_Dcaf, Dppa   
    5287      (6473,)                                            -1        30567               5_Dcaf   
    5288      (6473, 6477)                                       -1        30567         5_Dcaf, Dnfc   
    5289      (6473, 6475)                                       -1        30567         5_Dcaf, Dppa   
    
                                                                                         normed  \
    subset_pk intervention_pk                                    group_pk individual_pk           
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1               True   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1               True   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1               True   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1               True   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1               True   
    ...                                                                                     ...   
    5285      (6473, 6477)                                       -1        30565           True   
    5286      (6473, 6475)                                       -1        30565           True   
    5287      (6473,)                                            -1        30567           True   
    5288      (6473, 6477)                                       -1        30567           True   
    5289      (6473, 6475)                                       -1        30567           True   
    
                                                                                         tissue  \
    subset_pk intervention_pk                                    group_pk individual_pk           
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             plasma   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             plasma   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             plasma   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1              heart   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1              heart   
    ...                                                                                     ...   
    5285      (6473, 6477)                                       -1        30565         plasma   
    5286      (6473, 6475)                                       -1        30565         plasma   
    5287      (6473,)                                            -1        30567         plasma   
    5288      (6473, 6477)                                       -1        30567         plasma   
    5289      (6473, 6475)                                       -1        30567         plasma   
    
                                                                                        tissue_label  \
    subset_pk intervention_pk                                    group_pk individual_pk                
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1                  plasma   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                  plasma   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1                  plasma   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1                   heart   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                   heart   
    ...                                                                                          ...   
    5285      (6473, 6477)                                       -1        30565              plasma   
    5286      (6473, 6475)                                       -1        30565              plasma   
    5287      (6473,)                                            -1        30567              plasma   
    5288      (6473, 6477)                                       -1        30567              plasma   
    5289      (6473, 6475)                                       -1        30567              plasma   
    
                                                                                        method  \
    subset_pk intervention_pk                                    group_pk individual_pk          
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1               NaN   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1               NaN   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1               NaN   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1               NaN   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1               NaN   
    ...                                                                                    ...   
    5285      (6473, 6477)                                       -1        30565          hplc   
    5286      (6473, 6475)                                       -1        30565          hplc   
    5287      (6473,)                                            -1        30567          hplc   
    5288      (6473, 6477)                                       -1        30567          hplc   
    5289      (6473, 6475)                                       -1        30567          hplc   
    
                                                                                                                          method_label  \
    subset_pk intervention_pk                                    group_pk individual_pk                                                  
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1                                                       NaN   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                                                       NaN   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1                                                       NaN   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1                                                       NaN   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                                                       NaN   
    ...                                                                                                                            ...   
    5285      (6473, 6477)                                       -1        30565         High-performance liquid chromatography (HPLC)   
    5286      (6473, 6475)                                       -1        30565         High-performance liquid chromatography (HPLC)   
    5287      (6473,)                                            -1        30567         High-performance liquid chromatography (HPLC)   
    5288      (6473, 6477)                                       -1        30567         High-performance liquid chromatography (HPLC)   
    5289      (6473, 6475)                                       -1        30567         High-performance liquid chromatography (HPLC)   
    
                                                                                         ...  \
    subset_pk intervention_pk                                    group_pk individual_pk  ...   
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             ...   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             ...   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             ...   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             ...   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             ...   
    ...                                                                                  ...   
    5285      (6473, 6477)                                       -1        30565         ...   
    5286      (6473, 6475)                                       -1        30565         ...   
    5287      (6473,)                                            -1        30567         ...   
    5288      (6473, 6477)                                       -1        30567         ...   
    5289      (6473, 6475)                                       -1        30567         ...   
    
                                                                                         substance_label  \
    subset_pk intervention_pk                                    group_pk individual_pk                    
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1                  metoprolol   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                  metoprolol   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1                  metoprolol   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1                         NaN   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                         NaN   
    ...                                                                                              ...   
    5285      (6473, 6477)                                       -1        30565         caffeine (137X)   
    5286      (6473, 6475)                                       -1        30565         caffeine (137X)   
    5287      (6473,)                                            -1        30567         caffeine (137X)   
    5288      (6473, 6477)                                       -1        30567         caffeine (137X)   
    5289      (6473, 6475)                                       -1        30567         caffeine (137X)   
    
                                                                                                                                     value  \
    subset_pk intervention_pk                                    group_pk individual_pk                                                      
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1                                                           NaN   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                                                           NaN   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1                                                           NaN   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1                                                           NaN   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                                                           NaN   
    ...                                                                                                                                ...   
    5285      (6473, 6477)                                       -1        30565         (0.005779762, 0.007342083500000001, 0.00498195...   
    5286      (6473, 6475)                                       -1        30565         (0.007626138700000001, 0.0055641580000000005, ...   
    5287      (6473,)                                            -1        30567         (0.006376934, 0.005785014599999999, 0.00397134...   
    5288      (6473, 6477)                                       -1        30567         (0.008225058, 0.008221353, 0.00629417099999999...   
    5289      (6473, 6475)                                       -1        30567         (0.007026457000000001, 0.006938287700000001, 0...   
    
                                                                                                                                      mean  \
    subset_pk intervention_pk                                    group_pk individual_pk                                                      
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             (1.3223154736189403e-05, 5.053727096804881e-05...   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             (3.6470419909156005e-05, 8.83924221952528e-05,...   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             (2.18782508441315e-05, 1.9968919659494645e-05,...   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             (5.99242, 22.291657999999998, 17.3896269999999...   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             (10.060966, 19.742437, 14.791641, 9.828696, 8....   
    ...                                                                                                                                ...   
    5285      (6473, 6477)                                       -1        30565                                                       NaN   
    5286      (6473, 6475)                                       -1        30565                                                       NaN   
    5287      (6473,)                                            -1        30567                                                       NaN   
    5288      (6473, 6477)                                       -1        30567                                                       NaN   
    5289      (6473, 6475)                                       -1        30567                                                       NaN   
    
                                                                                        median  \
    subset_pk intervention_pk                                    group_pk individual_pk          
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1               NaN   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1               NaN   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1               NaN   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1               NaN   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1               NaN   
    ...                                                                                    ...   
    5285      (6473, 6477)                                       -1        30565           NaN   
    5286      (6473, 6475)                                       -1        30565           NaN   
    5287      (6473,)                                            -1        30567           NaN   
    5288      (6473, 6477)                                       -1        30567           NaN   
    5289      (6473, 6475)                                       -1        30567           NaN   
    
                                                                                         min  \
    subset_pk intervention_pk                                    group_pk individual_pk        
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             NaN   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             NaN   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             NaN   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             NaN   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             NaN   
    ...                                                                                  ...   
    5285      (6473, 6477)                                       -1        30565         NaN   
    5286      (6473, 6475)                                       -1        30565         NaN   
    5287      (6473,)                                            -1        30567         NaN   
    5288      (6473, 6477)                                       -1        30567         NaN   
    5289      (6473, 6475)                                       -1        30567         NaN   
    
                                                                                         max  \
    subset_pk intervention_pk                                    group_pk individual_pk        
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             NaN   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             NaN   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             NaN   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             NaN   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             NaN   
    ...                                                                                  ...   
    5285      (6473, 6477)                                       -1        30565         NaN   
    5286      (6473, 6475)                                       -1        30565         NaN   
    5287      (6473,)                                            -1        30567         NaN   
    5288      (6473, 6477)                                       -1        30567         NaN   
    5289      (6473, 6475)                                       -1        30567         NaN   
    
                                                                                                                                        sd  \
    subset_pk intervention_pk                                    group_pk individual_pk                                                      
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             (1.030063798165528e-05, 3.935558314793124e-05,...   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             (2.1727913322049826e-05, 2.9518215551111463e-0...   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             (1.4996018928739371e-05, 1.4993540482147688e-0...   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             (6.793094260620936, 4.414942082867226, 4.75367...   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             (7.98085849421614, 5.432896055288376, 5.263969...   
    ...                                                                                                                                ...   
    5285      (6473, 6477)                                       -1        30565                                                       NaN   
    5286      (6473, 6475)                                       -1        30565                                                       NaN   
    5287      (6473,)                                            -1        30567                                                       NaN   
    5288      (6473, 6477)                                       -1        30567                                                       NaN   
    5289      (6473, 6475)                                       -1        30567                                                       NaN   
    
                                                                                                                                        se  \
    subset_pk intervention_pk                                    group_pk individual_pk                                                      
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             (2.97353805576678e-06, 1.1360978262286402e-05,...   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             (6.2723083027071615e-06, 8.521174847215801e-06...   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             (4.3289777826402e-06, 4.32826231673676e-06, 4....   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             (1.9609974, 1.274484, 1.372267, 2.009764, 2.01...   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             (2.3038754, 1.568342, 1.519577, 1.911979, 2.45...   
    ...                                                                                                                                ...   
    5285      (6473, 6477)                                       -1        30565                                                       NaN   
    5286      (6473, 6475)                                       -1        30565                                                       NaN   
    5287      (6473,)                                            -1        30567                                                       NaN   
    5288      (6473, 6477)                                       -1        30567                                                       NaN   
    5289      (6473, 6475)                                       -1        30567                                                       NaN   
    
                                                                                                                                        cv  \
    subset_pk intervention_pk                                    group_pk individual_pk                                                      
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             [0.778984908454885, 0.7787437349518345, 0.2892...   
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             [0.5957681149866599, 0.3339450918757238, 0.320...   
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             [0.6854304320567665, 0.7508438482308527, 0.554...   
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1             [1.1336145097674957, 0.19805355361486465, 0.27...   
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             [0.7932497231594003, 0.2751887244360145, 0.355...   
    ...                                                                                                                                ...   
    5285      (6473, 6477)                                       -1        30565                                                       NaN   
    5286      (6473, 6475)                                       -1        30565                                                       NaN   
    5287      (6473,)                                            -1        30567                                                       NaN   
    5288      (6473, 6477)                                       -1        30567                                                       NaN   
    5289      (6473, 6475)                                       -1        30567                                                       NaN   
    
                                                                                                 unit  
    subset_pk intervention_pk                                    group_pk individual_pk                
    3307      (4448, 4449, 4450, 4451, 4452)                      2799    -1             gram / liter  
    3308      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1             gram / liter  
    3309      (4443, 4444, 4445, 4446, 4447)                      2799    -1             gram / liter  
    3310      (4448, 4449, 4450, 4451, 4452)                      2799    -1                  percent  
    3311      (4453, 4454, 4455, 4456, 4457, 4458, 4459, 4460...  2799    -1                  percent  
    ...                                                                                           ...  
    5285      (6473, 6477)                                       -1        30565         gram / liter  
    5286      (6473, 6475)                                       -1        30565         gram / liter  
    5287      (6473,)                                            -1        30567         gram / liter  
    5288      (6473, 6477)                                       -1        30567         gram / liter  
    5289      (6473, 6475)                                       -1        30567         gram / liter  
    
    [722 rows x 28 columns]



.. code:: ipython3

    data.scatters
    




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
          <th>subset_pk</th>
          <th>subset_name</th>
          <th>x_outputs_pk</th>
          <th>x_intervention_pk</th>
          <th>x_group_pk</th>
          <th>x_individual_pk</th>
          <th>x_normed</th>
          <th>...</th>
          <th>y_mean</th>
          <th>y_median</th>
          <th>y_min</th>
          <th>y_max</th>
          <th>y_sd</th>
          <th>y_se</th>
          <th>y_cv</th>
          <th>y_unit</th>
          <th>y_dimension</th>
          <th>y_data_point</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0</td>
          <td>28929443</td>
          <td>Lammers2018</td>
          <td>4557</td>
          <td>freefraction_vs_concentration_caffeine_control</td>
          <td>[233796, 233797, 233798, 233799, 233800, 23380...</td>
          <td>(5962, 5963, 5964, 5965, 5966)</td>
          <td>NaN</td>
          <td>[25771, 25772, 25773, 25774, 25775, 25776, 257...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
          <td>1</td>
          <td>[40158, 40159, 40160, 40161, 40162, 40163, 401...</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>28929443</td>
          <td>Lammers2018</td>
          <td>4558</td>
          <td>freefraction_vs_concentration_caffeine_fasting</td>
          <td>[233821, 233822, 233823, 233824, 233825, 23382...</td>
          <td>(5962, 5963, 5964, 5965, 5966)</td>
          <td>NaN</td>
          <td>[25796, 25797, 25798, 25799, 25800, 25801, 258...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
          <td>1</td>
          <td>[40183, 40184, 40185, 40186, 40187, 40188, 401...</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>28929443</td>
          <td>Lammers2018</td>
          <td>4559</td>
          <td>freefraction_vs_concentration_metoprolol_control</td>
          <td>[233857, 233858, 233859, 233860, 233861, 23386...</td>
          <td>(5962, 5963, 5964, 5965, 5966)</td>
          <td>NaN</td>
          <td>[25832, 25833, 25834, 25835, 25836, 25837, 258...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
          <td>1</td>
          <td>[40219, 40220, 40221, 40222, 40223, 40224, 402...</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>28929443</td>
          <td>Lammers2018</td>
          <td>4560</td>
          <td>freefraction_vs_concentration_metoprolol_fasting</td>
          <td>[233883, 233884, 233885, 233886, 233887, 23388...</td>
          <td>(5962, 5963, 5964, 5965, 5966)</td>
          <td>NaN</td>
          <td>[25858, 25859, 25860, 25861, 25862, 25863, 258...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
          <td>1</td>
          <td>[40245, 40246, 40247, 40248, 40249, 40250, 402...</td>
        </tr>
        <tr>
          <th>4</th>
          <td>4</td>
          <td>28929443</td>
          <td>Lammers2018</td>
          <td>4561</td>
          <td>freefraction_vs_concentration_warfarin_control</td>
          <td>[233916, 233917, 233918, 233919, 233920, 23392...</td>
          <td>(5962, 5963, 5964, 5965, 5966)</td>
          <td>NaN</td>
          <td>[25891, 25892, 25893, 25894, 25895, 25896, 258...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
          <td>1</td>
          <td>[40278, 40279, 40280, 40281, 40282, 40283, 402...</td>
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
          <th>75</th>
          <td>75</td>
          <td>PKDB00012</td>
          <td>Birkett1991</td>
          <td>4307</td>
          <td>plasma_urine</td>
          <td>[217839, 217840, 217841, 217842, 217843, 21784...</td>
          <td>(5538,)</td>
          <td>NaN</td>
          <td>[24641, 24642, 24643, 24644, 24645, 24646, 246...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
          <td>1</td>
          <td>[37450, 37451, 37452, 37453, 37454, 37455, 374...</td>
        </tr>
        <tr>
          <th>76</th>
          <td>76</td>
          <td>26862045</td>
          <td>Chia2016</td>
          <td>4390</td>
          <td>PX/CA_bmi_corr</td>
          <td>[223791, 223792, 223793, 223794, 223795, 22379...</td>
          <td>(5638,)</td>
          <td>NaN</td>
          <td>[24861, 24862, 24863, 24864, 24865, 24866, 248...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>kilogram / meter ** 2</td>
          <td>1</td>
          <td>[38180, 38181, 38182, 38183, 38184, 38185, 381...</td>
        </tr>
        <tr>
          <th>77</th>
          <td>77</td>
          <td>26862045</td>
          <td>Chia2016</td>
          <td>4391</td>
          <td>CA_bmi_corr</td>
          <td>[223841, 223842, 223843, 223844, 223845, 22384...</td>
          <td>(5638,)</td>
          <td>NaN</td>
          <td>[24911, 24912, 24913, 24914, 24915, 24916, 249...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>kilogram / meter ** 2</td>
          <td>1</td>
          <td>[38230, 38231, 38232, 38233, 38234, 38235, 382...</td>
        </tr>
        <tr>
          <th>78</th>
          <td>78</td>
          <td>26862045</td>
          <td>Chia2016</td>
          <td>4392</td>
          <td>PX_bmi_corr</td>
          <td>[223889, 223890, 223891, 223892, 223893, 22389...</td>
          <td>(5638,)</td>
          <td>NaN</td>
          <td>[24959, 24960, 24961, 24962, 24963, 24964, 249...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>kilogram / meter ** 2</td>
          <td>1</td>
          <td>[38278, 38279, 38280, 38281, 38282, 38283, 382...</td>
        </tr>
        <tr>
          <th>79</th>
          <td>79</td>
          <td>26862045</td>
          <td>Chia2016</td>
          <td>4393</td>
          <td>CA+PX_bmi_corr</td>
          <td>[223939, 223940, 223941, 223942, 223943, 22394...</td>
          <td>(5638,)</td>
          <td>NaN</td>
          <td>[25009, 25010, 25011, 25012, 25013, 25014, 250...</td>
          <td>True</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>kilogram / meter ** 2</td>
          <td>1</td>
          <td>[38328, 38329, 38330, 38331, 38332, 38333, 383...</td>
        </tr>
      </tbody>
    </table>
    <p>80 rows × 67 columns</p>
    </div>




.. parsed-literal::

        Unnamed: 0  study_sid   study_name  subset_pk  \
    0            0   28929443  Lammers2018       4557   
    1            1   28929443  Lammers2018       4558   
    2            2   28929443  Lammers2018       4559   
    3            3   28929443  Lammers2018       4560   
    4            4   28929443  Lammers2018       4561   
    ..         ...        ...          ...        ...   
    75          75  PKDB00012  Birkett1991       4307   
    76          76   26862045     Chia2016       4390   
    77          77   26862045     Chia2016       4391   
    78          78   26862045     Chia2016       4392   
    79          79   26862045     Chia2016       4393   
    
                                             subset_name  \
    0     freefraction_vs_concentration_caffeine_control   
    1     freefraction_vs_concentration_caffeine_fasting   
    2   freefraction_vs_concentration_metoprolol_control   
    3   freefraction_vs_concentration_metoprolol_fasting   
    4     freefraction_vs_concentration_warfarin_control   
    ..                                               ...   
    75                                      plasma_urine   
    76                                    PX/CA_bmi_corr   
    77                                       CA_bmi_corr   
    78                                       PX_bmi_corr   
    79                                    CA+PX_bmi_corr   
    
                                             x_outputs_pk  \
    0   [233796, 233797, 233798, 233799, 233800, 23380...   
    1   [233821, 233822, 233823, 233824, 233825, 23382...   
    2   [233857, 233858, 233859, 233860, 233861, 23386...   
    3   [233883, 233884, 233885, 233886, 233887, 23388...   
    4   [233916, 233917, 233918, 233919, 233920, 23392...   
    ..                                                ...   
    75  [217839, 217840, 217841, 217842, 217843, 21784...   
    76  [223791, 223792, 223793, 223794, 223795, 22379...   
    77  [223841, 223842, 223843, 223844, 223845, 22384...   
    78  [223889, 223890, 223891, 223892, 223893, 22389...   
    79  [223939, 223940, 223941, 223942, 223943, 22394...   
    
                     x_intervention_pk  x_group_pk  \
    0   (5962, 5963, 5964, 5965, 5966)         NaN   
    1   (5962, 5963, 5964, 5965, 5966)         NaN   
    2   (5962, 5963, 5964, 5965, 5966)         NaN   
    3   (5962, 5963, 5964, 5965, 5966)         NaN   
    4   (5962, 5963, 5964, 5965, 5966)         NaN   
    ..                             ...         ...   
    75                         (5538,)         NaN   
    76                         (5638,)         NaN   
    77                         (5638,)         NaN   
    78                         (5638,)         NaN   
    79                         (5638,)         NaN   
    
                                          x_individual_pk  x_normed  ...  y_mean  \
    0   [25771, 25772, 25773, 25774, 25775, 25776, 257...      True  ...     NaN   
    1   [25796, 25797, 25798, 25799, 25800, 25801, 258...      True  ...     NaN   
    2   [25832, 25833, 25834, 25835, 25836, 25837, 258...      True  ...     NaN   
    3   [25858, 25859, 25860, 25861, 25862, 25863, 258...      True  ...     NaN   
    4   [25891, 25892, 25893, 25894, 25895, 25896, 258...      True  ...     NaN   
    ..                                                ...       ...  ...     ...   
    75  [24641, 24642, 24643, 24644, 24645, 24646, 246...      True  ...     NaN   
    76  [24861, 24862, 24863, 24864, 24865, 24866, 248...      True  ...     NaN   
    77  [24911, 24912, 24913, 24914, 24915, 24916, 249...      True  ...     NaN   
    78  [24959, 24960, 24961, 24962, 24963, 24964, 249...      True  ...     NaN   
    79  [25009, 25010, 25011, 25012, 25013, 25014, 250...      True  ...     NaN   
    
       y_median y_min y_max y_sd y_se y_cv                 y_unit y_dimension  \
    0       NaN   NaN   NaN  NaN  NaN  NaN           gram / liter           1   
    1       NaN   NaN   NaN  NaN  NaN  NaN           gram / liter           1   
    2       NaN   NaN   NaN  NaN  NaN  NaN           gram / liter           1   
    3       NaN   NaN   NaN  NaN  NaN  NaN           gram / liter           1   
    4       NaN   NaN   NaN  NaN  NaN  NaN           gram / liter           1   
    ..      ...   ...   ...  ...  ...  ...                    ...         ...   
    75      NaN   NaN   NaN  NaN  NaN  NaN           gram / liter           1   
    76      NaN   NaN   NaN  NaN  NaN  NaN  kilogram / meter ** 2           1   
    77      NaN   NaN   NaN  NaN  NaN  NaN  kilogram / meter ** 2           1   
    78      NaN   NaN   NaN  NaN  NaN  NaN  kilogram / meter ** 2           1   
    79      NaN   NaN   NaN  NaN  NaN  NaN  kilogram / meter ** 2           1   
    
                                             y_data_point  
    0   [40158, 40159, 40160, 40161, 40162, 40163, 401...  
    1   [40183, 40184, 40185, 40186, 40187, 40188, 401...  
    2   [40219, 40220, 40221, 40222, 40223, 40224, 402...  
    3   [40245, 40246, 40247, 40248, 40249, 40250, 402...  
    4   [40278, 40279, 40280, 40281, 40282, 40283, 402...  
    ..                                                ...  
    75  [37450, 37451, 37452, 37453, 37454, 37455, 374...  
    76  [38180, 38181, 38182, 38183, 38184, 38185, 381...  
    77  [38230, 38231, 38232, 38233, 38234, 38235, 382...  
    78  [38278, 38279, 38280, 38281, 38282, 38283, 382...  
    79  [38328, 38329, 38330, 38331, 38332, 38333, 383...  
    
    [80 rows x 67 columns]



