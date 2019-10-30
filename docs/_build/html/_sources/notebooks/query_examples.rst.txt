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

    *** Querying data ***
    http://0.0.0.0:8000/api/v1/interventions_elastic/?format=json&page_size=2000&normed=true
    http://0.0.0.0:8000/api/v1/interventions_elastic/?format=json&page_size=2000&normed=true&page=1
    http://0.0.0.0:8000/api/v1/characteristica_individuals/?format=json&page_size=2000
    http://0.0.0.0:8000/api/v1/characteristica_individuals/?format=json&page_size=2000&page=1
    http://0.0.0.0:8000/api/v1/characteristica_individuals/?format=json&page_size=2000&page=2
    http://0.0.0.0:8000/api/v1/characteristica_groups/?format=json&page_size=2000
    http://0.0.0.0:8000/api/v1/characteristica_groups/?format=json&page_size=2000&page=1
    http://0.0.0.0:8000/api/v1/output_intervention/?format=json&page_size=2000&normed=true
    http://0.0.0.0:8000/api/v1/output_intervention/?format=json&page_size=2000&normed=true&page=1
    http://0.0.0.0:8000/api/v1/timecourse_intervention/?format=json&page_size=2000&normed=true
    http://0.0.0.0:8000/api/v1/timecourse_intervention/?format=json&page_size=2000&normed=true&page=1


.. parsed-literal::

    ------------------------------
    PKData (140034939923480)
    ------------------------------
    studies             4 
    groups              8  (   86)
    individuals       246  ( 3144)
    interventions       9  (    9)
    outputs           599  (  628)
    timecourses        20  (   23)
    ------------------------------


