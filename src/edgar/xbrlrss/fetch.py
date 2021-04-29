from pathlib import Path
from datetime import datetime
import requests
from src.edgar.xbrlrss import write


def fetch_rss(path: Path, period: datetime = datetime.now(),
              url: str = 'https://www.sec.gov/Archives/edgar/monthly',
              head: bool = False, check_url: bool = False, check_path: bool = False):
    # add the filename to the path
    path = write.write_path(path=path, period=period, check=check_path)
    # create the directory if it doesn't already exist
    # path.mkdir(parents=True, exist_ok=True)

    # write the url
    url = write.write_url(url=url, period=period, check=check_url)

    # if required, only process HEAD and return result
    if head:
        try:
            with requests.head(url) as r:
                return r.status_code
        except requests.exceptions.ConnectionError as e:
            msg = f"The url is invalid, verify it carefully.\n{url}"
            raise requests.exceptions.ConnectionError(msg) from e

    # source:
    # https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file
    with requests.get(url) as r:
        with path.open(mode='w') as f:
            if r.status_code == 200:
                f.write(r.text)
                # NOTE: lines to use if you want byte content instead of text.
                # mode='wb' could be used to download binary file
                # use f.write(r.content) when open(mode='wb')
                # f.write(r.content)
            elif r.status_code == 403:
                msg = f"\nstatus {r.status_code}: Access not granted by SEC. Just retry later.\n"
                raise ConnectionRefusedError(msg)
            else:
                msg = f"\nstatus {r.status_code}: Connection error with SEC other than access not granted.\n"
                raise requests.exceptions.ConnectionError(msg)
            return r.status.code

# NOTE: How to do it with urllib3. requets uses urlib3.
# source:
# https://urllib3.readthedocs.io/en/latest/user-guide.html
# https://stackoverflow.com/questions/27387783/how-to-download-a-file-with-urllib3
# from urllib3 import PoolManager
# http = PoolManager()
# with http.request(method='GET', url=url, preload_content=False) as r:
#     with open(file=path, mode='wb') as f:
#         if r.status == 200:
#             f.write(r.data)
#         elif r.status == 403:
#             msg = f"\nstatus {r.status}: Access not granted by SEC. Just retry later.\n"
#             raise ConnectionRefusedError(msg)
#         else:
#             msg = f"status {r.status}: Connection error with SEC other than access not granted."
#             raise ConnectionError(msg)
