from pathlib import Path
from datetime import datetime
import requests
import fetch

TEST_URL = 'https://httpbin.org'  # site build explicitly for testing, nice!
WRONG_URL = "http://WRONG_URL"
EDGAR_URL = 'http://www.sec.gov/Archives/edgar/monthly'

a_period = datetime(2021, 1, 1)
a_dir = Path.cwd().joinpath('data', 'xbrlrss', str(a_period.year))
a_file = "-".join(('xbrlrss', str(a_period.year),
                  str(a_period.month).zfill(2))) + '.xml'
a_path = a_dir.joinpath(a_file)
a_url = EDGAR_URL
a_url = requests.compat.urljoin(a_url, a_file)

out = fetch.fetch_rss(path=a_dir, period=a_period, url=EDGAR_URL)
print(out)
