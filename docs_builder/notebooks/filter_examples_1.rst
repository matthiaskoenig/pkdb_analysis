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


.. parsed-literal::

    INFO NumExpr defaulting to 8 threads.


.. code:: ipython3

    test_data._concise()
    print(test_data)


.. parsed-literal::

    ------------------------------
    PKData (140070362791696)
    ------------------------------
    studies           444  (  444)
    groups            932  ( 8340)
    individuals      5957  (53939)
    interventions    1209  ( 1865)
    outputs         72206  (72206)
    timecourses       423  (  423)
    ------------------------------


.. code:: ipython3

    test_data1 =  test_data.filter_study(lambda x: x["licence"] == "open")

.. code:: ipython3

    print(test_data1)


.. parsed-literal::

    ------------------------------
    PKData (140070307177168)
    ------------------------------
    studies            54  (   54)
    groups            932  ( 8340)
    individuals      5957  (53939)
    interventions    1209  ( 1865)
    outputs         72206  (72206)
    timecourses       423  (  423)
    ------------------------------


.. code:: ipython3

    list(test_data.study_sids)[:10]




.. parsed-literal::

    ['PKDB00183',
     '6743445',
     'Roberts1976',
     '3335120',
     'PKDB00137',
     'PKDB00008',
     'PKDB00281',
     'PKDB00319',
     'PKDB00254',
     '14612892']



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
    PKData (140070307177360)
    ------------------------------
    studies             1  (    1)
    groups              4  (   35)
    individuals        46  (  400)
    interventions       1  (    1)
    outputs           147  (  147)
    timecourses         1  (    1)
    ------------------------------


The PKData now only contains data for the given study_sid:

.. code:: ipython3

    print(data.study_sids)


.. parsed-literal::

    {'PKDB00198'}


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
          <th>intervention_pk</th>
          <th>Unnamed: 0</th>
          <th>study_sid</th>
          <th>study_name</th>
          <th>raw_pk</th>
          <th>normed</th>
          <th>name</th>
          <th>route</th>
          <th>form</th>
          <th>application</th>
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
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0</td>
          <td>0</td>
          <td>PKDB00198</td>
          <td>Abernethy1982</td>
          <td>1</td>
          <td>True</td>
          <td>paracetamol_iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>single dose</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.65</td>
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
    <p>1 rows × 25 columns</p>
    </div>



.. parsed-literal::

       intervention_pk  Unnamed: 0  study_sid     study_name  raw_pk  normed  \
    0                0           0  PKDB00198  Abernethy1982       1    True   
    
                 name route      form  application  ...    substance value  mean  \
    0  paracetamol_iv    iv  solution  single dose  ...  paracetamol  0.65  None   
    
      median   min   max    sd    se    cv  unit  
    0   None  None  None  None  None  None  gram  
    
    [1 rows x 25 columns]


One could also define this as a simple lambda function

.. code:: ipython3

    data = test_data.filter_intervention(lambda d: d.study_sid == "PKDB00198")
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (140070307219856)
    ------------------------------
    studies             1  (    1)
    groups              4  (   35)
    individuals        46  (  400)
    interventions       1  (    1)
    outputs           147  (  147)
    timecourses         1  (    1)
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
    PKData (140070307161296)
    ------------------------------
    studies             1  (    1)
    groups              4  (   35)
    individuals        46  (  400)
    interventions       1  (    1)
    outputs           147  (  147)
    timecourses         1  (    1)
    ------------------------------
    ------------------------------
    PKData (140070307153232)
    ------------------------------
    studies           444  (  444)
    groups            932  ( 8340)
    individuals      5957  (53939)
    interventions       1  (    1)
    outputs         72206  (72206)
    timecourses       423  (  423)
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
          <td>0</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.65</td>
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
    <p>1 rows × 24 columns</p>
    </div>




