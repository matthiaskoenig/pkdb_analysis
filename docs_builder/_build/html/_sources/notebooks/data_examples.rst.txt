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


.. parsed-literal::

    INFO NumExpr defaulting to 8 threads.


.. parsed-literal::

    ------------------------------
    PKData (139910592982608)
    ------------------------------
    studies           505  (  505)
    groups           1456  (11993)
    individuals      6395  (57683)
    interventions    1209  ( 1865)
    outputs         72206  (72206)
    timecourses       423  (  423)
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
    PKData (139910592982608)
    ------------------------------
    studies           505  (  505)
    groups           1456  (11993)
    individuals      6395  (57683)
    interventions    1209  ( 1865)
    outputs         72206  (72206)
    timecourses       423  (  423)
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
          <th>0</th>
          <td>0</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>sex</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>25</td>
          <td>-1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1</td>
          <td>8</td>
          <td>NaN</td>
          <td>F</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>species</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>-1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1</td>
          <td>5</td>
          <td>NaN</td>
          <td>homo sapiens</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>healthy</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>-1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1</td>
          <td>6</td>
          <td>NaN</td>
          <td>Y</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>sex</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>17</td>
          <td>-1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1</td>
          <td>7</td>
          <td>NaN</td>
          <td>M</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>4</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>species</td>
          <td>21</td>
          <td>obese</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2</td>
          <td>5</td>
          <td>NaN</td>
          <td>homo sapiens</td>
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
          <th>11988</th>
          <td>11988</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>sex</td>
          <td>24</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>24</td>
          <td>-1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>28452</td>
          <td>NaN</td>
          <td>M</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>11989</th>
          <td>11989</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>age</td>
          <td>24</td>
          <td>all</td>
          <td>40.0</td>
          <td>nan</td>
          <td>24</td>
          <td>-1</td>
          <td>...</td>
          <td>year</td>
          <td>NaN</td>
          <td>18.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>28453</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>11990</th>
          <td>11990</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>bmi</td>
          <td>24</td>
          <td>all</td>
          <td>24.0</td>
          <td>nan</td>
          <td>24</td>
          <td>-1</td>
          <td>...</td>
          <td>kilogram / meter ** 2</td>
          <td>NaN</td>
          <td>19.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>28454</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>11991</th>
          <td>11991</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>overnight fast</td>
          <td>24</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>24</td>
          <td>-1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>28455</td>
          <td>NaN</td>
          <td>Y</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>11992</th>
          <td>11992</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>species</td>
          <td>24</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>24</td>
          <td>-1</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>28456</td>
          <td>NaN</td>
          <td>homo sapiens</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>11993 rows × 21 columns</p>
    </div>




.. parsed-literal::

           Unnamed: 0     study_name  study_sid measurement_type  group_count  \
    0               0  Abernethy1982  PKDB00198              sex           42   
    1               1  Abernethy1982  PKDB00198          species           42   
    2               2  Abernethy1982  PKDB00198          healthy           42   
    3               3  Abernethy1982  PKDB00198              sex           42   
    4               4  Abernethy1982  PKDB00198          species           21   
    ...           ...            ...        ...              ...          ...   
    11988       11988      Zhang2016  PKDB00275              sex           24   
    11989       11989      Zhang2016  PKDB00275              age           24   
    11990       11990      Zhang2016  PKDB00275              bmi           24   
    11991       11991      Zhang2016  PKDB00275   overnight fast           24   
    11992       11992      Zhang2016  PKDB00275          species           24   
    
          group_name   max substance  count  group_parent_pk  ...  \
    0            all   NaN       nan     25               -1  ...   
    1            all   NaN       nan     42               -1  ...   
    2            all   NaN       nan     42               -1  ...   
    3            all   NaN       nan     17               -1  ...   
    4          obese   NaN       nan     42                1  ...   
    ...          ...   ...       ...    ...              ...  ...   
    11988        all   NaN       nan     24               -1  ...   
    11989        all  40.0       nan     24               -1  ...   
    11990        all  24.0       nan     24               -1  ...   
    11991        all   NaN       nan     24               -1  ...   
    11992        all   NaN       nan     24               -1  ...   
    
                            unit  se   min  cv  median  group_pk  \
    0                        NaN NaN   NaN NaN     NaN         1   
    1                        NaN NaN   NaN NaN     NaN         1   
    2                        NaN NaN   NaN NaN     NaN         1   
    3                        NaN NaN   NaN NaN     NaN         1   
    4                        NaN NaN   NaN NaN     NaN         2   
    ...                      ...  ..   ...  ..     ...       ...   
    11988                    NaN NaN   NaN NaN     NaN      1504   
    11989                   year NaN  18.0 NaN     NaN      1504   
    11990  kilogram / meter ** 2 NaN  19.0 NaN     NaN      1504   
    11991                    NaN NaN   NaN NaN     NaN      1504   
    11992                    NaN NaN   NaN NaN     NaN      1504   
    
           characteristica_pk  mean        choice value  
    0                       8   NaN             F   NaN  
    1                       5   NaN  homo sapiens   NaN  
    2                       6   NaN             Y   NaN  
    3                       7   NaN             M   NaN  
    4                       5   NaN  homo sapiens   NaN  
    ...                   ...   ...           ...   ...  
    11988               28452   NaN             M   NaN  
    11989               28453   NaN           NaN   NaN  
    11990               28454   NaN           NaN   NaN  
    11991               28455   NaN             Y   NaN  
    11992               28456   NaN  homo sapiens   NaN  
    
    [11993 rows x 21 columns]



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
          <th rowspan="4" valign="top">1</th>
          <th>5</th>
          <td>1</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>species</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
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
          <th>6</th>
          <td>2</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>healthy</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
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
          <th>7</th>
          <td>3</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>sex</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>17</td>
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
          <th>8</th>
          <td>0</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>sex</td>
          <td>42</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>25</td>
          <td>-1</td>
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
          <th>2</th>
          <th>5</th>
          <td>4</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>species</td>
          <td>21</td>
          <td>obese</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>1</td>
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
          <th rowspan="5" valign="top">1504</th>
          <th>28452</th>
          <td>11988</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>sex</td>
          <td>24</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>24</td>
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
          <th>28453</th>
          <td>11989</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>age</td>
          <td>24</td>
          <td>all</td>
          <td>40.0</td>
          <td>nan</td>
          <td>24</td>
          <td>-1</td>
          <td>NaN</td>
          <td>year</td>
          <td>NaN</td>
          <td>18.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>28454</th>
          <td>11990</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>bmi</td>
          <td>24</td>
          <td>all</td>
          <td>24.0</td>
          <td>nan</td>
          <td>24</td>
          <td>-1</td>
          <td>NaN</td>
          <td>kilogram / meter ** 2</td>
          <td>NaN</td>
          <td>19.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>28455</th>
          <td>11991</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>overnight fast</td>
          <td>24</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>24</td>
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
          <th>28456</th>
          <td>11992</td>
          <td>Zhang2016</td>
          <td>PKDB00275</td>
          <td>species</td>
          <td>24</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>24</td>
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
      </tbody>
    </table>
    <p>11993 rows × 19 columns</p>
    </div>




