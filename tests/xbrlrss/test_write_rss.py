import pytest
from pathlib import Path
from datetime import datetime
import requests
from src.edgar import registry
from src.edgar.xbrlrss import write


@pytest.fixture
def prefix():
    return registry.rss()


@pytest.fixture
def test_url():
    return registry.test_url()


def test_write_fn(prefix):
    """write_fn()
    """
    period = datetime.now()
    target = '-'.join((prefix, str(period.year),
                       str(period.month).zfill(2)))
    target += '.xml'
    assert write.write_fn(period=period) == target
    # verify that the constant in the registry is used at the beginning
    assert write.write_fn(period=period).find(prefix) == 0


@pytest.mark.parametrize('per', [datetime(2005, 3, 31), datetime(2100, 1, 1)])
def test_write_fn_err_period(per):
    """write_fn() with invalid periods
    """
    with pytest.raises(ValueError):
        write.write_fn(period=per)


def test_write_url(test_url):
    """write_url()
    """
    url = test_url
    fn = 'test.xml'
    target = url + r"/" + fn
    assert write.write_url(url=url, fn=fn) == target


def test_write_url_err_url():
    """write_url() with invalid url
    """
    fn = 'test.xml'
    url = '/'.join(('url', 'invalid'))
    with pytest.raises(ValueError):
        write.write_url(url=url, fn=fn)
