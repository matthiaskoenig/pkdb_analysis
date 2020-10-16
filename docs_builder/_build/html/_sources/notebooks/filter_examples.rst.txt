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

    INFO NumExpr defaulting to 8 threads.


.. parsed-literal::

    ------------------------------
    PKData (140073344574672)
    ------------------------------
    studies           505  (  505)
    groups           1456  (11993)
    individuals      6395  (57683)
    interventions    1209  ( 1865)
    outputs         72206  (72206)
    timecourses       423  (  423)
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

    {'10381807',
     '10412886',
     '10444424',
     '10460065',
     '10634135',
     '10741630',
     '10934672',
     '10976543',
     '11061578',
     '11112089',
     '11180018',
     '11259986',
     '1133173',
     '11361054',
     '11497338',
     '1154379',
     '11709322',
     '11736870',
     '11753267',
     '11872673',
     '11986393',
     '12189441',
     '12200754',
     '12236852',
     '1246330',
     '12723464',
     '12784317',
     '13053413',
     '14612892',
     '14691614',
     '1484193',
     '1488408',
     '14979606',
     '14982753',
     '15206993',
     '15317833',
     '1551497',
     '15518608',
     '1577043',
     '1613123',
     '16158445',
     '1623898',
     '16261361',
     '170711',
     '17108811',
     '1732127',
     '17541571',
     '18213452',
     '1895958',
     '19094067',
     '20853468',
     '2121568',
     '21252240',
     '2198434',
     '22673010',
     '23469684',
     '24517114',
     '25323804',
     '2584298',
     '25853045',
     '264686',
     '28063968',
     '2816559',
     '28350522',
     '2857025',
     '2902373',
     '2921843',
     '29230348',
     '29403866',
     '30171779',
     '30729119',
     '3113968',
     '32071850',
     '3335120',
     '3356089',
     '3356110',
     '3437070',
     '3514335',
     '3519643',
     '3522621',
     '3546378',
     '3604267',
     '3722329',
     '3741728',
     '3741730',
     '3816112',
     '385271',
     '3971846',
     '4027137',
     '4079279',
     '4127645',
     '4430704',
     '4552828',
     '4850385',
     '4856884',
     '4942784',
     '5957477',
     '6041196',
     '6135578',
     '6141519',
     '6368593',
     '659633',
     '6734698',
     '6743445',
     '6883911',
     '7009366',
     '7094509',
     '7742721',
     '7898078',
     '7983238',
     '8138261',
     '8149872',
     '8375123',
     '8423228',
     '8445222',
     '856672',
     '8568017',
     '8622603',
     '8690818',
     '8823235',
     '8852486',
     '8877677',
     '8988072',
     '908472',
     '9272591',
     '9542477',
     '9696456',
     '9725479',
     '9728898',
     '9792543',
     '9834039',
     '9920147',
     'Andersen1999',
     'Arold2005',
     'Becker1984',
     'Bochner1999',
     'Borin1989',
     'Branch1976',
     'Burns1991',
     'Chen1989ThesisChapter4',
     'Chijiiwa2000',
     'Cysneiros2007',
     'DOnofrio2014',
     'Gadano1997',
     'Geneve1990',
     'Grundmann1992',
     'Hasselstrom1993',
     'He2017',
     'Huet1980',
     'Itoh2001',
     'Kamimori1999',
     'Kawasaki1988',
     'Kearns1990',
     'Kinzler2019',
     'Klockowski1990',
     'Lane1992',
     'Leevy1962',
     'Ma2008',
     'Martin1975',
     'Meijer1988',
     'Niemann2000',
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
     'PKDB00020',
     'PKDB00021',
     'PKDB00022',
     'PKDB00023',
     'PKDB00024',
     'PKDB00025',
     'PKDB00026',
     'PKDB00027',
     'PKDB00028',
     'PKDB00029',
     'PKDB00030',
     'PKDB00031',
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
     'PKDB00066',
     'PKDB00067',
     'PKDB00068',
     'PKDB00069',
     'PKDB00070',
     'PKDB00071',
     'PKDB00072',
     'PKDB00073',
     'PKDB00074',
     'PKDB00075',
     'PKDB00076',
     'PKDB00077',
     'PKDB00078',
     'PKDB00079',
     'PKDB00080',
     'PKDB00081',
     'PKDB00082',
     'PKDB00083',
     'PKDB00084',
     'PKDB00085',
     'PKDB00086',
     'PKDB00087',
     'PKDB00089',
     'PKDB00090',
     'PKDB00091',
     'PKDB00092',
     'PKDB00093',
     'PKDB00094',
     'PKDB00095',
     'PKDB00096',
     'PKDB00097',
     'PKDB00098',
     'PKDB00100',
     'PKDB00101',
     'PKDB00102',
     'PKDB00103',
     'PKDB00104',
     'PKDB00105',
     'PKDB00106',
     'PKDB00107',
     'PKDB00108',
     'PKDB00109',
     'PKDB00110',
     'PKDB00111',
     'PKDB00112',
     'PKDB00113',
     'PKDB00114',
     'PKDB00115',
     'PKDB00116',
     'PKDB00117',
     'PKDB00118',
     'PKDB00119',
     'PKDB00120',
     'PKDB00121',
     'PKDB00122',
     'PKDB00123',
     'PKDB00124',
     'PKDB00125',
     'PKDB00126',
     'PKDB00127',
     'PKDB00128',
     'PKDB00129',
     'PKDB00130',
     'PKDB00131',
     'PKDB00132',
     'PKDB00133',
     'PKDB00134',
     'PKDB00135',
     'PKDB00136',
     'PKDB00137',
     'PKDB00138',
     'PKDB00139',
     'PKDB00140',
     'PKDB00141',
     'PKDB00142',
     'PKDB00143',
     'PKDB00144',
     'PKDB00145',
     'PKDB00146',
     'PKDB00147',
     'PKDB00148',
     'PKDB00149',
     'PKDB00150',
     'PKDB00151',
     'PKDB00152',
     'PKDB00153',
     'PKDB00154',
     'PKDB00155',
     'PKDB00156',
     'PKDB00157',
     'PKDB00158',
     'PKDB00159',
     'PKDB00160',
     'PKDB00161',
     'PKDB00162',
     'PKDB00163',
     'PKDB00164',
     'PKDB00165',
     'PKDB00166',
     'PKDB00167',
     'PKDB00168',
     'PKDB00169',
     'PKDB00170',
     'PKDB00171',
     'PKDB00172',
     'PKDB00174',
     'PKDB00175',
     'PKDB00176',
     'PKDB00177',
     'PKDB00178',
     'PKDB00179',
     'PKDB00180',
     'PKDB00181',
     'PKDB00182',
     'PKDB00183',
     'PKDB00184',
     'PKDB00185',
     'PKDB00186',
     'PKDB00188',
     'PKDB00189',
     'PKDB00190',
     'PKDB00191',
     'PKDB00192',
     'PKDB00193',
     'PKDB00194',
     'PKDB00195',
     'PKDB00196',
     'PKDB00197',
     'PKDB00198',
     'PKDB00199',
     'PKDB00200',
     'PKDB00201',
     'PKDB00202',
     'PKDB00203',
     'PKDB00204',
     'PKDB00205',
     'PKDB00206',
     'PKDB00207',
     'PKDB00208',
     'PKDB00209',
     'PKDB00210',
     'PKDB00211',
     'PKDB00212',
     'PKDB00213',
     'PKDB00214',
     'PKDB00215',
     'PKDB00216',
     'PKDB00217',
     'PKDB00218',
     'PKDB00219',
     'PKDB00220',
     'PKDB00221',
     'PKDB00222',
     'PKDB00223',
     'PKDB00224',
     'PKDB00225',
     'PKDB00226',
     'PKDB00227',
     'PKDB00228',
     'PKDB00243',
     'PKDB00244',
     'PKDB00245',
     'PKDB00246',
     'PKDB00247',
     'PKDB00248',
     'PKDB00249',
     'PKDB00250',
     'PKDB00251',
     'PKDB00252',
     'PKDB00253',
     'PKDB00254',
     'PKDB00255',
     'PKDB00256',
     'PKDB00257',
     'PKDB00258',
     'PKDB00259',
     'PKDB00260',
     'PKDB00261',
     'PKDB00262',
     'PKDB00263',
     'PKDB00264',
     'PKDB00265',
     'PKDB00266',
     'PKDB00268',
     'PKDB00269',
     'PKDB00270',
     'PKDB00271',
     'PKDB00272',
     'PKDB00273',
     'PKDB00274',
     'PKDB00275',
     'PKDB00276',
     'PKDB00277',
     'PKDB00278',
     'PKDB00279',
     'PKDB00280',
     'PKDB00281',
     'PKDB00282',
     'PKDB00283',
     'PKDB00284',
     'PKDB00285',
     'PKDB00286',
     'PKDB00287',
     'PKDB00288',
     'PKDB00289',
     'PKDB00290',
     'PKDB00291',
     'PKDB00292',
     'PKDB00293',
     'PKDB00294',
     'PKDB00295',
     'PKDB00296',
     'PKDB00297',
     'PKDB00298',
     'PKDB00299',
     'PKDB00300',
     'PKDB00301',
     'PKDB00302',
     'PKDB00303',
     'PKDB00304',
     'PKDB00305',
     'PKDB00306',
     'PKDB00307',
     'PKDB00308',
     'PKDB00309',
     'PKDB00310',
     'PKDB00311',
     'PKDB00312',
     'PKDB00313',
     'PKDB00314',
     'PKDB00315',
     'PKDB00316',
     'PKDB00317',
     'PKDB00318',
     'PKDB00319',
     'PKDB00320',
     'PKDB00321',
     'PKDB00322',
     'PKDB00323',
     'PKDB00324',
     'PKDB00325',
     'PKDB00326',
     'PKDB00327',
     'PKDB00328',
     'PKDB00329',
     'PKDB00330',
     'PKDB00331',
     'PKDB00332',
     'PKDB00333',
     'PKDB00334',
     'PKDB00335',
     'PKDB00336',
     'PKDB00337',
     'PKDB00338',
     'PKDB00339',
     'PKDB00341',
     'Roberts1976',
     'Scott1989',
     'Seideman1980',
     'Tanaka1993',
     'Trang1985',
     'Walker1990',
     'Wood1979',
     'Yiamouyiannis1994'}



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
    PKData (140073385145552)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    ------------------------------


