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


def read_study_identifiers(path: Path) -> pd.DataFrame:
    """Reads information from study_identifiers.json."""
    with open(path, 'r') as f:
        sids_json = json.load(f)

    # sid, substance, name, data,
    entries = []
    columns = "sid", "date", "name", "substance"
    for sid, data in sids_json.items():
        entry = {
            "sid": sid,
            "date": datetime.strptime(data[1], '%Y-%m-%d'),
            "substance": data[0].split("/")[0],   # possible curation errors in here
            "fullname": data[0],
        }
        entries.append(entry)

    return pd.DataFrame(entries, columns=columns)


def query_studies(api_base, username, password):
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
        json_data = response.json()
        data += response.json()["data"]["data"]

    return data


if __name__ == "__main__":

    update_data = 1  # load data from database
    data_path = Path("report_data.tsv")

    if update_data:
        # 1. read study identifiers for timeline
        path_sids = Path('study_identifiers.json')
        sids_df = read_study_identifiers(path_sids)
        # print(sids_df.head())

        # 2. read study information from database via endpoints
        from pkdb_analysis.envs import API_URL, USER, PASSWORD
        data = query_studies(api_base=API_URL, username=USER, password=PASSWORD)
        # pprint(data)

        # 3. create DataFrames for plotting
        entries = []
        columns = ["sid", "name", "licence", "access", "curators",
                   "group_count", "individual_count", "intervention_count", "output_count", "timecourse_count"]
        for study in data:
            entry = {}
            for key in columns:
                entry[key] = study[key]

            entry["curators"] = [item['username'] for item in entry["curators"]]
            entries.append(entry)

        study_df = pd.DataFrame(entries, columns=columns)
        # print(study_df.head())

        # merge data frames
        df = pd.merge(sids_df, study_df, on='sid')
        df.to_csv(data_path, sep="\t", index=False)
    else:
        df = pd.read_csv(data_path, sep="\t")

    print(df.head())

    # 4. altair plot
    import altair as alt
    from vega_datasets import data

    source = data.unemployment_across_industries.url

    chart = alt.Chart(source).mark_area().encode(
        alt.X('yearmonth(date):T',
              axis=alt.Axis(format='%Y', domain=False, tickSize=0)
              ),
        alt.Y('sum(count):Q', stack='center', axis=None),
        alt.Color('series:N',
                  scale=alt.Scale(scheme='category20b')
                  )
    )
    chart.interactive()

    # json serialization
    chart.save('chart.json')

    # 5. include vega lite plot in vue.js
    # see https://nesterone.github.io/vue-vega
    # better use vega and vega-lite libaries directly
    pass



