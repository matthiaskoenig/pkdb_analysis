"""
Create report over data base content over time.
"""
from pkdb_analysis.query import PKDB
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from urllib import parse as urlparse
import requests
import logging
from pprint import pprint


logger = logging.getLogger(__name__)


def query_statistics_df(api_base, username, password):
    url = urlparse.urljoin(api_base, "/api/v1/statistics/?format=json")

    headers = PKDB.get_authentication_headers(api_base=api_base,
                                              username=username,
                                              password=password)
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        json_data = response.json()

        entries = []
        columns = ["sid", "date", "name", "creator", "licence", "access",
                   "group_count", "individual_count", "intervention_count",
                   "output_count", "timecourse_count"]
        for study in json_data['studies']:
            entry = {}
            for key in columns:
                entry[key] = study[key]

            entries.append(entry)

        return pd.DataFrame(entries, columns=columns)

    except requests.exceptions.HTTPError as err:
        raise err


def query_studies_df(api_base, username, password):
    url = urlparse.urljoin(api_base, "/api/v1/studies/?format=json")

    headers = PKDB.get_authentication_headers(api_base=api_base, username=username, password=password)
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        num_pages = response.json()["last_page"]

    except requests.exceptions.HTTPError as err:
        raise err

    data = []
    for page in range(1, num_pages + 1):
        url_current = url + f"&page={page}"
        logger.warning(url_current)

        response = requests.get(url_current, headers=headers)

        data += response.json()["data"]["data"]

    # create DataFrames for plotting
    entries = []
    columns = ["sid", "date", "name", "licence", "access",
               "group_count", "individual_count", "intervention_count",
               "output_count", "timecourse_count"]
    for study in data:
        entry = {}
        for key in columns:
            entry[key] = study[key]

        # entry["curators"] = [item['username'] for item in entry["curators"]]
        entries.append(entry)

    return pd.DataFrame(entries, columns=columns)


if __name__ == "__main__":

    update_data = 1  # load data from database
    data_path = Path("report_data.tsv")
    if update_data:

        # 1. read study information from database via endpoints

        API_BASE = "http://0.0.0.0:8000/"
        USER = "admin"
        PASSWORD = "pkdb_admin"

        # df = query_studies_df(api_base=API_BASE, username=USER, password=PASSWORD)
        df = query_statistics_df(api_base=API_BASE, username=USER,
                              password=PASSWORD)


        df.to_csv(data_path, sep="\t", index=False)

    else:
        df = pd.read_csv(data_path, sep="\t")

    print(df.head())



