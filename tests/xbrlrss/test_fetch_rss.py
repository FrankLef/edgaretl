import pytest
from pathlib import Path
from datetime import datetime
import responses
import requests
from src.edgar.xbrlrss import fetch

TEST_URL = 'https://httpbin.org'  # site build explicitly for testing, nice!
WRONG_URL = "http://WRONG_URL"
EDGAR_URL = 'http://www.sec.gov/Archives/edgar/monthly'

a_period = datetime(2020, 1, 1)
a_dir = Path.cwd().joinpath('data', 'xbrlrss', str(a_period.year))
a_file = "-".join(('xbrlrss', str(a_period.year),
                  str(a_period.month).zfill(2))) + '.xml'
a_path = a_dir.joinpath(a_file)
a_url = EDGAR_URL
a_url = requests.compat.urljoin(a_url, a_file)


# def test_fetch_rss_head():
#     assert fetch.fetch_rss(path=a_dir, period=a_period,
#                            url=EDGAR_URL, head=True) in {200, 301, 403}


def test_fetch_rss_head_err():
    with pytest.raises(requests.exceptions.ConnectionError):
        fetch.fetch_rss(path=a_dir, period=a_period, url=WRONG_URL, head=True)


# NOTE: Do this only when necessry
# def test_fetch_rss():
#     assert fetch.fetch_rss(path=a_dir, period=a_period,
#                            url=EDGAR_URL) in {200, 403}
