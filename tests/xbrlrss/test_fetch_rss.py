import pytest
from pathlib import Path
from datetime import datetime
import responses
import requests
from src.edgar import registry
from src.edgar.xbrlrss import write
from src.edgar.xbrlrss import fetch

prefix = registry.rss()  # we use the prefix also for the subdirectory, discretionary
test_url = str(registry.test_url())
egdar_url = registry.edgar_url(0)
month_url = registry.edgar_url(1)
oldmonth_url = registry.edgar_url(2)

a_period = datetime(2020, 1, 1)
# we use 'xbrlrss' for the subdirectory
a_dir = Path.cwd().joinpath('data', 'xbrlrss', str(a_period.year))
a_file = write.write_fn(period=a_period)
a_path = a_dir.joinpath(a_file)
a_url = month_url
a_url_fn = a_url + r"/" + a_file


def test_fetch_rss_err_dir():
    with pytest.raises(FileNotFoundError):
        assert fetch.fetch_rss(url=test_url, path=Path.cwd().joinpath('WRONG'))


def test_fetch_rss_head_oldmonth():
    assert fetch.fetch_rss(url=oldmonth_url, path=a_dir,
                           period=a_period, head=True) in {301, 403}


def test_fetch_rss_head_month():
    assert fetch.fetch_rss(url=month_url, path=a_dir,
                           period=a_period, head=True) in {200, 403}


# only done from time to time as it takes resources
# def test_fetch_rss():
#     assert fetch.fetch_rss(url=month_url, path=a_dir,
#                            period=a_period, overwrite=True) in {200, 403}


def test_fetch_rss_err_exists():
    with pytest.raises(FileExistsError):
        assert fetch.fetch_rss(url=month_url, path=a_dir,
                               period=a_period, overwrite=False)