.. parsed-literal::

                                 Unnamed: 0     study_name  study_sid  \
    group_pk characteristica_pk                                         
    1        5                            1  Abernethy1982  PKDB00198   
             6                            2  Abernethy1982  PKDB00198   
             7                            3  Abernethy1982  PKDB00198   
             8                            0  Abernethy1982  PKDB00198   
    2        5                            4  Abernethy1982  PKDB00198   
    ...                                 ...            ...        ...   
    1504     28452                    11988      Zhang2016  PKDB00275   
             28453                    11989      Zhang2016  PKDB00275   
             28454                    11990      Zhang2016  PKDB00275   
             28455                    11991      Zhang2016  PKDB00275   
             28456                    11992      Zhang2016  PKDB00275   
    
                                measurement_type  group_count group_name   max  \
    group_pk characteristica_pk                                                  
    1        5                           species           42        all   NaN   
             6                           healthy           42        all   NaN   
             7                               sex           42        all   NaN   
             8                               sex           42        all   NaN   
    2        5                           species           21      obese   NaN   
    ...                                      ...          ...        ...   ...   
    1504     28452                           sex           24        all   NaN   
             28453                           age           24        all  40.0   
             28454                           bmi           24        all  24.0   
             28455                overnight fast           24        all   NaN   
             28456                       species           24        all   NaN   
    
                                substance  count  group_parent_pk  sd  \
    group_pk characteristica_pk                                         
    1        5                        nan     42               -1 NaN   
             6                        nan     42               -1 NaN   
             7                        nan     17               -1 NaN   
             8                        nan     25               -1 NaN   
    2        5                        nan     42                1 NaN   
    ...                               ...    ...              ...  ..   
    1504     28452                    nan     24               -1 NaN   
             28453                    nan     24               -1 NaN   
             28454                    nan     24               -1 NaN   
             28455                    nan     24               -1 NaN   
             28456                    nan     24               -1 NaN   
    
                                                  unit  se   min  cv  median  \
    group_pk characteristica_pk                                                
    1        5                                     NaN NaN   NaN NaN     NaN   
             6                                     NaN NaN   NaN NaN     NaN   
             7                                     NaN NaN   NaN NaN     NaN   
             8                                     NaN NaN   NaN NaN     NaN   
    2        5                                     NaN NaN   NaN NaN     NaN   
    ...                                            ...  ..   ...  ..     ...   
    1504     28452                                 NaN NaN   NaN NaN     NaN   
             28453                                year NaN  18.0 NaN     NaN   
             28454               kilogram / meter ** 2 NaN  19.0 NaN     NaN   
             28455                                 NaN NaN   NaN NaN     NaN   
             28456                                 NaN NaN   NaN NaN     NaN   
    
                                 mean        choice  value  
    group_pk characteristica_pk                             
    1        5                    NaN  homo sapiens    NaN  
             6                    NaN             Y    NaN  
             7                    NaN             M    NaN  
             8                    NaN             F    NaN  
    2        5                    NaN  homo sapiens    NaN  
    ...                           ...           ...    ...  
    1504     28452                NaN             M    NaN  
             28453                NaN           NaN    NaN  
             28454                NaN           NaN    NaN  
             28455                NaN             Y    NaN  
             28456                NaN  homo sapiens    NaN  
    
    [11993 rows x 19 columns]



To access the number of items use the ``*_count``.

.. code:: ipython3

    print(f"Number of groups: {data.groups_count}")


.. parsed-literal::

    Number of groups: 1456


The ``groups``, ``individuals``, ``interventions``, ``outputs`` and
``timecourses`` are ``pandas.DataFrame`` instances, so all the classical
pandas operations can be applied on the data. For instance to access a
single ``group`` use logical indexing by the ``group_pk`` field. E.g. to
get the group ``20`` use

.. code:: ipython3

    data.groups[data.groups.group_pk==312]



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
          <th>2472</th>
          <td>2472</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>sex</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6112</td>
          <td>NaN</td>
          <td>M</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2473</th>
          <td>2473</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>smoking</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6113</td>
          <td>NaN</td>
          <td>N</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2474</th>
          <td>2474</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>alcohol</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6114</td>
          <td>NaN</td>
          <td>N</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2475</th>
          <td>2475</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>abstinence medication</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>day</td>
          <td>NaN</td>
          <td>30.4375</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6115</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2476</th>
          <td>2476</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>kidney function test</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6116</td>
          <td>NaN</td>
          <td>normal</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2477</th>
          <td>2477</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>liver function test</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6117</td>
          <td>NaN</td>
          <td>normal</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2478</th>
          <td>2478</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>overnight fast</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6118</td>
          <td>NaN</td>
          <td>Y</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2479</th>
          <td>2479</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>age</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>6</td>
          <td>311</td>
          <td>...</td>
          <td>year</td>
          <td>2.6</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6121</td>
          <td>33.3</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2480</th>
          <td>2480</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>weight</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>6</td>
          <td>311</td>
          <td>...</td>
          <td>kilogram</td>
          <td>2.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6122</td>
          <td>56.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2481</th>
          <td>2481</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>species</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6110</td>
          <td>NaN</td>
          <td>homo sapiens</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2482</th>
          <td>2482</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>healthy</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>312</td>
          <td>6111</td>
          <td>NaN</td>
          <td>NR</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>11 rows × 21 columns</p>
    </div>




