.. code:: ipython3

    
    import pandas as pd
    from IPython.display import display
    
    from pkdb_analysis import PKData, PKFilter
    from pkdb_analysis.tests.constants import TEST_HDF5

Filter data
===========

A recurring task is to filter data for a certain question. E.g. to
compare two groups, or get the subset of data for all healthy smokers.

We work again with our test data set and will filter various subsets
from it.

.. code:: ipython3

    test_data = PKData.from_hdf5(TEST_HDF5)
    print(test_data)


.. parsed-literal::

    ------------------------------
    PKData (140030700226768)
    ------------------------------
    studies             4 
    groups              8  (   86)
    individuals       246  ( 3144)
    interventions      18  (   18)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
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

A first example is filtering by ``study_sid``, i.e. we only want the
subset of data from a single study. An overview over the existing study
sids in the dataset is available via

.. code:: ipython3

    test_data.study_sids




.. parsed-literal::

    {'PKDB99996', 'PKDB99997', 'PKDB99998', 'PKDB99999'}



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

    Concise DataFrames


.. parsed-literal::

    ------------------------------
    PKData (140028654470144)
    ------------------------------
    studies             1 
    groups              1  (    6)
    individuals         6  (   42)
    interventions       3  (    3)
    outputs           194  (  194)
    timecourses         4  (    4)
    ------------------------------


The PKData now only contains data for the given study\_sid:

.. code:: ipython3

    print(data.study_sids)


.. parsed-literal::

    {'PKDB99999'}


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
          <th>study_sid</th>
          <th>study_name</th>
          <th>intervention_pk</th>
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
      </thead>
      <tbody>
        <tr>
          <th>8</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>93</td>
          <td>91</td>
          <td>True</td>
          <td>po75</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
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
          <th>9</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>94</td>
          <td>92</td>
          <td>True</td>
          <td>po15</td>
          <td>oral</td>
          <td>tablet</td>
          <td>single dose</td>
          <td>0.0</td>
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
          <th>11</th>
          <td>PKDB99999</td>
          <td>Test1</td>
          <td>96</td>
          <td>95</td>
          <td>True</td>
          <td>iv</td>
          <td>iv</td>
          <td>solution</td>
          <td>single dose</td>
          <td>0.0</td>
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
      </tbody>
    </table>
    <p>3 rows × 23 columns</p>
    </div>


One could also define this as a simple lambda function

.. code:: ipython3

    data = test_data.filter_intervention(lambda d: d.study_sid == "PKDB99999")
    print(data)


.. parsed-literal::

    Concise DataFrames


.. parsed-literal::

    ------------------------------
    PKData (140028654862408)
    ------------------------------
    studies             1 
    groups              1  (    6)
    individuals         6  (   42)
    interventions       3  (    3)
    outputs           194  (  194)
    timecourses         4  (    4)
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

    Concise DataFrames


