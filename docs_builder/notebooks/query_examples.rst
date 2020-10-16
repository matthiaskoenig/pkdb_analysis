.. code:: ipython3

    
    import pandas as pd
    from IPython.display import display

Query PK-DB
===========

-  how to set the endpoint for queries
-  how to query data from PKDB

To query the complete database content we can do

.. code:: ipython3

    from pkdb_analysis import PKDB, PKData, PKFilter

.. code:: ipython3

    data = PKDB.query()
    print(data)


.. parsed-literal::

    INFO *** Querying data ***
    INFO http://0.0.0.0:8000/api/v1/pkdata/studies/?format=json&page_size=2000
    INFO http://0.0.0.0:8000/api/v1/pkdata/studies/?format=json&page_size=2000&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/interventions/?format=json&page_size=2000&normed=true
    INFO http://0.0.0.0:8000/api/v1/pkdata/interventions/?format=json&page_size=2000&normed=true&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=2
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=3
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=4
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=5
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=6
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=7
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=8
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=9
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=10
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=11
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=12
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=13
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=14
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=15
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=16
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=17
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=18
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=19
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=20
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=21
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=22
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=23
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=24
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=25
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=26
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=27
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=28
    INFO http://0.0.0.0:8000/api/v1/pkdata/individuals/?format=json&page_size=2000&page=29
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&page=2
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&page=3
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&page=4
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&page=5
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&page=6
    INFO http://0.0.0.0:8000/api/v1/pkdata/groups/?format=json&page_size=2000&page=7
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=2
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=3
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=4
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=5
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=6
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=7
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=8
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=9
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=10
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=11
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=12
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=13
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=14
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=15
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=16
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=17
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=18
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=19
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=20
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=21
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=22
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=23
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=24
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=25
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=26
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=27
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=28
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=29
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=30
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=31
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=32
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=33
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=34
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=35
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=36
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=37
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=38
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=39
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=40
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=41
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=42
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=43
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=44
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=45
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=46
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=47
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=48
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=49
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=50
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=51
    INFO http://0.0.0.0:8000/api/v1/pkdata/outputs/?format=json&page_size=2000&normed=true&page=52
    INFO http://0.0.0.0:8000/api/v1/pkdata/timecourses/?format=json&page_size=2000
    INFO http://0.0.0.0:8000/api/v1/pkdata/timecourses/?format=json&page_size=2000&page=1
    INFO http://0.0.0.0:8000/api/v1/pkdata/timecourses/?format=json&page_size=2000&page=2
    INFO NumExpr defaulting to 8 threads.


.. parsed-literal::

    ------------------------------
    PKData (140114386249680)
    ------------------------------
    studies           520  (  520)
    groups           1490  (12276)
    individuals      6424  (57787)
    interventions    1230  ( 1888)
    outputs         73638  (73638)
    timecourses       879  (  879)
    ------------------------------