.. parsed-literal::

                     Unnamed: 0  study_sid     study_name  raw_pk  normed  \
    intervention_pk                                                         
    0                         0  PKDB00198  Abernethy1982       1    True   
    
                               name route      form  application time  ...  \
    intervention_pk                                                    ...   
    0                paracetamol_iv    iv  solution  single dose    0  ...   
    
                       substance value  mean median   min   max    sd    se    cv  \
    intervention_pk                                                                 
    0                paracetamol  0.65  None   None  None  None  None  None  None   
    
                     unit  
    intervention_pk        
    0                gram  
    
    [1 rows x 24 columns]



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
          <td>0</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.65</td>
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
    <p>1 rows × 24 columns</p>
    </div>




.. parsed-literal::

                     Unnamed: 0  study_sid     study_name  raw_pk  normed  \
    intervention_pk                                                         
    0                         0  PKDB00198  Abernethy1982       1    True   
    
                               name route      form  application time  ...  \
    intervention_pk                                                    ...   
    0                paracetamol_iv    iv  solution  single dose    0  ...   
    
                       substance value  mean median   min   max    sd    se    cv  \
    intervention_pk                                                                 
    0                paracetamol  0.65  None   None  None  None  None  None  None   
    
                     unit  
    intervention_pk        
    0                gram  
    
    [1 rows x 24 columns]



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
          <th>output_pk</th>
          <th>intervention_pk</th>
          <th>Unnamed: 0</th>
          <th>study_name</th>
          <th>measurement_type</th>
          <th>tissue</th>
          <th>sd</th>
          <th>se</th>
          <th>min</th>
          <th>group_pk</th>
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
          <td>21</td>
          <td>0</td>
          <td>6</td>
          <td>Abernethy1982</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1.9900</td>
          <td>3</td>
          <td>...</td>
          <td>3.4700</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>-1</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2.550000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>22</td>
          <td>0</td>
          <td>9</td>
          <td>Abernethy1982</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>62.2000</td>
          <td>3</td>
          <td>...</td>
          <td>151.4000</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>-1</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>108.500000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2</th>
          <td>23</td>
          <td>0</td>
          <td>2</td>
          <td>Abernethy1982</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.5300</td>
          <td>3</td>
          <td>...</td>
          <td>1.3100</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>-1</td>
          <td>liter / kilogram</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.810000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>24</td>
          <td>0</td>
          <td>8</td>
          <td>Abernethy1982</td>
          <td>clearance</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>19.4400</td>
          <td>3</td>
          <td>...</td>
          <td>38.7600</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>-1</td>
          <td>liter / hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>29.040000</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>25</td>
          <td>0</td>
          <td>10</td>
          <td>Abernethy1982</td>
          <td>clearance</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.1452</td>
          <td>3</td>
          <td>...</td>
          <td>0.3156</td>
          <td>paracetamol</td>
          <td>NaN</td>
          <td>-1</td>
          <td>liter / hour / kilogram</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.224400</td>
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
          <th>72201</th>
          <td>153076</td>
          <td>1208</td>
          <td>100516</td>
          <td>Zhang2016</td>
          <td>kel</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>...</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>-1</td>
          <td>1 / minute</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.003658</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>72202</th>
          <td>153077</td>
          <td>1208</td>
          <td>100342</td>
          <td>Zhang2016</td>
          <td>thalf</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>...</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>-1</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>3.157929</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>72203</th>
          <td>153078</td>
          <td>1208</td>
          <td>100520</td>
          <td>Zhang2016</td>
          <td>tmax</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>...</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>-1</td>
          <td>hour</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.760958</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>72204</th>
          <td>153079</td>
          <td>1208</td>
          <td>100463</td>
          <td>Zhang2016</td>
          <td>vd</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>...</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>-1</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>11.511323</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>72205</th>
          <td>153080</td>
          <td>1208</td>
          <td>100494</td>
          <td>Zhang2016</td>
          <td>vd_ss</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1504</td>
          <td>...</td>
          <td>NaN</td>
          <td>torasemide</td>
          <td>NaN</td>
          <td>-1</td>
          <td>liter</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>12.039979</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>72206 rows × 27 columns</p>
    </div>




