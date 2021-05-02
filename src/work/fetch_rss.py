from pathlib import Path  # noqa
import sys  # noqa
import winsound
# must insert the level above src in the sys.path
# the level just above in this case is the cwd()
sys.path.insert(1, str(Path.cwd()))  # noqa
# print(sys.path)  # noqa

from src.edgar import registry
from src.edgar.xbrlrss import write
from src.edgar.xbrlrss import fetch
import requests
from datetime import datetime

# we use the prefix also for the subdirectory, discretionary
prefix = registry.rss_prefix()
dir_2020 = registry.rss_path(0)
test_url = str(registry.test_url())
edgar_url = registry.edgar_url(0)
month_url = registry.edgar_url(1)
oldmonth_url = registry.edgar_url(2)


a_period = datetime(2020, 1, 1)
# we use the prefix also for the subdirectory, discretionary
# a_dir = Path.cwd().joinpath('data', prefix, str(a_period.year))
a_dir = Path(dir_2020)
a_file = write.write_fn(period=a_period)
a_path = a_dir.joinpath(a_file)
a_url = month_url
a_url_fn = a_url + r"/" + a_file

# print(a_path)

# print(a_url)
# with requests.head(a_url) as r:
#     print(r.status_code)
#     print(r.headers)


print(a_url_fn)
# with requests.head(a_url_fn) as r:
#     print(r.status_code)
#     print(r.headers)

winsound.PlaySound('SystemAsterix', winsound.SND_ALIAS)
