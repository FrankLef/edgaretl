from pathlib import Path
from datetime import datetime
import requests
from src.edgar.xbrlrss import write


def fetch_rss(url: str, path: Path = Path.cwd(), period: datetime = datetime.now(),
              head: bool = False, overwrite: bool = False):

    # create the file name and add it to the path
    if path.exists():
        fn = write.write_fn(period=period)
        path = path.joinpath(fn)
    else:
        msg = "The directory des not exist.\n{path}"
        raise FileNotFoundError(msg)

    # don't process a file that already exists unless required
    if not head and path.exists and not overwrite:
        msg = f"File already exists and will be skiped.\n{fn}"
        raise FileExistsError(msg)

    # add filename to the url
    url_fn = write.write_url(url=url, fn=fn)

    # make the request
    if not head:
        with requests.get(url_fn) as r:
            with path.open(mode='w') as f:
                if r.status_code == 200:
                    f.write(r.text)
                    # msg = f"\"{fn}\" download OK. Content length = {r.headers['content-length']}"
                    # print(msg)
    else:
        with requests.head(url_fn) as r:
            pass

    return r.status_code