.. parsed-literal::

          Unnamed: 0 study_name  study_sid       measurement_type  group_count  \
    2472        2472    Ray1986  PKDB00257                    sex            6   
    2473        2473    Ray1986  PKDB00257                smoking            6   
    2474        2474    Ray1986  PKDB00257                alcohol            6   
    2475        2475    Ray1986  PKDB00257  abstinence medication            6   
    2476        2476    Ray1986  PKDB00257   kidney function test            6   
    2477        2477    Ray1986  PKDB00257    liver function test            6   
    2478        2478    Ray1986  PKDB00257         overnight fast            6   
    2479        2479    Ray1986  PKDB00257                    age            6   
    2480        2480    Ray1986  PKDB00257                 weight            6   
    2481        2481    Ray1986  PKDB00257                species            6   
    2482        2482    Ray1986  PKDB00257                healthy            6   
    
         group_name  max substance  count  group_parent_pk  ...      unit   se  \
    2472   patients  NaN       nan     13              311  ...       NaN  NaN   
    2473   patients  NaN       nan     13              311  ...       NaN  NaN   
    2474   patients  NaN       nan     13              311  ...       NaN  NaN   
    2475   patients  NaN       nan     13              311  ...       day  NaN   
    2476   patients  NaN       nan     13              311  ...       NaN  NaN   
    2477   patients  NaN       nan     13              311  ...       NaN  NaN   
    2478   patients  NaN       nan     13              311  ...       NaN  NaN   
    2479   patients  NaN       nan      6              311  ...      year  2.6   
    2480   patients  NaN       nan      6              311  ...  kilogram  2.0   
    2481   patients  NaN       nan     13              311  ...       NaN  NaN   
    2482   patients  NaN       nan     13              311  ...       NaN  NaN   
    
              min  cv  median  group_pk  characteristica_pk  mean        choice  \
    2472      NaN NaN     NaN       312                6112   NaN             M   
    2473      NaN NaN     NaN       312                6113   NaN             N   
    2474      NaN NaN     NaN       312                6114   NaN             N   
    2475  30.4375 NaN     NaN       312                6115   NaN           NaN   
    2476      NaN NaN     NaN       312                6116   NaN        normal   
    2477      NaN NaN     NaN       312                6117   NaN        normal   
    2478      NaN NaN     NaN       312                6118   NaN             Y   
    2479      NaN NaN     NaN       312                6121  33.3           NaN   
    2480      NaN NaN     NaN       312                6122  56.0           NaN   
    2481      NaN NaN     NaN       312                6110   NaN  homo sapiens   
    2482      NaN NaN     NaN       312                6111   NaN            NR   
    
         value  
    2472   NaN  
    2473   NaN  
    2474   NaN  
    2475   NaN  
    2476   NaN  
    2477   NaN  
    2478   NaN  
    2479   NaN  
    2480   NaN  
    2481   NaN  
    2482   NaN  
    
    [11 rows x 21 columns]



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
          <th>6110</th>
          <td>2481</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>species</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
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
          <th>6111</th>
          <td>2482</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>healthy</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NR</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6112</th>
          <td>2472</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>sex</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
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
          <th>6113</th>
          <td>2473</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>smoking</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
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
          <th>6114</th>
          <td>2474</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>alcohol</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
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
          <th>6115</th>
          <td>2475</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>abstinence medication</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>NaN</td>
          <td>day</td>
          <td>NaN</td>
          <td>30.4375</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6116</th>
          <td>2476</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>kidney function test</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>normal</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6117</th>
          <td>2477</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>liver function test</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>normal</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6118</th>
          <td>2478</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>overnight fast</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>13</td>
          <td>311</td>
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
          <th>6121</th>
          <td>2479</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>age</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>6</td>
          <td>311</td>
          <td>NaN</td>
          <td>year</td>
          <td>2.6</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>33.3</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6122</th>
          <td>2480</td>
          <td>Ray1986</td>
          <td>PKDB00257</td>
          <td>weight</td>
          <td>6</td>
          <td>patients</td>
          <td>NaN</td>
          <td>nan</td>
          <td>6</td>
          <td>311</td>
          <td>NaN</td>
          <td>kilogram</td>
          <td>2.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>56.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>




.. parsed-literal::

                        Unnamed: 0 study_name  study_sid       measurement_type  \
    characteristica_pk                                                            
    6110                      2481    Ray1986  PKDB00257                species   
    6111                      2482    Ray1986  PKDB00257                healthy   
    6112                      2472    Ray1986  PKDB00257                    sex   
    6113                      2473    Ray1986  PKDB00257                smoking   
    6114                      2474    Ray1986  PKDB00257                alcohol   
    6115                      2475    Ray1986  PKDB00257  abstinence medication   
    6116                      2476    Ray1986  PKDB00257   kidney function test   
    6117                      2477    Ray1986  PKDB00257    liver function test   
    6118                      2478    Ray1986  PKDB00257         overnight fast   
    6121                      2479    Ray1986  PKDB00257                    age   
    6122                      2480    Ray1986  PKDB00257                 weight   
    
                        group_count group_name  max substance  count  \
    characteristica_pk                                                 
    6110                          6   patients  NaN       nan     13   
    6111                          6   patients  NaN       nan     13   
    6112                          6   patients  NaN       nan     13   
    6113                          6   patients  NaN       nan     13   
    6114                          6   patients  NaN       nan     13   
    6115                          6   patients  NaN       nan     13   
    6116                          6   patients  NaN       nan     13   
    6117                          6   patients  NaN       nan     13   
    6118                          6   patients  NaN       nan     13   
    6121                          6   patients  NaN       nan      6   
    6122                          6   patients  NaN       nan      6   
    
                        group_parent_pk  sd      unit   se      min  cv  median  \
    characteristica_pk                                                            
    6110                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6111                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6112                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6113                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6114                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6115                            311 NaN       day  NaN  30.4375 NaN     NaN   
    6116                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6117                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6118                            311 NaN       NaN  NaN      NaN NaN     NaN   
    6121                            311 NaN      year  2.6      NaN NaN     NaN   
    6122                            311 NaN  kilogram  2.0      NaN NaN     NaN   
    
                        mean        choice  value  
    characteristica_pk                             
    6110                 NaN  homo sapiens    NaN  
    6111                 NaN            NR    NaN  
    6112                 NaN             M    NaN  
    6113                 NaN             N    NaN  
    6114                 NaN             N    NaN  
    6115                 NaN           NaN    NaN  
    6116                 NaN        normal    NaN  
    6117                 NaN        normal    NaN  
    6118                 NaN             Y    NaN  
    6121                33.3           NaN    NaN  
    6122                56.0           NaN    NaN  



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
          <th rowspan="5" valign="top">1</th>
          <th rowspan="5" valign="top">individual1</th>
          <th>5</th>
          <td>2</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>species</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>7</td>
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
          <th>6</th>
          <td>3</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>healthy</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>7</td>
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
          <th>33</th>
          <td>0</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>obesity index</td>
          <td>112.0</td>
          <td>nan</td>
          <td>21</td>
          <td>7</td>
          <td>NaN</td>
          <td>percent</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>34</th>
          <td>1</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>weight (categorial)</td>
          <td>NaN</td>
          <td>nan</td>
          <td>21</td>
          <td>7</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>normal</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>52</th>
          <td>4</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>weight</td>
          <td>66.0</td>
          <td>nan</td>
          <td>11</td>
          <td>7</td>
          <td>NaN</td>
          <td>kilogram</td>
          <td>NaN</td>
          <td>45.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>55.0</td>
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
          <th rowspan="5" valign="top">6439</th>
          <th rowspan="5" valign="top">16</th>
          <th>28328</th>
          <td>57679</td>
          <td>Spahn1990</td>
          <td>PKDB00289</td>
          <td>disease</td>
          <td>NaN</td>
          <td>nan</td>
          <td>9</td>
          <td>1503</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>renal disease</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>28439</th>
          <td>57682</td>
          <td>Spahn1990</td>
          <td>PKDB00289</td>
          <td>sex</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>1503</td>
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
          <th>28440</th>
          <td>57677</td>
          <td>Spahn1990</td>
          <td>PKDB00289</td>
          <td>age</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>1503</td>
          <td>NaN</td>
          <td>year</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>31.00</td>
        </tr>
        <tr>
          <th>28441</th>
          <td>57680</td>
          <td>Spahn1990</td>
          <td>PKDB00289</td>
          <td>clearance</td>
          <td>NaN</td>
          <td>creatinine</td>
          <td>1</td>
          <td>1503</td>
          <td>NaN</td>
          <td>liter / hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2.88</td>
        </tr>
        <tr>
          <th>28442</th>
          <td>57681</td>
          <td>Spahn1990</td>
          <td>PKDB00289</td>
          <td>disease</td>
          <td>NaN</td>
          <td>nan</td>
          <td>1</td>
          <td>1503</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>chronic pyelonephritis</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>57683 rows × 17 columns</p>
    </div>