.. parsed-literal::

           output_pk  intervention_pk  Unnamed: 0     study_name measurement_type  \
    0             21                0           6  Abernethy1982            thalf   
    1             22                0           9  Abernethy1982               vd   
    2             23                0           2  Abernethy1982               vd   
    3             24                0           8  Abernethy1982        clearance   
    4             25                0          10  Abernethy1982        clearance   
    ...          ...              ...         ...            ...              ...   
    72201     153076             1208      100516      Zhang2016              kel   
    72202     153077             1208      100342      Zhang2016            thalf   
    72203     153078             1208      100520      Zhang2016             tmax   
    72204     153079             1208      100463      Zhang2016               vd   
    72205     153080             1208      100494      Zhang2016            vd_ss   
    
           tissue  sd  se      min  group_pk  ...       max    substance  label  \
    0      plasma NaN NaN   1.9900         3  ...    3.4700  paracetamol    NaN   
    1      plasma NaN NaN  62.2000         3  ...  151.4000  paracetamol    NaN   
    2      plasma NaN NaN   0.5300         3  ...    1.3100  paracetamol    NaN   
    3      plasma NaN NaN  19.4400         3  ...   38.7600  paracetamol    NaN   
    4      plasma NaN NaN   0.1452         3  ...    0.3156  paracetamol    NaN   
    ...       ...  ..  ..      ...       ...  ...       ...          ...    ...   
    72201  plasma NaN NaN      NaN      1504  ...       NaN   torasemide    NaN   
    72202  plasma NaN NaN      NaN      1504  ...       NaN   torasemide    NaN   
    72203  plasma NaN NaN      NaN      1504  ...       NaN   torasemide    NaN   
    72204  plasma NaN NaN      NaN      1504  ...       NaN   torasemide    NaN   
    72205  plasma NaN NaN      NaN      1504  ...       NaN   torasemide    NaN   
    
           individual_pk                     unit  cv median        mean time  \
    0                 -1                     hour NaN    NaN    2.550000  NaN   
    1                 -1                    liter NaN    NaN  108.500000  NaN   
    2                 -1         liter / kilogram NaN    NaN    0.810000  NaN   
    3                 -1             liter / hour NaN    NaN   29.040000  NaN   
    4                 -1  liter / hour / kilogram NaN    NaN    0.224400  NaN   
    ...              ...                      ...  ..    ...         ...  ...   
    72201             -1               1 / minute NaN    NaN    0.003658  NaN   
    72202             -1                     hour NaN    NaN    3.157929  NaN   
    72203             -1                     hour NaN    NaN    0.760958  NaN   
    72204             -1                    liter NaN    NaN   11.511323  NaN   
    72205             -1                    liter NaN    NaN   12.039979  NaN   
    
          choice  
    0        NaN  
    1        NaN  
    2        NaN  
    3        NaN  
    4        NaN  
    ...      ...  
    72201    NaN  
    72202    NaN  
    72203    NaN  
    72204    NaN  
    72205    NaN  
    
    [72206 rows x 27 columns]



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
    PKData (140070307167120)
    ------------------------------
    studies           165  (  165)
    groups            271  ( 2774)
    individuals      1989  (20777)
    interventions     402  (  633)
    outputs         22886  (22886)
    timecourses       135  (  135)
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
          <th rowspan="5" valign="top">3</th>
          <th>5</th>
          <td>10</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>species</td>
          <td>7</td>
          <td>obese men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>2</td>
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
          <td>11</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>healthy</td>
          <td>7</td>
          <td>obese men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>2</td>
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
          <th>11</th>
          <td>12</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>obesity index</td>
          <td>7</td>
          <td>obese men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>21</td>
          <td>2</td>
          <td>NaN</td>
          <td>percent</td>
          <td>NaN</td>
          <td>133.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>12</th>
          <td>13</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>weight (categorial)</td>
          <td>7</td>
          <td>obese men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>21</td>
          <td>2</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>obese</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>18</th>
          <td>14</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>sex</td>
          <td>7</td>
          <td>obese men</td>
          <td>NaN</td>
          <td>nan</td>
          <td>7</td>
          <td>2</td>
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
          <th rowspan="5" valign="top">1433</th>
          <th>27416</th>
          <td>11419</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>age</td>
          <td>7</td>
          <td>all</td>
          <td>42.0</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
          <td>NaN</td>
          <td>year</td>
          <td>NaN</td>
          <td>26.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>30.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>27417</th>
          <td>11420</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>weight</td>
          <td>7</td>
          <td>all</td>
          <td>84.0</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
          <td>NaN</td>
          <td>kilogram</td>
          <td>NaN</td>
          <td>70.5</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>77.3</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>27418</th>
          <td>11421</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>medication</td>
          <td>7</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
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
          <th>27419</th>
          <td>11422</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>smoking</td>
          <td>7</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
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
          <th>27420</th>
          <td>11423</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>fasting (duration)</td>
          <td>7</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
          <td>NaN</td>
          <td>day</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>2774 rows × 19 columns</p>
    </div>




