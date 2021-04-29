from pathlib import Path
from datetime import datetime
import requests


def write_fn(dir: Path = Path.cwd(), period={'year': None, 'month': None}, prefix: str = 'xbrlrss',
             ext: str = '.xml', check: bool = False) -> Path:
    """Write the full file name for the rss feed file

    Args:
        dir (Path, optional): Basic path excluding file name. Created with write_dir().
        period (dict, optional): Year and month of the rss feed. Defaults to {'year': None, 'month': None}.
                                 When either is None, current year and month are used.
        prefix (str, optional): prefix of filename. Defaults to 'edgar'.
        ext (str, optional): Extension of the file. Defaults to '.xml'.
        check (bool, optional): TRUE=Error if file already exists, FALSE=do nothing. Defaults to False.

    Raises:
        ValueError: [description]

    Returns:
        Path: Full name where the xbrl file will be saved.
    """
    if not isinstance(dir, Path):
        msg = ("The data directory path is missing. Must be a pathlib.Path object.")
        raise ValueError(msg)
    if period['year'] is None or period['month'] is None:
        now = datetime.now()
        period['year'] = now.year
        period['month'] = now.month

    a_file = prefix + '_' + '-'.join((str(period['year']),
                                     str(period['month']).zfill(2))) + ext
    a_file = dir.joinpath(a_file)
    if check and a_file.exists:
        msg = "File already exists. Delete it or use another name."
        msg = f"\n{msg}\n\"{a_file}\"\n"
        raise ValueError(msg)
    return a_file


def write_dir(dir: Path = Path('data', 'xbrlrss'), year: int = None) -> Path:
    """Write the full directory where xbrlsrss files will be stored

    Args:
        dir (Path, optional): Data directory. Defaults to Path('data', 'xbrlrss').
        year (int, optional): Year representing subdirecory of data directory. Defaults to None.
                              When None, current year is used.

    Raises:
        ValueError: The year is out-of-bound.

    Returns:
        Path: Full path of data directory with year subdirectory.
    """
    # must use current year if None
    year = datetime.now().year if year is None else year
    limits = (2000, 2030)  # the allowed range of years
    if not year >= limits[0] and year <= limits[1]:
        msg = f"The year {year} is not between {limits[0]} and {limits[1]}"
        raise ValueError(msg)
    a_path = Path.cwd()
    a_path = a_path.joinpath(dir, str(year))
    # a_path.mkdir(parents=True, exist_ok=True)
    return a_path


def write_url(url: str = 'https://www.sec.gov/Archives/edgar/monthly', prefix: str = 'xbrlrss',
              period: list = {'year': None, 'month': None}, ext: str = '.xml') -> str:
    """Write full url to of xbrl rss feed

    Args:
        url (str, optional): Basic url of rss site. Defaults to 'https://www.sec.gov/Archives/edgar/monthly'.
        prefix (str, optional): Prefix of xbrl rss. Defaults to 'xbrlrss'.
        period (list, optional): Period in yyyy-mm format. Defaults to {'year': None, 'month': None}.
                                 When None, current year and month willl be used.
        ext (str, optional): File extension. Defaults to '.xml'.

    Returns:
        str: Full url for xbrl rss feed.
    """
    # assign default values
    if (period['year'] is None) or (period['month'] is None):
        now = datetime.now()
        period['year'] = now.year
        period['month'] = now.month

    doc = "-".join((prefix, str(period['year']),
                    str(period['month']).zfill(2)))
    url = '/'.join((url, doc)) + ext
    # validate the url before using it
    try:
        r = requests.head(url)
    except requests.exceptions.ConnectionError as e:
        msg = f"The url is invalid, usually caused by an inexistant url.\n{url}"
        print(msg)
        raise requests.exceptions.ConnectionError
    return url