.. parsed-literal::

    ------------------------------
    PKData (140028659442464)
    ------------------------------
    studies             1 
    groups              1  (    6)
    individuals         6  (   42)
    interventions       3  (    3)
    outputs           194  (  194)
    timecourses         4  (    4)
    ------------------------------
    ------------------------------
    PKData (140028655198392)
    ------------------------------
    studies             4 
    groups              8  (   86)
    individuals       246  ( 3144)
    interventions       6  (    6)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
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
      </tbody>
    </table>
    <p>3 rows × 22 columns</p>
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
      </tbody>
    </table>
    <p>6 rows × 22 columns</p>
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
          <th>study_sid</th>
          <th>study_name</th>
          <th>output_pk</th>
          <th>intervention_pk</th>
          <th>group_pk</th>
          <th>individual_pk</th>
          <th>normed</th>
          <th>calculated</th>
          <th>tissue</th>
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
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>2510</td>
          <td>106</td>
          <td>27</td>
          <td>-1</td>
          <td>False</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>caffeine</td>
          <td>NaN</td>
          <td>0.78000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.18000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>hr</td>
        </tr>
        <tr>
          <th>1</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>2515</td>
          <td>106</td>
          <td>27</td>
          <td>-1</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>caffeine</td>
          <td>NaN</td>
          <td>4.80000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>1.10000</td>
          <td>0.27500</td>
          <td>0.229</td>
          <td>hour</td>
        </tr>
        <tr>
          <th>2</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>2519</td>
          <td>108</td>
          <td>27</td>
          <td>-1</td>
          <td>False</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>caffeine</td>
          <td>NaN</td>
          <td>4.07000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.56000</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>µg/ml</td>
        </tr>
        <tr>
          <th>3</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>2523</td>
          <td>106</td>
          <td>27</td>
          <td>-1</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>caffeine</td>
          <td>NaN</td>
          <td>0.00407</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.00056</td>
          <td>0.00014</td>
          <td>0.138</td>
          <td>gram / liter</td>
        </tr>
        <tr>
          <th>4</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>2528</td>
          <td>106</td>
          <td>27</td>
          <td>-1</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>24.0</td>
          <td>...</td>
          <td>caffeine</td>
          <td>NaN</td>
          <td>0.02970</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.00660</td>
          <td>0.00165</td>
          <td>0.222</td>
          <td>gram * hour / liter</td>
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
          <th>1101</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>2095</td>
          <td>98</td>
          <td>-1</td>
          <td>171</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.0577</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram * hour / liter</td>
        </tr>
        <tr>
          <th>1102</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>2105</td>
          <td>98</td>
          <td>-1</td>
          <td>181</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.0536</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram * hour / liter</td>
        </tr>
        <tr>
          <th>1103</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>2110</td>
          <td>98</td>
          <td>-1</td>
          <td>186</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.0414</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram * hour / liter</td>
        </tr>
        <tr>
          <th>1104</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>2111</td>
          <td>98</td>
          <td>-1</td>
          <td>187</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.0502</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram * hour / liter</td>
        </tr>
        <tr>
          <th>1105</th>
          <td>PKDB99998</td>
          <td>Test2</td>
          <td>2116</td>
          <td>98</td>
          <td>-1</td>
          <td>192</td>
          <td>True</td>
          <td>False</td>
          <td>plasma</td>
          <td>NaN</td>
          <td>...</td>
          <td>paracetamol</td>
          <td>0.0659</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>gram * hour / liter</td>
        </tr>
      </tbody>
    </table>
    <p>1106 rows × 23 columns</p>
    </div>



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

    test_data = PKData.from_hdf5(TEST_HDF5)

``f_idx`` can be a single function, or a list of functions. A list of
functions are applied successively and is equivalent to "AND logic". "OR
logic" can be directly applied on the index.

.. code:: ipython3

    healthy_nonsmoker = test_data.filter_subject(f_idx=[is_healthy, nonsmoker])
    print(healthy_nonsmoker)
    healthy_nonsmoker.groups_mi


.. parsed-literal::

    Concise DataFrames


.. parsed-literal::

    ------------------------------
    PKData (140028653461800)
    ------------------------------
    studies             4 
    groups              6  (   73)
    individuals       246  ( 3144)
    interventions       9  (    9)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
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
    <p>73 rows × 18 columns</p>
    </div>



Often attributes are mixed for groups so we have to exclude the
opposites. In the example, the group ``20`` consists of 5 smokers and 1
nonsmoker. So for a subset of the group smoking is No. We can exclude
groups via

.. code:: ipython3

    healthy_nonsmoker = test_data.filter_subject([is_healthy, nonsmoker]).exclude_subject([smoker])
    print(healthy_nonsmoker)
    display(healthy_nonsmoker.groups_mi)


.. parsed-literal::

    Concise DataFrames
    Concise DataFrames