.. parsed-literal::

                                 Unnamed: 0          study_name  study_sid  \
    group_pk characteristica_pk                                              
    3        5                           10       Abernethy1982  PKDB00198   
             6                           11       Abernethy1982  PKDB00198   
             11                          12       Abernethy1982  PKDB00198   
             12                          13       Abernethy1982  PKDB00198   
             18                          14       Abernethy1982  PKDB00198   
    ...                                 ...                 ...        ...   
    1433     27416                    11419  TubicGrozdanis2008   18213452   
             27417                    11420  TubicGrozdanis2008   18213452   
             27418                    11421  TubicGrozdanis2008   18213452   
             27419                    11422  TubicGrozdanis2008   18213452   
             27420                    11423  TubicGrozdanis2008   18213452   
    
                                    measurement_type  group_count group_name  \
    group_pk characteristica_pk                                                
    3        5                               species            7  obese men   
             6                               healthy            7  obese men   
             11                        obesity index            7  obese men   
             12                  weight (categorial)            7  obese men   
             18                                  sex            7  obese men   
    ...                                          ...          ...        ...   
    1433     27416                               age            7        all   
             27417                            weight            7        all   
             27418                        medication            7        all   
             27419                           smoking            7        all   
             27420                fasting (duration)            7        all   
    
                                  max substance  count  group_parent_pk  sd  \
    group_pk characteristica_pk                                               
    3        5                    NaN       nan     42                2 NaN   
             6                    NaN       nan     42                2 NaN   
             11                   NaN       nan     21                2 NaN   
             12                   NaN       nan     21                2 NaN   
             18                   NaN       nan      7                2 NaN   
    ...                           ...       ...    ...              ...  ..   
    1433     27416               42.0       nan      7               -1 NaN   
             27417               84.0       nan      7               -1 NaN   
             27418                NaN       nan      7               -1 NaN   
             27419                NaN       nan      7               -1 NaN   
             27420                NaN       nan      7               -1 NaN   
    
                                     unit  se    min  cv  median  mean  \
    group_pk characteristica_pk                                          
    3        5                        NaN NaN    NaN NaN     NaN   NaN   
             6                        NaN NaN    NaN NaN     NaN   NaN   
             11                   percent NaN  133.0 NaN     NaN   NaN   
             12                       NaN NaN    NaN NaN     NaN   NaN   
             18                       NaN NaN    NaN NaN     NaN   NaN   
    ...                               ...  ..    ...  ..     ...   ...   
    1433     27416                   year NaN   26.0 NaN     NaN  30.0   
             27417               kilogram NaN   70.5 NaN     NaN  77.3   
             27418                    NaN NaN    NaN NaN     NaN   NaN   
             27419                    NaN NaN    NaN NaN     NaN   NaN   
             27420                    day NaN    NaN NaN     NaN   NaN   
    
                                       choice  value  
    group_pk characteristica_pk                       
    3        5                   homo sapiens    NaN  
             6                              Y    NaN  
             11                           NaN    NaN  
             12                         obese    NaN  
             18                             M    NaN  
    ...                                   ...    ...  
    1433     27416                        NaN    NaN  
             27417                        NaN    NaN  
             27418                          N    NaN  
             27419                          N    NaN  
             27420                        NaN    NaN  
    
    [2774 rows x 19 columns]



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
    PKData (140070305783440)
    ------------------------------
    studies           140  (  140)
    groups            202  ( 1960)
    individuals      1241  (12212)
    interventions     339  (  550)
    outputs         18013  (18013)
    timecourses       115  (  115)
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
          <th rowspan="5" valign="top">4</th>
          <th>5</th>
          <td>19</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>species</td>
          <td>14</td>
          <td>obese women</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>2</td>
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
          <td>20</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>healthy</td>
          <td>14</td>
          <td>obese women</td>
          <td>NaN</td>
          <td>nan</td>
          <td>42</td>
          <td>2</td>
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
          <th>11</th>
          <td>21</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>obesity index</td>
          <td>14</td>
          <td>obese women</td>
          <td>NaN</td>
          <td>nan</td>
          <td>21</td>
          <td>2</td>
          <td>NaN</td>
          <td>percent</td>
          <td>NaN</td>
          <td>133.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>12</th>
          <td>22</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>weight (categorial)</td>
          <td>14</td>
          <td>obese women</td>
          <td>NaN</td>
          <td>nan</td>
          <td>21</td>
          <td>2</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>obese</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>27</th>
          <td>23</td>
          <td>Abernethy1982</td>
          <td>PKDB00198</td>
          <td>sex</td>
          <td>14</td>
          <td>obese women</td>
          <td>NaN</td>
          <td>nan</td>
          <td>14</td>
          <td>2</td>
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
          <th rowspan="5" valign="top">1433</th>
          <th>27416</th>
          <td>11419</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>age</td>
          <td>7</td>
          <td>all</td>
          <td>42.0</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
          <td>NaN</td>
          <td>year</td>
          <td>NaN</td>
          <td>26.0</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>30.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>27417</th>
          <td>11420</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>weight</td>
          <td>7</td>
          <td>all</td>
          <td>84.0</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
          <td>NaN</td>
          <td>kilogram</td>
          <td>NaN</td>
          <td>70.5</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>77.3</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>27418</th>
          <td>11421</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>medication</td>
          <td>7</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
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
          <th>27419</th>
          <td>11422</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>smoking</td>
          <td>7</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
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
          <th>27420</th>
          <td>11423</td>
          <td>TubicGrozdanis2008</td>
          <td>18213452</td>
          <td>fasting (duration)</td>
          <td>7</td>
          <td>all</td>
          <td>NaN</td>
          <td>nan</td>
          <td>7</td>
          <td>-1</td>
          <td>NaN</td>
          <td>day</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>1960 rows × 19 columns</p>
    </div>



