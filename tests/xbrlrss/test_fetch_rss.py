import pytest
from pathlib import Path
from datetime import datetime
from src.edgaretl import registry
from src.edgaretl.xbrlrss import write
from src.edgaretl.xbrlrss import fetch


@pytest.fixture
def dir_2020():
    return registry.rss_path(0)


@pytest.fixture
def test_url():
    return registry.test_url()


@pytest.fixture
def edgar_url():
    return registry.edgar_url(0)


@pytest.fixture
def month_url():
    return registry.edgar_url(1)


@pytest.fixture
def oldmonth_url():
    return registry.edgar_url(2)


@pytest.fixture
def specs(dir_2020, month_url):
    per = datetime(2020, 1, 1)
    a_dir = Path(dir_2020)
    fn = write.write_fn(period=per)
    path = a_dir.joinpath(fn)
    url = month_url
    url_fn = url + r"/" + fn
    specs = {'period': per,
             'dir': a_dir,
             'file': fn,
             'path': path,
             'url': url,
             'url_fn': url_fn}
    return(specs)


def test_fetch_rss_err_dir(test_url):
    with pytest.raises(FileNotFoundError):
        assert fetch.fetch_rss(url=test_url, path=Path.cwd().joinpath('WRONG'))


def test_fetch_rss_head_oldmonth(oldmonth_url, specs):
    assert fetch.fetch_rss(url=oldmonth_url, path=specs['dir'],
                           period=specs['period'], head=True) in {301, 403}


def test_fetch_rss_head_month(specs):
    assert fetch.fetch_rss(url=specs['url'], path=specs['dir'],
                           period=specs['period'], head=True) in {200, 403}


# only done from time to time as it takes resources
@pytest.mark.skip(reason="too slow, do it only if necessary")
def test_fetch_rss(specs):
    assert fetch.fetch_rss(url=specs['url'], path=specs['dir'],
                           period=specs['period'], overwrite=True) in {200, 403}


def test_fetch_rss_err_exists(specs):
    with pytest.raises(FileExistsError):
        assert fetch.fetch_rss(url=specs['url'], path=specs['dir'],
                               period=specs['period'], overwrite=False)