.. parsed-literal::

                                                      Unnamed: 0     study_name  \
    individual_pk individual_name characteristica_pk                              
    1             individual1     5                            2  Abernethy1982   
                                  6                            3  Abernethy1982   
                                  33                           0  Abernethy1982   
                                  34                           1  Abernethy1982   
                                  52                           4  Abernethy1982   
    ...                                                      ...            ...   
    6439          16              28328                    57679      Spahn1990   
                                  28439                    57682      Spahn1990   
                                  28440                    57677      Spahn1990   
                                  28441                    57680      Spahn1990   
                                  28442                    57681      Spahn1990   
    
                                                      study_sid  \
    individual_pk individual_name characteristica_pk              
    1             individual1     5                   PKDB00198   
                                  6                   PKDB00198   
                                  33                  PKDB00198   
                                  34                  PKDB00198   
                                  52                  PKDB00198   
    ...                                                     ...   
    6439          16              28328               PKDB00289   
                                  28439               PKDB00289   
                                  28440               PKDB00289   
                                  28441               PKDB00289   
                                  28442               PKDB00289   
    
                                                         measurement_type    max  \
    individual_pk individual_name characteristica_pk                               
    1             individual1     5                               species    NaN   
                                  6                               healthy    NaN   
                                  33                        obesity index  112.0   
                                  34                  weight (categorial)    NaN   
                                  52                               weight   66.0   
    ...                                                               ...    ...   
    6439          16              28328                           disease    NaN   
                                  28439                               sex    NaN   
                                  28440                               age    NaN   
                                  28441                         clearance    NaN   
                                  28442                           disease    NaN   
    
                                                       substance  count  \
    individual_pk individual_name characteristica_pk                      
    1             individual1     5                          nan     42   
                                  6                          nan     42   
                                  33                         nan     21   
                                  34                         nan     21   
                                  52                         nan     11   
    ...                                                      ...    ...   
    6439          16              28328                      nan      9   
                                  28439                      nan      1   
                                  28440                      nan      1   
                                  28441               creatinine      1   
                                  28442                      nan      1   
    
                                                      individual_group_pk  sd  \
    individual_pk individual_name characteristica_pk                            
    1             individual1     5                                     7 NaN   
                                  6                                     7 NaN   
                                  33                                    7 NaN   
                                  34                                    7 NaN   
                                  52                                    7 NaN   
    ...                                                               ...  ..   
    6439          16              28328                              1503 NaN   
                                  28439                              1503 NaN   
                                  28440                              1503 NaN   
                                  28441                              1503 NaN   
                                  28442                              1503 NaN   
    
                                                              unit  se   min  cv  \
    individual_pk individual_name characteristica_pk                               
    1             individual1     5                            NaN NaN   NaN NaN   
                                  6                            NaN NaN   NaN NaN   
                                  33                       percent NaN   NaN NaN   
                                  34                           NaN NaN   NaN NaN   
                                  52                      kilogram NaN  45.0 NaN   
    ...                                                        ...  ..   ...  ..   
    6439          16              28328                        NaN NaN   NaN NaN   
                                  28439                        NaN NaN   NaN NaN   
                                  28440                       year NaN   NaN NaN   
                                  28441               liter / hour NaN   NaN NaN   
                                  28442                        NaN NaN   NaN NaN   
    
                                                      median  mean  \
    individual_pk individual_name characteristica_pk                 
    1             individual1     5                      NaN   NaN   
                                  6                      NaN   NaN   
                                  33                     NaN   NaN   
                                  34                     NaN   NaN   
                                  52                     NaN  55.0   
    ...                                                  ...   ...   
    6439          16              28328                  NaN   NaN   
                                  28439                  NaN   NaN   
                                  28440                  NaN   NaN   
                                  28441                  NaN   NaN   
                                  28442                  NaN   NaN   
    
                                                                      choice  \
    individual_pk individual_name characteristica_pk                           
    1             individual1     5                             homo sapiens   
                                  6                                        Y   
                                  33                                     NaN   
                                  34                                  normal   
                                  52                                     NaN   
    ...                                                                  ...   
    6439          16              28328                        renal disease   
                                  28439                                    F   
                                  28440                                  NaN   
                                  28441                                  NaN   
                                  28442               chronic pyelonephritis   
    
                                                      value  
    individual_pk individual_name characteristica_pk         
    1             individual1     5                     NaN  
                                  6                     NaN  
                                  33                    NaN  
                                  34                    NaN  
                                  52                    NaN  
    ...                                                 ...  
    6439          16              28328                 NaN  
                                  28439                 NaN  
                                  28440               31.00  
                                  28441                2.88  
                                  28442                 NaN  
    
    [57683 rows x 17 columns]



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
          <th>form</th>
          <th>application</th>
          <th>time</th>
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
          <th>0</th>
          <td>0</td>
          <td>PKDB00198</td>
          <td>Abernethy1982</td>
          <td>1</td>
          <td>True</td>
          <td>paracetamol_iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.65</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2</td>
          <td>PKDB00197</td>
          <td>Abernethy1982a</td>
          <td>3</td>
          <td>True</td>
          <td>paracetamol_iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>constant infusion</td>
          <td>0.0</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.65</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>2</th>
          <td>1</td>
          <td>PKDB00160</td>
          <td>Adithan1982</td>
          <td>5</td>
          <td>True</td>
          <td>paracetamol1000mg</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>1.00</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>PKDB00223</td>
          <td>Adithan1988</td>
          <td>7</td>
          <td>True</td>
          <td>paracetamol1000mg_po</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>1.00</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>4</th>
          <td>4</td>
          <td>PKDB00258</td>
          <td>AdjeponYamoah1986</td>
          <td>9</td>
          <td>True</td>
          <td>paracetamol1500mg_po</td>
          <td>oral</td>
          <td>solution</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>1.50</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
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
          <th>1204</th>
          <td>1400</td>
          <td>PKDB00315</td>
          <td>Neugebauer1988</td>
          <td>2883</td>
          <td>True</td>
          <td>Dtor40_po</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>torasemide</td>
          <td>0.04</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>1205</th>
          <td>1401</td>
          <td>PKDB00292</td>
          <td>Schwarz1993</td>
          <td>2887</td>
          <td>True</td>
          <td>Dtor_iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>torasemide</td>
          <td>0.01</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>1206</th>
          <td>1402</td>
          <td>PKDB00292</td>
          <td>Schwarz1993</td>
          <td>2888</td>
          <td>True</td>
          <td>Dtor_po</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>torasemide</td>
          <td>0.01</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>1207</th>
          <td>1403</td>
          <td>PKDB00289</td>
          <td>Spahn1990</td>
          <td>2891</td>
          <td>True</td>
          <td>Dtor</td>
          <td>iv</td>
          <td>solution</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>torasemide</td>
          <td>0.02</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
        <tr>
          <th>1208</th>
          <td>1404</td>
          <td>PKDB00275</td>
          <td>Zhang2016</td>
          <td>2893</td>
          <td>True</td>
          <td>Dtor</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
          <td>...</td>
          <td>torasemide</td>
          <td>0.01</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>None</td>
          <td>gram</td>
        </tr>
      </tbody>
    </table>
    <p>1865 rows × 24 columns</p>
    </div>




