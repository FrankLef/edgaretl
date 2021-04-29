import pytest
from pathlib import Path
from datetime import datetime
import requests
from src.edgar.xbrlrss import fetch

TEST_URL = 'https://httpbin.org'  # site build explicitly for testing, nice!
WRONG_URL = TEST_URL+'X'
EDGAR_URL = 'https://www.sec.gov/Archives/edgar/monthly'
period = datetime.now()
path = Path.cwd().joinpath('data', 'xbrlrss', str(period.year))


def test_fetch_rss_head():
    assert fetch.fetch_rss(path=path, period=period,
                           url=TEST_URL, head=True) >= 200


def test_fetch_rss_head_err():
    with pytest.raises(requests.exceptions.ConnectionError):
        fetch.fetch_rss(path=path, period=period, url=WRONG_URL, head=True)
