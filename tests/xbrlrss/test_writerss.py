import pytest
from pathlib import Path
from datetime import datetime
import requests
from src.edgar.xbrlrss import write

EDGAR_URL = 'https://www.sec.gov/Archives/edgar/monthly'


def test_write_url():
    """Test write_url() with defaults values
    """
    url = EDGAR_URL
    now = datetime.now()
    doc = "-".join(('xbrlrss', str(now.year), str(now.month).zfill(2)))
    target = '/'.join((url, doc)) + '.xml'
    assert write.write_url() == target


@pytest.mark.parametrize('per', [datetime(2005, 3, 31), datetime(2100, 1, 1)])
def test_write_url_err_period(per):
    """Test period validation
    """
    with pytest.raises(ValueError):
        write.write_url(period=per)


def test_write_url_err_url():
    """Test write_url() with invalid url
    """
    url = '/'.join(('https:/', 'url', 'invalid'))
    with pytest.raises(requests.exceptions.ConnectionError):
        write.write_url(url=url, check=True)


def test_write_dir():
    """Test write_dir with default values.
    """
    year = datetime.now().year
    target = Path.cwd()
    target = target.joinpath('data', 'xbrlrss', str(year))
    assert write.write_dir(year=year) == target


def test_write_fn():
    """Test write_fn with default values
    """
    now = datetime.now()
    a_dir = write.write_dir(year=now.year)
    a_file = 'xbrlrss' + '_'
    a_file += '-'.join((str(now.year), str(now.month).zfill(2))) + '.xml'
    target = a_dir.joinpath(a_file)
    assert write.write_fn(dir=a_dir) == target


def test_write_fn_err_dir():
    """Test write-fn error: the dir arg must be a pathlib.Path object
    """
    with pytest.raises(ValueError):
        write.write_fn(dir='wrong, must be a pathlib.Path object')


def test_write_fn_err_check():
    with pytest.raises(ValueError):
        write.write_fn(dir=Path.cwd().joinpath("WONG"), check=True)