.. parsed-literal::

                                 Unnamed: 0          study_name  study_sid  \
    group_pk characteristica_pk                                              
    4        5                           19       Abernethy1982  PKDB00198   
             6                           20       Abernethy1982  PKDB00198   
             11                          21       Abernethy1982  PKDB00198   
             12                          22       Abernethy1982  PKDB00198   
             27                          23       Abernethy1982  PKDB00198   
    ...                                 ...                 ...        ...   
    1433     27416                    11419  TubicGrozdanis2008   18213452   
             27417                    11420  TubicGrozdanis2008   18213452   
             27418                    11421  TubicGrozdanis2008   18213452   
             27419                    11422  TubicGrozdanis2008   18213452   
             27420                    11423  TubicGrozdanis2008   18213452   
    
                                    measurement_type  group_count   group_name  \
    group_pk characteristica_pk                                                  
    4        5                               species           14  obese women   
             6                               healthy           14  obese women   
             11                        obesity index           14  obese women   
             12                  weight (categorial)           14  obese women   
             27                                  sex           14  obese women   
    ...                                          ...          ...          ...   
    1433     27416                               age            7          all   
             27417                            weight            7          all   
             27418                        medication            7          all   
             27419                           smoking            7          all   
             27420                fasting (duration)            7          all   
    
                                  max substance  count  group_parent_pk  sd  \
    group_pk characteristica_pk                                               
    4        5                    NaN       nan     42                2 NaN   
             6                    NaN       nan     42                2 NaN   
             11                   NaN       nan     21                2 NaN   
             12                   NaN       nan     21                2 NaN   
             27                   NaN       nan     14                2 NaN   
    ...                           ...       ...    ...              ...  ..   
    1433     27416               42.0       nan      7               -1 NaN   
             27417               84.0       nan      7               -1 NaN   
             27418                NaN       nan      7               -1 NaN   
             27419                NaN       nan      7               -1 NaN   
             27420                NaN       nan      7               -1 NaN   
    
                                     unit  se    min  cv  median  mean  \
    group_pk characteristica_pk                                          
    4        5                        NaN NaN    NaN NaN     NaN   NaN   
             6                        NaN NaN    NaN NaN     NaN   NaN   
             11                   percent NaN  133.0 NaN     NaN   NaN   
             12                       NaN NaN    NaN NaN     NaN   NaN   
             27                       NaN NaN    NaN NaN     NaN   NaN   
    ...                               ...  ..    ...  ..     ...   ...   
    1433     27416                   year NaN   26.0 NaN     NaN  30.0   
             27417               kilogram NaN   70.5 NaN     NaN  77.3   
             27418                    NaN NaN    NaN NaN     NaN   NaN   
             27419                    NaN NaN    NaN NaN     NaN   NaN   
             27420                    day NaN    NaN NaN     NaN   NaN   
    
                                       choice  value  
    group_pk characteristica_pk                       
    4        5                   homo sapiens    NaN  
             6                              Y    NaN  
             11                           NaN    NaN  
             12                         obese    NaN  
             27                             F    NaN  
    ...                                   ...    ...  
    1433     27416                        NaN    NaN  
             27417                        NaN    NaN  
             27418                          N    NaN  
             27419                          N    NaN  
             27420                        NaN    NaN  
    
    [1960 rows x 19 columns]


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
    PKData (140070305622992)
    ------------------------------
    studies           409  (  409)
    groups            760  ( 6858)
    individuals      4939  (43337)
    interventions    1088  ( 1722)
    outputs         61672  (61672)
    timecourses       384  (  384)
    ------------------------------
    ------------------------------
    PKData (140070305623696)
    ------------------------------
    studies           424  (  424)
    groups            797  ( 7111)
    individuals      5006  (43686)
    interventions    1120  ( 1762)
    outputs         63558  (63558)
    timecourses       402  (  402)
    ------------------------------
    ------------------------------
    PKData (140070307172176)
    ------------------------------
    studies           407  (  407)
    groups            744  ( 6670)
    individuals      4869  (42651)
    interventions    1081  ( 1711)
    outputs         60992  (60992)
    timecourses       384  (  384)
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
    PKData (140070306525584)
    ------------------------------
    studies            81  (   81)
    groups            136  ( 1336)
    individuals      1022  (10148)
    interventions     153  (  260)
    outputs          9864  ( 9864)
    timecourses        43  (   43)
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
    PKData (140070325904144)
    ------------------------------
    studies           311  (  311)
    groups            470  ( 4492)
    individuals       717  ( 7014)
    interventions     694  (  998)
    outputs          3324  ( 3324)
    timecourses         0  (    0)
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
    PKData (140070307222288)
    ------------------------------
    studies             3  (    3)
    groups              5  (   41)
    individuals        14  (   98)
    interventions       3  (    3)
    outputs            19  (   19)
    timecourses         0  (    0)
    ------------------------------

