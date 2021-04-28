from pathlib import Path
from datetime import datetime


def get_fn(path, period={'year': 0, 'month': 0}, prefix: str = 'edgar', ext: str = '.xml', check: bool = False) -> Path:
    """Write the full file name for the rss feed file

    Args:
        path ([type]): Basic path exlcuding file name.
        period (dict, optional): Year an dmonth of the rss feed. Defaults to {'year': 0, 'month': 0}.
        prefix (str, optional): prefix of filename. Defaults to 'edgar'.
        ext (str, optional): Extension of the file. Defaults to '.xml'.
        check (bool, optional): TRUE=Error if file already exists, FALSE=do nothing. Defaults to False.

    Raises:
        ValueError: [description]

    Returns:
        Path: Full name where the xbrl file will be saved.
    """
    a_file = '-'.join((prefix, str(period['year']),
                       str(period['month']).zfill(2))) + ext
    a_file = path.joinpath(a_file)
    if check and path.exists:
        msg = "File already exists. Delete it or use another name."
        msg = f"\n{msg}\n\"{a_file}\"\n"
        raise ValueError(msg)
    return a_file


def get_dir(dir: str = 'data/xbrlrss', year: int = None) -> Path:
    year = datetime.now().year if year is None else year
    a_path = Path(__file__).parent.resolve().joinpath(dir)
    a_path = a_path.joinpath(str(year))
    # a_path.mkdir(parents=True, exist_ok=True)
    return a_path


def write_url(url: str, prefix: str = 'xbrlrss', period: list = {'year': None, 'month': None}) -> str:
    """Write full url to of xbrl rss feed

    Args:
        url (str): Basic url of rss site
        prefix (str, optional): Prefix of xbrl rss. Defaults to 'xbrlrss'.
        period (list, optional): Period in yyy-mm format. Defaults to {'year': 0, 'month': 0}.

    Returns:
        str: Full url for xbrl rss feed.
    """
    if (period['year'] is None) or (period['month'] is None):
        now = datetime.now()
        period['year'] = now.year
        period['month'] = now.month

    doc = "-".join((prefix, str(period['year']),
                    str(period['month']).zfill(2)))
    url = '/'.join((url, doc)) + '.xml'
    return url