.. parsed-literal::

                     Unnamed: 0  study_sid         study_name  raw_pk  normed  \
    intervention_pk                                                             
    0                         0  PKDB00198      Abernethy1982       1    True   
    1                         2  PKDB00197     Abernethy1982a       3    True   
    2                         1  PKDB00160        Adithan1982       5    True   
    3                         3  PKDB00223        Adithan1988       7    True   
    4                         4  PKDB00258  AdjeponYamoah1986       9    True   
    ...                     ...        ...                ...     ...     ...   
    1204                   1400  PKDB00315     Neugebauer1988    2883    True   
    1205                   1401  PKDB00292        Schwarz1993    2887    True   
    1206                   1402  PKDB00292        Schwarz1993    2888    True   
    1207                   1403  PKDB00289          Spahn1990    2891    True   
    1208                   1404  PKDB00275          Zhang2016    2893    True   
    
                                     name route      form        application  \
    intervention_pk                                                            
    0                      paracetamol_iv    iv  solution        single dose   
    1                      paracetamol_iv    iv  solution  constant infusion   
    2                   paracetamol1000mg  oral    tablet        single dose   
    3                paracetamol1000mg_po  oral    tablet        single dose   
    4                paracetamol1500mg_po  oral  solution        single dose   
    ...                               ...   ...       ...                ...   
    1204                        Dtor40_po  oral    tablet        single dose   
    1205                          Dtor_iv    iv  solution        single dose   
    1206                          Dtor_po  oral    tablet        single dose   
    1207                             Dtor    iv  solution        single dose   
    1208                             Dtor  oral    tablet        single dose   
    
                     time  ...    substance value  mean median min  max  sd  se  \
    intervention_pk        ...                                                    
    0                 0.0  ...  paracetamol  0.65  None   None NaN  NaN NaN NaN   
    1                 0.0  ...  paracetamol  0.65  None   None NaN  NaN NaN NaN   
    2                 0.0  ...  paracetamol  1.00  None   None NaN  NaN NaN NaN   
    3                 0.0  ...  paracetamol  1.00  None   None NaN  NaN NaN NaN   
    4                 0.0  ...  paracetamol  1.50  None   None NaN  NaN NaN NaN   
    ...               ...  ...          ...   ...   ...    ...  ..  ...  ..  ..   
    1204              0.0  ...   torasemide  0.04  None   None NaN  NaN NaN NaN   
    1205              0.0  ...   torasemide  0.01  None   None NaN  NaN NaN NaN   
    1206              0.0  ...   torasemide  0.01  None   None NaN  NaN NaN NaN   
    1207              0.0  ...   torasemide  0.02  None   None NaN  NaN NaN NaN   
    1208              0.0  ...   torasemide  0.01  None   None NaN  NaN NaN NaN   
    
                       cv  unit  
    intervention_pk              
    0                None  gram  
    1                None  gram  
    2                None  gram  
    3                None  gram  
    4                None  gram  
    ...               ...   ...  
    1204             None  gram  
    1205             None  gram  
    1206             None  gram  
    1207             None  gram  
    1208             None  gram  
    
    [1865 rows x 24 columns]



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
          <th>21</th>
          <th>0</th>
          <th>3</th>
          <th>-1</th>
          <td>6</td>
          <td>Abernethy1982</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1.9900</td>
          <td>NaN</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>3.4700</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2.550000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>22</th>
          <th>0</th>
          <th>3</th>
          <th>-1</th>
          <td>9</td>
          <td>Abernethy1982</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>62.2000</td>
          <td>NaN</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>151.4000</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>108.500000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>23</th>
          <th>0</th>
          <th>3</th>
          <th>-1</th>
          <td>2</td>
          <td>Abernethy1982</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.5300</td>
          <td>NaN</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>1.3100</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>liter / kilogram</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.810000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>24</th>
          <th>0</th>
          <th>3</th>
          <th>-1</th>
          <td>8</td>
          <td>Abernethy1982</td>
          <td>clearance</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>19.4400</td>
          <td>NaN</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>38.7600</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>liter / hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>29.040000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>25</th>
          <th>0</th>
          <th>3</th>
          <th>-1</th>
          <td>10</td>
          <td>Abernethy1982</td>
          <td>clearance</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.1452</td>
          <td>NaN</td>
          <td>True</td>
          <td>False</td>
          <td>...</td>
          <td>NaN</td>
          <td>0.3156</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>liter / hour / kilogram</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.224400</td>
          <td>NaN</td>
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
          <th>153076</th>
          <th>1208</th>
          <th>1504</th>
          <th>-1</th>
          <td>100516</td>
          <td>Zhang2016</td>
          <td>kel</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>HPLC MS/MS</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>1 / minute</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.003658</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>153077</th>
          <th>1208</th>
          <th>1504</th>
          <th>-1</th>
          <td>100342</td>
          <td>Zhang2016</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>HPLC MS/MS</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3.157929</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>153078</th>
          <th>1208</th>
          <th>1504</th>
          <th>-1</th>
          <td>100520</td>
          <td>Zhang2016</td>
          <td>tmax</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>HPLC MS/MS</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.760958</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>153079</th>
          <th>1208</th>
          <th>1504</th>
          <th>-1</th>
          <td>100463</td>
          <td>Zhang2016</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>HPLC MS/MS</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>11.511323</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>153080</th>
          <th>1208</th>
          <th>1504</th>
          <th>-1</th>
          <td>100494</td>
          <td>Zhang2016</td>
          <td>vd_ss</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>True</td>
          <td>True</td>
          <td>...</td>
          <td>HPLC MS/MS</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>12.039979</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>72206 rows × 23 columns</p>
    </div>




