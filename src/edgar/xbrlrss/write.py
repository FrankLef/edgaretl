from pathlib import Path
from datetime import datetime
import requests


def write_fn(dir: Path = Path.cwd(), period: datetime = datetime.now(), prefix: str = 'xbrlrss',
             ext: str = '.xml', check: bool = False) -> Path:
    """Write the full file name for the rss feed file

    Args:
        dir (Path, optional): Basic path excluding file name. Created with write_dir().
        period (datetime, optional):  Period whose year and month will be used to write the file name.
        prefix (str, optional): prefix of filename. Defaults to 'edgar'.
        ext (str, optional): Extension of the file. Defaults to '.xml'.
        check (bool, optional): TRUE=Error if file already exists. Defaults to False.

    Raises:
        ValueError: dir must be a pathlib.Path object.

    Returns:
        Path: Full name where the xbrl file will be saved.
    """
    if not isinstance(dir, Path):
        msg = ("The data directory path is missing. Must be a pathlib.Path object.")
        raise ValueError(msg)

    a_file = prefix + '_'
    a_file += '-'.join((str(period.year), str(period.month).zfill(2))) + ext
    a_file = dir.joinpath(a_file)
    if check and a_file.exists:
        msg = "File already exists. Delete it or use another name."
        msg = f"\n{msg}\n\"{a_file}\"\n"
        raise ValueError(msg)
    return a_file


def write_dir(dir: Path = Path('data', 'xbrlrss'), year: int = datetime.now().year) -> Path:
    """Write the full directory where xbrlsrss files will be stored

    Args:
        dir (Path, optional): Data directory. Defaults to Path('data', 'xbrlrss').
        year (int, optional): Year representing subdirecory of data directory. Defaults to current year.
                              When None, current year is used.

    Returns:
        Path: Full path of data directory with year subdirectory.
    """
    a_path = Path.cwd()
    a_path = a_path.joinpath(dir, str(year))
    # a_path.mkdir(parents=True, exist_ok=True)
    return a_path


def write_url(url: str = 'https://www.sec.gov/Archives/edgar/monthly', prefix: str = 'xbrlrss',
              period: datetime = datetime.now(), ext: str = '.xml', check: bool = False) -> str:
    """Write full url to of xbrl rss feed

    Args:
        url (str, optional): Basic url of rss site. Defaults to 'https://www.sec.gov/Archives/edgar/monthly'.
        prefix (str, optional): Prefix of xbrl rss. Defaults to 'xbrlrss'.
        period (datetime, optional): Period whose year and month will be used to write the url.
        ext (str, optional): File extension. Defaults to '.xml'.
        check (bool, optional): True=Verify is url exists.

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
            raise requests.exceptions.ConnectionError
    return url
