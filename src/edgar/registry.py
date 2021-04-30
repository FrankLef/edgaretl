"""Singleton with the EDGAR specs such as url, rss prefix"""

# The public example provided by IANA
EXAMPLE_URL = 'http://example.com'
# A simple HTTP request and response service by Kenneth Reitz
SIMPLE_URL = 'https://httpbin.org'


EDGAR_URL = 'https://www.sec.gov/Archives/edgar'
EDGAR_URL_MONTH = 'https://www.sec.gov/Archives/edgar/monthly'
# this is the olf edgar monthly url.  It has http instead of https
# it is useful to test, for example, the http code 301
EDGAR_URL_MONTH_OLD = 'http://www.sec.gov/Archives/edgar/monthly'
EDGAR_XBRLRSS = 'xbrlrss'


def test_url(choice: int = 0):
    val = (EXAMPLE_URL, SIMPLE_URL)
    return val[choice]


def edgar_url(choice: int = 0):
    val = (EDGAR_URL, EDGAR_URL_MONTH, EDGAR_URL_MONTH_OLD)
    return val[choice]


def rss():
    """The prefix used to create te rss feed file.

    Returns:
        [str]: Prefix to rss feed file.
    """
    return EDGAR_XBRLRSS
