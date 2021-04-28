import sys
from rss import write
from urllib3 import PoolManager
import requests
# import responses

# source: https: // urllib3.readthedocs.io/en/latest/user-guide.html

EDGAR_URL = 'https://www.sec.gov/Archives/edgar/monthly'
period = {'year': 2020, 'month': 1}

# write the full file name
edgar_path = write.get_dir(path='data', period=period)
try:
    edgar_fn = write.get_fn(path=edgar_path, period=period,
                            prefix='edgar', ext='.xml')
except ValueError as e:
    print(e, file=sys.stderr)
    raise
print(edgar_fn, end='\n')

# write the url
edgar_url = write.write_url(url=EDGAR_URL, period=period)
print(edgar_url, end='\n')

# source:
# https://stackoverflow.com/questions/27387783/how-to-download-a-file-with-urllib3
# http = urllib3.PoolManager()
# with http.request(method='GET', url=edgar_url, preload_content=False) as r:
#     with open(file=edgar_fn, mode='wb') as f:
#         if r.status == 200:
#             f.write(r.data)
#         elif r.status == 403:
#             msg = f"\nstatus {r.status}: Access not granted by SEC. Just retry later.\n"
#             print(msg)
#             raise ConnectionRefusedError(msg)
#         else:
#             msg = f"status {r.status}: Connection error with SEC."
#             print(msg)
#             raise ConnectionError(msg)


# source:
# https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file
with requests.get(edgar_url) as r:
    # mode='wb' could be used to download binary file
    with open(file=edgar_fn, mode='w') as f:
        if r.status_code == 200:
            f.write(r.text)
            # use f.write(r.content) when open(mode='wb')
            # f.write(r.content)
        elif r.status_code == 403:
            msg = f"\nstatus {r.status_code}: Access not granted by SEC. Just retry later.\n"
            print(msg)
            raise ConnectionRefusedError(msg)
        else:
            msg = f"\nstatus {r.status_code}: Connection error with SEC.\n"
            print(msg)
            raise ConnectionError(msg)

# TODO: Now parse the file with feeparser

# feed = feedparser.parse(r.data)

# print(r.status)

# print(r.data)

# json.loads(r.data.decode('utf-8'))
