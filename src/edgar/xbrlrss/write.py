from pathlib import Path
from datetime import datetime
import requests


def write_path(path: Path, period: datetime = datetime.now(),
               prefix: str = 'xbrlrss', ext: str = '.xml', check: bool = False) -> Path:
    """Write the full file name for the rss feed file using a given path.

    Args:
        path (Path, optional): Basic path excluding file name where data will be stored.
        period (datetime, optional):  Period whose year and month will be used to write the file name.
        prefix (str, optional): prefix of filename. Defaults to 'edgar'.
        ext (str, optional): Extension of the file. Defaults to '.xml'.
        check (bool, optional): TRUE: reurn ValueError if file already exists.

    Raises:
        ValueError: path must be a pathlib.Path object.
        FileExistsError: When check=True, file already exists.

    Returns:
        Path: Path where the xbrl rss file will be saved.
    """
    if not isinstance(path, Path):
        msg = ("The data directory path must be a pathlib.Path object.")
        raise ValueError(msg)

    fn = prefix + '_'
    fn += '-'.join((str(period.year), str(period.month).zfill(2))) + ext
    path = path.joinpath(fn)
    if check:
        if path.exists:
            msg = f"The file already exists.\n{path}"
            raise FileExistsError(msg)
    return path


def write_url(url: str = 'https://www.sec.gov/Archives/edgar/monthly',
              period: datetime = datetime.now(),
              prefix: str = 'xbrlrss', ext: str = '.xml', check: bool = False) -> str:
    """Write full url to of xbrl rss feed

    Args:
        url (str, optional): Basic url of rss site. Defaults to 'https://www.sec.gov/Archives/edgar/monthly'.
        period (datetime, optional): Period whose year and month will be used to write the url.
        prefix (str, optional): Prefix of xbrl rss. Defaults to 'xbrlrss'.
        ext (str, optional): File extension. Defaults to '.xml'.
        check (bool, optional): True=Raise ValueError is url does not exist.

    Raises:
        ValueError: When check=True, url must be valid.

    Returns:
        str: url for xbrl rss feed.
    """
    # the xbrl rss from EDGA begin in 2005-04. They are not available before.
    limits = (datetime(year=2005, month=4, day=1), datetime(2100, 1, 1))
    if period < limits[0] or period >= limits[1]:
        msg = f"The period must be between {limits[0]} and {limits[1]}.\nperiod: {period}"
        raise ValueError(msg)

    doc = "-".join((prefix, str(period.year), str(period.month).zfill(2)))
    url = '/'.join((url, doc)) + ext

    # validate the url before using it
    if check:
        try:
            r = requests.head(url)
        except requests.exceptions.ConnectionError as e:
            msg = f"The url is invalid, verify it carefully.\n{url}"
            raise requests.exceptions.ConnectionError(msg) from e
    return url