The PKData now only contains data for the given study_sid:

.. code:: ipython3

    print(data.study_sids)


.. parsed-literal::

    set()


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
      </tbody>
    </table>
    <p>0 rows × 25 columns</p>
    </div>



.. parsed-literal::

    Empty DataFrame
    Columns: [intervention_pk, Unnamed: 0, study_sid, study_name, raw_pk, normed, name, route, form, application, time, time_end, time_unit, measurement_type, choice, substance, value, mean, median, min, max, sd, se, cv, unit]
    Index: []
    
    [0 rows x 25 columns]


One could also define this as a simple lambda function

.. code:: ipython3

    data = test_data.filter_intervention(lambda d: d.study_sid == "PKDB99999")
    print(data)


.. parsed-literal::

    ------------------------------
    PKData (140074325498576)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
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
    PKData (140073376541712)
    ------------------------------
    studies             0  (    0)
    groups              0  (    0)
    individuals         0  (    0)
    interventions       0  (    0)
    outputs             0  (    0)
    timecourses         0  (    0)
    ------------------------------
    ------------------------------
    PKData (140073376537296)
    ------------------------------
    studies           505  (  505)
    groups           1456  (11993)
    individuals      6395  (57683)
    interventions       0  (    0)
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
    PKData (140073382514896)
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
    PKData (140073376596112)
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
    PKData (140073376598800)
    ------------------------------
    studies           409  (  409)
    groups            760  ( 6858)
    individuals      4939  (43337)
    interventions    1088  ( 1722)
    outputs         61672  (61672)
    timecourses       384  (  384)
    ------------------------------
    ------------------------------
    PKData (140073396104400)
    ------------------------------
    studies           424  (  424)
    groups            797  ( 7111)
    individuals      5006  (43686)
    interventions    1120  ( 1762)
    outputs         63558  (63558)
    timecourses       402  (  402)
    ------------------------------
    ------------------------------
    PKData (140073396101584)
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
    PKData (140073376303632)
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
    PKData (140073378072784)
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
    PKData (140073346167888)
    ------------------------------
    studies             3  (    3)
    groups              5  (   41)
    individuals        14  (   98)
    interventions       3  (    3)
    outputs            19  (   19)
    timecourses         0  (    0)
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


