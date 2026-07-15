import re
import requests
from urllib.parse import urlencode

BASE_URL = "https://api.tgju.org/v1/market/indicator/summary-table-data"

_TAG_RE = re.compile(r"<[^>]+>")


def get_er_data(
    er_type,
    start=0,
    length=30,
    lang="fa",
    draw=1,
    order_dir="asc",
    search="",
    order_col="",
    from_date="",
    to_date="",
    convert_to_ad=1,
):
    """
    Fetch exchange-rate (or other market) data from the TGJU API.

    Parameters
    ----------
    er_type : str
        Endpoint name (e.g. "price_dollar_rl", "price_eur", ...)
    start : int
        Starting record.
    length : int
        Number of records to fetch.

    Returns
    -------
    dict
        JSON response from the API.
    """

    params = {
        "lang": lang,
        "draw": draw,
        "order_dir": order_dir,
    }

    # DataTables column definitions
    for i in range(8):
        params[f"columns[{i}][data]"] = i
        params[f"columns[{i}][name]"] = ""
        params[f"columns[{i}][searchable]"] = "true"
        params[f"columns[{i}][orderable]"] = "true"
        params[f"columns[{i}][search][value]"] = ""
        params[f"columns[{i}][search][regex]"] = "false"

    params.update({
        "start": start,
        "length": length,
        "search": search,
        "order_col": order_col,
        "from": from_date,
        "to": to_date,
        "convert_to_ad": convert_to_ad,
    })

    url = f"{BASE_URL}/{er_type}"

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def parse_er_data(response, columns, strip_html=True):
    """
    Convert the API response into a list of dictionaries.

    Parameters
    ----------
    response : dict
        JSON returned by get_er_data().
    columns : list[str]
        Column names.
    strip_html : bool
        Remove HTML tags from values.

    Returns
    -------
    dict
    """

    rows = []

    for row in response.get("data", []):
        if strip_html:
            row = [_TAG_RE.sub("", str(value)).strip() for value in row]

        rows.append(dict(zip(columns, row)))

    return {
        "recordsTotal": int(response.get("recordsTotal", 0)),
        "recordsFiltered": int(response.get("recordsFiltered", 0)),
        "rows": rows,
    }

def fetch_market_data(er_type, columns, **kwargs):
    """
    API -> Parsed dictionary
    """

    response = get_er_data(
        er_type=er_type,
        **kwargs
    )

    return parse_er_data(
        response,
        columns=columns,
    )