.. parsed-literal::

    ------------------------------
    PKData (140028652166504)
    ------------------------------
    studies             2 
    groups              1  (   11)
    individuals         2  (    8)
    interventions       5  (    5)
    outputs           191  (  233)
    timecourses        12  (   18)
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
          <th rowspan="11" valign="top">27</th>
          <th>1080</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
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
          <th>1081</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
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
          <th>1082</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
          <td>sex</td>
          <td>M</td>
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
          <th>1083</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
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
          <th>1084</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
          <td>abstinence</td>
          <td>None</td>
          <td>methylxanthine</td>
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
          <th>1085</th>
          <td>PKDB99996</td>
          <td>Test4</td>
          <td>all</td>
          <td>16</td>
          <td>-1</td>
          <td>16</td>
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
    </div>


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

    Concise DataFrames
    Concise DataFrames
    Concise DataFrames
    Concise DataFrames


.. parsed-literal::

    ------------------------------
    PKData (140028650634712)
    ------------------------------
    studies             4 
    groups              6  (   73)
    individuals       246  ( 3144)
    interventions       9  (    9)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
    ------------------------------
    ------------------------------
    PKData (140028653047592)
    ------------------------------
    studies             4 
    groups              6  (   73)
    individuals       246  ( 3144)
    interventions       9  (    9)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
    ------------------------------
    ------------------------------
    PKData (140028652099288)
    ------------------------------
    studies             4 
    groups              6  (   73)
    individuals       246  ( 3144)
    interventions       9  (    9)
    outputs          1064  ( 1106)
    timecourses        40  (   46)
    ------------------------------


3 Query interventions
---------------------

3.1 Get outputs/timecourses for intervention with substance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

intervention with measurement\_type "dosing" and substance "caffeine"

.. code:: ipython3

    def dosing_and_caffeine(d):
        return ((d["measurement_type"]=="dosing") & (d["substance"]=="caffeine"))

3.2 Get outputs/timecourses where multiple interventions were given
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    test_data = PKData.from_hdf5(TEST_HDF5)

.. code:: ipython3

    caffeine_data = test_data.filter_intervention(dosing_and_caffeine)


.. parsed-literal::

    Concise DataFrames


.. code:: ipython3

    print(caffeine_data)


.. parsed-literal::

    ------------------------------
    PKData (140028652099904)
    ------------------------------
    studies             1 
    groups              1  (   11)
    individuals         0  (    0)
    interventions       1  (    1)
    outputs            71  (   71)
    timecourses        12  (   12)
    ------------------------------


4 Query outputs/timecourses
---------------------------

4.1 query by measurement\_type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

filter all outputs with measurement\_type auc\_inf

.. code:: ipython3

    def is_auc_inf(d):
        return (d["measurement_type"]=="auc_inf")  
    
    test_data = PKData.from_hdf5(TEST_HDF5)
    
    test_data = test_data.filter_output(is_auc_inf).delete_timecourses()
    print(test_data)


.. parsed-literal::

    Concise DataFrames
    Concise DataFrames


.. parsed-literal::

    ------------------------------
    PKData (140028648894360)
    ------------------------------
    studies             3 
    groups              6  (   73)
    individuals       118  ( 1534)
    interventions       5  (    5)
    outputs           276  (  278)
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

    test_data = PKData.from_hdf5(TEST_HDF5)
    phenotyped_data = test_data.filter_output(is_cyp2d6_phenotyped)


.. parsed-literal::

    Concise DataFrames


.. code:: ipython3

    test_data.groups = phenotyped_data.groups
    test_data.individuals = phenotyped_data.individuals
    test_data = test_data.filter_output(codeine_clearance).delete_timecourses()


.. parsed-literal::

    Concise DataFrames
    Concise DataFrames


.. code:: ipython3

    print(test_data)


.. parsed-literal::

    ------------------------------
    PKData (140028655198336)
    ------------------------------
    studies             0 
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    ------------------------------


6 Pitfalls
----------

.. code:: ipython3

    test_data = PKData.from_hdf5(TEST_HDF5)
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



.. parsed-literal::

    Concise DataFrames
    Concise DataFrames
    Concise DataFrames
    Concise DataFrames


