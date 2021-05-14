import re
from datetime import datetime


def write_fn(period: datetime = datetime.now(), prefix: str = 'xbrlrss', ext: str = '.xml') -> str:
    """Write the filename with pattern prefix-YYYY-MM-.xml

    Args:
        period (datetime, optional): Date from which year and month come. Defaults to datetime.now().
        prefix (str, optional): The prefix for the filename. Defaults to 'xbrlrss'.
        ext (str, optional): The extension of the file. Defaults to '.xml'.

    Raises:
        ValueError: The period is out-of-bound.

    Returns:
        str: String with pattern prefix-YYYY-MM-.xml
    """

    # the xbrl rss from EDGAR begin in 2005-04. They are not available before.
    limits = (datetime(year=2005, month=4, day=1), datetime(2100, 1, 1))
    if period < limits[0] or period >= limits[1]:
        msg = f"The period must be between {limits[0]} and {limits[1]}.\nperiod: {period}"
        raise ValueError(msg)

    fn = '-'.join((prefix, str(period.year), str(period.month).zfill(2))) + ext
    assert len(fn) > len(ext)

    return fn


def write_url(url: str, fn: str) -> str:
    """Add the file name to the url.

    Args:
        url (str): The url before appending the filename.
        fn (str): The filename without the directory path.

    Raises:
        ValueError: The url does not start with "http"

    Returns:
        str: The url including the file name
    """

    # this is also useful to ensure the length > 0
    p = re.compile(r"http.+")
    if not p.match(url):
        msg = "The url must begin with \"http\".\n{url}"
        raise ValueError(msg)

    # concatenate the url with the file name, add / if there is none
    # NOTE: do not use requests.compat.urljoin(), it creates problems
    # problems by truncating anything after the last "/".add().
    # Also, it removes a dependency.
    p = re.compile(r"/$")
    if p.search(url):
        url = url + fn
    else:
        url = url + r"/" + fn

    return url