.. parsed-literal::

                                                      Unnamed: 0     study_name  \
    output_pk intervention_pk group_pk individual_pk                              
    21        0               3        -1                      6  Abernethy1982   
    22        0               3        -1                      9  Abernethy1982   
    23        0               3        -1                      2  Abernethy1982   
    24        0               3        -1                      8  Abernethy1982   
    25        0               3        -1                     10  Abernethy1982   
    ...                                                      ...            ...   
    153076    1208            1504     -1                 100516      Zhang2016   
    153077    1208            1504     -1                 100342      Zhang2016   
    153078    1208            1504     -1                 100520      Zhang2016   
    153079    1208            1504     -1                 100463      Zhang2016   
    153080    1208            1504     -1                 100494      Zhang2016   
    
                                                     measurement_type  tissue  sd  \
    output_pk intervention_pk group_pk individual_pk                                
    21        0               3        -1                       thalf  plasma NaN   
    22        0               3        -1                          vd  plasma NaN   
    23        0               3        -1                          vd  plasma NaN   
    24        0               3        -1                   clearance  plasma NaN   
    25        0               3        -1                   clearance  plasma NaN   
    ...                                                           ...     ...  ..   
    153076    1208            1504     -1                         kel  plasma NaN   
    153077    1208            1504     -1                       thalf  plasma NaN   
    153078    1208            1504     -1                        tmax  plasma NaN   
    153079    1208            1504     -1                          vd  plasma NaN   
    153080    1208            1504     -1                       vd_ss  plasma NaN   
    
                                                      se      min time_unit  \
    output_pk intervention_pk group_pk individual_pk                          
    21        0               3        -1            NaN   1.9900       NaN   
    22        0               3        -1            NaN  62.2000       NaN   
    23        0               3        -1            NaN   0.5300       NaN   
    24        0               3        -1            NaN  19.4400       NaN   
    25        0               3        -1            NaN   0.1452       NaN   
    ...                                               ..      ...       ...   
    153076    1208            1504     -1            NaN      NaN       NaN   
    153077    1208            1504     -1            NaN      NaN       NaN   
    153078    1208            1504     -1            NaN      NaN       NaN   
    153079    1208            1504     -1            NaN      NaN       NaN   
    153080    1208            1504     -1            NaN      NaN       NaN   
    
                                                      normed  calculated  ...  \
    output_pk intervention_pk group_pk individual_pk                      ...   
    21        0               3        -1               True       False  ...   
    22        0               3        -1               True       False  ...   
    23        0               3        -1               True       False  ...   
    24        0               3        -1               True       False  ...   
    25        0               3        -1               True       False  ...   
    ...                                                  ...         ...  ...   
    153076    1208            1504     -1               True        True  ...   
    153077    1208            1504     -1               True        True  ...   
    153078    1208            1504     -1               True        True  ...   
    153079    1208            1504     -1               True        True  ...   
    153080    1208            1504     -1               True        True  ...   
    
                                                          method       max  \
    output_pk intervention_pk group_pk individual_pk                         
    21        0               3        -1                    NaN    3.4700   
    22        0               3        -1                    NaN  151.4000   
    23        0               3        -1                    NaN    1.3100   
    24        0               3        -1                    NaN   38.7600   
    25        0               3        -1                    NaN    0.3156   
    ...                                                      ...       ...   
    153076    1208            1504     -1             HPLC MS/MS       NaN   
    153077    1208            1504     -1             HPLC MS/MS       NaN   
    153078    1208            1504     -1             HPLC MS/MS       NaN   
    153079    1208            1504     -1             HPLC MS/MS       NaN   
    153080    1208            1504     -1             HPLC MS/MS       NaN   
    
                                                        substance label  \
    output_pk intervention_pk group_pk individual_pk                      
    21        0               3        -1             paracetamol   NaN   
    22        0               3        -1             paracetamol   NaN   
    23        0               3        -1             paracetamol   NaN   
    24        0               3        -1             paracetamol   NaN   
    25        0               3        -1             paracetamol   NaN   
    ...                                                       ...   ...   
    153076    1208            1504     -1              torasemide   NaN   
    153077    1208            1504     -1              torasemide   NaN   
    153078    1208            1504     -1              torasemide   NaN   
    153079    1208            1504     -1              torasemide   NaN   
    153080    1208            1504     -1              torasemide   NaN   
    
                                                                         unit  cv  \
    output_pk intervention_pk group_pk individual_pk                                
    21        0               3        -1                                hour NaN   
    22        0               3        -1                               liter NaN   
    23        0               3        -1                    liter / kilogram NaN   
    24        0               3        -1                        liter / hour NaN   
    25        0               3        -1             liter / hour / kilogram NaN   
    ...                                                                   ...  ..   
    153076    1208            1504     -1                          1 / minute NaN   
    153077    1208            1504     -1                                hour NaN   
    153078    1208            1504     -1                                hour NaN   
    153079    1208            1504     -1                               liter NaN   
    153080    1208            1504     -1                               liter NaN   
    
                                                     median        mean  time  \
    output_pk intervention_pk group_pk individual_pk                            
    21        0               3        -1               NaN    2.550000   NaN   
    22        0               3        -1               NaN  108.500000   NaN   
    23        0               3        -1               NaN    0.810000   NaN   
    24        0               3        -1               NaN   29.040000   NaN   
    25        0               3        -1               NaN    0.224400   NaN   
    ...                                                 ...         ...   ...   
    153076    1208            1504     -1               NaN    0.003658   NaN   
    153077    1208            1504     -1               NaN    3.157929   NaN   
    153078    1208            1504     -1               NaN    0.760958   NaN   
    153079    1208            1504     -1               NaN   11.511323   NaN   
    153080    1208            1504     -1               NaN   12.039979   NaN   
    
                                                      choice  
    output_pk intervention_pk group_pk individual_pk          
    21        0               3        -1                NaN  
    22        0               3        -1                NaN  
    23        0               3        -1                NaN  
    24        0               3        -1                NaN  
    25        0               3        -1                NaN  
    ...                                                  ...  
    153076    1208            1504     -1                NaN  
    153077    1208            1504     -1                NaN  
    153078    1208            1504     -1                NaN  
    153079    1208            1504     -1                NaN  
    153080    1208            1504     -1                NaN  
    
    [72206 rows x 23 columns]



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
          <th>3</th>
          <th>NaN</th>
          <th>-1</th>
          <th>3</th>
          <td>0</td>
          <td>PKDB00198</td>
          <td>Abernethy1982</td>
          <td>(209,  210,  211,  212,  213,  214,  215,  216...</td>
          <td>individual3</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>[0.023173645, 0.015295007000000001, 0.00840042...</td>
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
          <th>5</th>
          <th>NaN</th>
          <th>-1</th>
          <th>47</th>
          <td>5</td>
          <td>PKDB00197</td>
          <td>Abernethy1982a</td>
          <td>(397,  398,  399,  400,  401,  402,  403,  404...</td>
          <td>Individual1</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>[0.025428612000000003, 0.026277569, 0.01054481...</td>
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
          <th>7</th>
          <th>NaN</th>
          <th>11</th>
          <th>-1</th>
          <td>2</td>
          <td>PKDB00160</td>
          <td>Adithan1982</td>
          <td>(551,  552,  553,  554,  555,  556,  557,  558...</td>
          <td>saliva</td>
          <td>True</td>
          <td>saliva</td>
          <td>saliva</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>[0.0024863925, 0.010972241, 0.013427557, 0.012...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[0.0012576718, 0.003521531, 0.000987326, 0.001...</td>
          <td>[1.5995493217437526, 1.0149302053145217, 0.232...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>9</th>
          <th>NaN</th>
          <th>13</th>
          <th>-1</th>
          <td>10</td>
          <td>PKDB00223</td>
          <td>Adithan1988</td>
          <td>(777,  778,  779,  780,  781,  782)</td>
          <td>control</td>
          <td>True</td>
          <td>saliva</td>
          <td>saliva</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>[0.0, 0.0096739025, 0.006031417000000001, 0.00...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[None, 0.0010189905000000002, 0.00058879860000...</td>
          <td>[None, 0.00032223308940738075, 0.0001861944659...</td>
          <td>[None, 0.10533396424038802, 0.0976219352765694...</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>12</th>
          <th>NaN</th>
          <th>17</th>
          <th>-1</th>
          <td>9</td>
          <td>PKDB00258</td>
          <td>AdjeponYamoah1986</td>
          <td>(993,  994,  995,  996,  997,  998,  999,  100...</td>
          <td>paracetamol1500mg_po</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>[0.0036345977999999997, 0.012722702, 0.0156748...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
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
          <th>2941</th>
          <th>NaN</th>
          <th>1471</th>
          <th>-1</th>
          <td>2704</td>
          <td>PKDB00300</td>
          <td>Barr1990</td>
          <td>(145401,  145402,  145403,  145404,  145405,  ...</td>
          <td>fig3_Dtor_po_single_young</td>
          <td>True</td>
          <td>urine</td>
          <td>urine</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>[0.0037218813333333325, 0.005685071666666666, ...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>milligram / minute</td>
        </tr>
        <tr>
          <th>2970</th>
          <th>NaN</th>
          <th>1473</th>
          <th>-1</th>
          <td>2745</td>
          <td>PKDB00309</td>
          <td>Barr1990a</td>
          <td>(146277,  146278,  146279,  146280,  146281,  ...</td>
          <td>fig5_h2o_Dtor_po_10</td>
          <td>True</td>
          <td>urine</td>
          <td>urine</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>water</td>
          <td>NaN</td>
          <td>[488.58234000000004, 705.58344, 526.6213, 440....</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>milliliter / hour</td>
        </tr>
        <tr>
          <th>3035</th>
          <th>NaN</th>
          <th>1478</th>
          <th>-1</th>
          <td>2782</td>
          <td>PKDB00316</td>
          <td>Brater1993a</td>
          <td>(147192,  147193,  147194,  147195,  147196,  ...</td>
          <td>fig1_Dtor25_moderate</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>[5.622130200000001e-05, 0.0019021378000000002,...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>3041</th>
          <th>NaN</th>
          <th>1485</th>
          <th>-1</th>
          <td>2790</td>
          <td>PKDB00290</td>
          <td>Brunner1988</td>
          <td>(147915,  147916,  147917,  147918,  147919,  ...</td>
          <td>control</td>
          <td>True</td>
          <td>serum</td>
          <td>serum</td>
          <td>hplc</td>
          <td>High-performance liquid chromatography (HPLC)</td>
          <td>...</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>[8.169760999999999e-05, 0.00074270557, 0.00156...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>3256</th>
          <th>NaN</th>
          <th>1504</th>
          <th>-1</th>
          <td>2914</td>
          <td>PKDB00275</td>
          <td>Zhang2016</td>
          <td>(153013,  153014,  153015,  153016,  153017,  ...</td>
          <td>reference</td>
          <td>True</td>
          <td>plasma</td>
          <td>plasma</td>
          <td>hplc-ms-ms</td>
          <td>High performance liquid chromatography-tandem ...</td>
          <td>...</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>[0.0, 6.0163113000000016e-05, 0.00045699417000...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>[None, 6.242241700000001e-05, 0.00029877763000...</td>
          <td>[None, 1.2741922513436193e-05, 6.0987728338172...</td>
          <td>[None, 1.0375529770209861, 0.653788712446813, ...</td>
          <td>gram / liter</td>
        </tr>
      </tbody>
    </table>
    <p>423 rows × 28 columns</p>
    </div>




.. parsed-literal::

                                                      Unnamed: 0  study_sid  \
    subset_pk intervention_pk group_pk individual_pk                          
    3         NaN             -1        3                      0  PKDB00198   
    5         NaN             -1        47                     5  PKDB00197   
    7         NaN              11      -1                      2  PKDB00160   
    9         NaN              13      -1                     10  PKDB00223   
    12        NaN              17      -1                      9  PKDB00258   
    ...                                                      ...        ...   
    2941      NaN              1471    -1                   2704  PKDB00300   
    2970      NaN              1473    -1                   2745  PKDB00309   
    3035      NaN              1478    -1                   2782  PKDB00316   
    3041      NaN              1485    -1                   2790  PKDB00290   
    3256      NaN              1504    -1                   2914  PKDB00275   
    
                                                             study_name  \
    subset_pk intervention_pk group_pk individual_pk                      
    3         NaN             -1        3                 Abernethy1982   
    5         NaN             -1        47               Abernethy1982a   
    7         NaN              11      -1                   Adithan1982   
    9         NaN              13      -1                   Adithan1988   
    12        NaN              17      -1             AdjeponYamoah1986   
    ...                                                             ...   
    2941      NaN              1471    -1                      Barr1990   
    2970      NaN              1473    -1                     Barr1990a   
    3035      NaN              1478    -1                   Brater1993a   
    3041      NaN              1485    -1                   Brunner1988   
    3256      NaN              1504    -1                     Zhang2016   
    
                                                                                              output_pk  \
    subset_pk intervention_pk group_pk individual_pk                                                      
    3         NaN             -1        3             (209,  210,  211,  212,  213,  214,  215,  216...   
    5         NaN             -1        47            (397,  398,  399,  400,  401,  402,  403,  404...   
    7         NaN              11      -1             (551,  552,  553,  554,  555,  556,  557,  558...   
    9         NaN              13      -1                           (777,  778,  779,  780,  781,  782)   
    12        NaN              17      -1             (993,  994,  995,  996,  997,  998,  999,  100...   
    ...                                                                                             ...   
    2941      NaN              1471    -1             (145401,  145402,  145403,  145404,  145405,  ...   
    2970      NaN              1473    -1             (146277,  146278,  146279,  146280,  146281,  ...   
    3035      NaN              1478    -1             (147192,  147193,  147194,  147195,  147196,  ...   
    3041      NaN              1485    -1             (147915,  147916,  147917,  147918,  147919,  ...   
    3256      NaN              1504    -1             (153013,  153014,  153015,  153016,  153017,  ...   
    
                                                                    subset_name  \
    subset_pk intervention_pk group_pk individual_pk                              
    3         NaN             -1        3                           individual3   
    5         NaN             -1        47                          Individual1   
    7         NaN              11      -1                                saliva   
    9         NaN              13      -1                               control   
    12        NaN              17      -1                  paracetamol1500mg_po   
    ...                                                                     ...   
    2941      NaN              1471    -1             fig3_Dtor_po_single_young   
    2970      NaN              1473    -1                   fig5_h2o_Dtor_po_10   
    3035      NaN              1478    -1                  fig1_Dtor25_moderate   
    3041      NaN              1485    -1                               control   
    3256      NaN              1504    -1                             reference   
    
                                                      normed  tissue tissue_label  \
    subset_pk intervention_pk group_pk individual_pk                                
    3         NaN             -1        3               True  plasma       plasma   
    5         NaN             -1        47              True  plasma       plasma   
    7         NaN              11      -1               True  saliva       saliva   
    9         NaN              13      -1               True  saliva       saliva   
    12        NaN              17      -1               True  plasma       plasma   
    ...                                                  ...     ...          ...   
    2941      NaN              1471    -1               True   urine        urine   
    2970      NaN              1473    -1               True   urine        urine   
    3035      NaN              1478    -1               True  plasma       plasma   
    3041      NaN              1485    -1               True   serum        serum   
    3256      NaN              1504    -1               True  plasma       plasma   
    
                                                          method  \
    subset_pk intervention_pk group_pk individual_pk               
    3         NaN             -1        3                    NaN   
    5         NaN             -1        47                   NaN   
    7         NaN              11      -1                    NaN   
    9         NaN              13      -1                    NaN   
    12        NaN              17      -1                    NaN   
    ...                                                      ...   
    2941      NaN              1471    -1                   hplc   
    2970      NaN              1473    -1                   hplc   
    3035      NaN              1478    -1                   hplc   
    3041      NaN              1485    -1                   hplc   
    3256      NaN              1504    -1             hplc-ms-ms   
    
                                                                                           method_label  \
    subset_pk intervention_pk group_pk individual_pk                                                      
    3         NaN             -1        3                                                           NaN   
    5         NaN             -1        47                                                          NaN   
    7         NaN              11      -1                                                           NaN   
    9         NaN              13      -1                                                           NaN   
    12        NaN              17      -1                                                           NaN   
    ...                                                                                             ...   
    2941      NaN              1471    -1                 High-performance liquid chromatography (HPLC)   
    2970      NaN              1473    -1                 High-performance liquid chromatography (HPLC)   
    3035      NaN              1478    -1                 High-performance liquid chromatography (HPLC)   
    3041      NaN              1485    -1                 High-performance liquid chromatography (HPLC)   
    3256      NaN              1504    -1             High performance liquid chromatography-tandem ...   
    
                                                      ... substance_label  \
    subset_pk intervention_pk group_pk individual_pk  ...                   
    3         NaN             -1        3             ...     paracetamol   
    5         NaN             -1        47            ...     paracetamol   
    7         NaN              11      -1             ...     paracetamol   
    9         NaN              13      -1             ...     paracetamol   
    12        NaN              17      -1             ...     paracetamol   
    ...                                               ...             ...   
    2941      NaN              1471    -1             ...      torasemide   
    2970      NaN              1473    -1             ...           water   
    3035      NaN              1478    -1             ...      torasemide   
    3041      NaN              1485    -1             ...      torasemide   
    3256      NaN              1504    -1             ...      torasemide   
    
                                                                                                  value  \
    subset_pk intervention_pk group_pk individual_pk                                                      
    3         NaN             -1        3             [0.023173645, 0.015295007000000001, 0.00840042...   
    5         NaN             -1        47            [0.025428612000000003, 0.026277569, 0.01054481...   
    7         NaN              11      -1                                                           NaN   
    9         NaN              13      -1                                                           NaN   
    12        NaN              17      -1                                                           NaN   
    ...                                                                                             ...   
    2941      NaN              1471    -1                                                           NaN   
    2970      NaN              1473    -1                                                           NaN   
    3035      NaN              1478    -1                                                           NaN   
    3041      NaN              1485    -1                                                           NaN   
    3256      NaN              1504    -1                                                           NaN   
    
                                                                                                   mean  \
    subset_pk intervention_pk group_pk individual_pk                                                      
    3         NaN             -1        3                                                           NaN   
    5         NaN             -1        47                                                          NaN   
    7         NaN              11      -1             [0.0024863925, 0.010972241, 0.013427557, 0.012...   
    9         NaN              13      -1             [0.0, 0.0096739025, 0.006031417000000001, 0.00...   
    12        NaN              17      -1             [0.0036345977999999997, 0.012722702, 0.0156748...   
    ...                                                                                             ...   
    2941      NaN              1471    -1             [0.0037218813333333325, 0.005685071666666666, ...   
    2970      NaN              1473    -1             [488.58234000000004, 705.58344, 526.6213, 440....   
    3035      NaN              1478    -1             [5.622130200000001e-05, 0.0019021378000000002,...   
    3041      NaN              1485    -1             [8.169760999999999e-05, 0.00074270557, 0.00156...   
    3256      NaN              1504    -1             [0.0, 6.0163113000000016e-05, 0.00045699417000...   
    
                                                     median  min  max  \
    subset_pk intervention_pk group_pk individual_pk                    
    3         NaN             -1        3               NaN  NaN  NaN   
    5         NaN             -1        47              NaN  NaN  NaN   
    7         NaN              11      -1               NaN  NaN  NaN   
    9         NaN              13      -1               NaN  NaN  NaN   
    12        NaN              17      -1               NaN  NaN  NaN   
    ...                                                 ...  ...  ...   
    2941      NaN              1471    -1               NaN  NaN  NaN   
    2970      NaN              1473    -1               NaN  NaN  NaN   
    3035      NaN              1478    -1               NaN  NaN  NaN   
    3041      NaN              1485    -1               NaN  NaN  NaN   
    3256      NaN              1504    -1               NaN  NaN  NaN   
    
                                                                                                     sd  \
    subset_pk intervention_pk group_pk individual_pk                                                      
    3         NaN             -1        3                                                           NaN   
    5         NaN             -1        47                                                          NaN   
    7         NaN              11      -1                                                           NaN   
    9         NaN              13      -1             [None, 0.0010189905000000002, 0.00058879860000...   
    12        NaN              17      -1                                                           NaN   
    ...                                                                                             ...   
    2941      NaN              1471    -1                                                           NaN   
    2970      NaN              1473    -1                                                           NaN   
    3035      NaN              1478    -1                                                           NaN   
    3041      NaN              1485    -1                                                           NaN   
    3256      NaN              1504    -1             [None, 6.242241700000001e-05, 0.00029877763000...   
    
                                                                                                     se  \
    subset_pk intervention_pk group_pk individual_pk                                                      
    3         NaN             -1        3                                                           NaN   
    5         NaN             -1        47                                                          NaN   
    7         NaN              11      -1             [0.0012576718, 0.003521531, 0.000987326, 0.001...   
    9         NaN              13      -1             [None, 0.00032223308940738075, 0.0001861944659...   
    12        NaN              17      -1                                                           NaN   
    ...                                                                                             ...   
    2941      NaN              1471    -1                                                           NaN   
    2970      NaN              1473    -1                                                           NaN   
    3035      NaN              1478    -1                                                           NaN   
    3041      NaN              1485    -1                                                           NaN   
    3256      NaN              1504    -1             [None, 1.2741922513436193e-05, 6.0987728338172...   
    
                                                                                                     cv  \
    subset_pk intervention_pk group_pk individual_pk                                                      
    3         NaN             -1        3                                                           NaN   
    5         NaN             -1        47                                                          NaN   
    7         NaN              11      -1             [1.5995493217437526, 1.0149302053145217, 0.232...   
    9         NaN              13      -1             [None, 0.10533396424038802, 0.0976219352765694...   
    12        NaN              17      -1                                                           NaN   
    ...                                                                                             ...   
    2941      NaN              1471    -1                                                           NaN   
    2970      NaN              1473    -1                                                           NaN   
    3035      NaN              1478    -1                                                           NaN   
    3041      NaN              1485    -1                                                           NaN   
    3256      NaN              1504    -1             [None, 1.0375529770209861, 0.653788712446813, ...   
    
                                                                    unit  
    subset_pk intervention_pk group_pk individual_pk                      
    3         NaN             -1        3                   gram / liter  
    5         NaN             -1        47                  gram / liter  
    7         NaN              11      -1                   gram / liter  
    9         NaN              13      -1                   gram / liter  
    12        NaN              17      -1                   gram / liter  
    ...                                                              ...  
    2941      NaN              1471    -1             milligram / minute  
    2970      NaN              1473    -1              milliliter / hour  
    3035      NaN              1478    -1                   gram / liter  
    3041      NaN              1485    -1                   gram / liter  
    3256      NaN              1504    -1                   gram / liter  
    
    [423 rows x 28 columns]




