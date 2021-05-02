from pathlib import Path
from datetime import datetime
from time import mktime
import feedparser
from pprint import pprint as pp
import winsound

# must be same year as directory since used below
period = datetime(2020, 1, 1)
path = Path.cwd().joinpath('data', 'xbrlrss', '2020')

# print(path)
if not path.exists:
    msg = f"Invalid path.\n{path}"
    winsound.PlaySound('SystemHand', winsound.SND_ALIAS)
    raise FileNotFoundError(msg)

# fn = 'xbrlrss-2020-01.xml'
# path_fn = path.joinpath(fn)

# NOTE: **/*.xml would be used if we needed recursive
files = path.glob(pattern=r"*.xml")
# tuple don't exist with generators because they are immutable
# wwe simply enclosed the generator in the tuple() fonction to convert it
files = tuple(x for x in files if x.is_file())
# print(type(files))

# for f in files:
#     print(f)

path_fn = path.joinpath(files[0])
# print(path_fn)
fpd = feedparser.parse(path_fn)
if not isinstance(fpd, feedparser.util.FeedParserDict):
    msg = f"The feed is a {type(fpd)}"
    winsound.PlaySound('SystemHand', winsound.SND_ALIAS)
    raise ValueError(msg)

# NOTE: the feed header=None since we are using a local file
msg = f"\nHEADERS\n{fpd.headers}\n"
if len(fpd.entries):
    msg += f"Number of items in the feed = {len(fpd.entries)}"
else:
    msg += "There is no entry in the feed."
    winsound.PlaySound('SystemHand', winsound.SND_ALIAS)
    raise ValueError(msg)
print(msg)

# print the top feed (channel)
print(f"\nCHANNEL is a {type(fpd.feed)}\n")
for key in fpd.feed:
    val = fpd.feed[key]
    msg = f"{key} = {val}"
    print(msg)

# update data dict with channel data
data = {}
# convert time stamp to datetime
pubDate_datetime = datetime.fromtimestamp(mktime(fpd.feed['published_parsed']))
data['channel'] = {'title': fpd.feed['title'],
                   'language': fpd.feed['language'],
                   'pubDate': pubDate_datetime,
                   'items_nb': len(fpd.entries)}

print(f"\nITEMS\n")
msg = f"Number of items in the feed = {len(fpd.entries)}"
print(msg)

ndx = 0
itemKey = "item" + str(ndx)
msg = f"\nITEM\n{fpd.entries[ndx]['title']}\n"
print(msg)

entry = fpd.entries[ndx]
for key in entry:
    val = entry[key]
    msg = f"\"{key}\""
    print(msg)

# update data dict with item data
pubDate_datetime = datetime.fromtimestamp(mktime(entry['published_parsed']))
data_item = {'title': entry['title'],
             'pubDate': pubDate_datetime,
             'edgar:companyName': entry['edgar_companyname'],
             'edgar:formType': entry['edgar_formtype'],
             'edgar:cikNumber': entry['edgar_ciknumber'],
             'edgar:accessionNumber': entry['edgar_accessionnumber'],
             'edgar:period': entry['edgar_period'],
             'edgar:fiscalyearend': entry['edgar_fiscalyearend']}

msg = f"\nENCLOSURE\n"
print(msg)

links = entry.links
enclosures = [x for x in links if x['rel'] == 'enclosure']
print(type(enclosures))
print(enclosures)
if len(enclosures):
    enclosure = enclosures[0]
    enclosure_len = enclosure['length']
    enclosure_url = enclosure['href']

# update data dict with enclosure data
data_item['enclosure_len'] = enclosure_len
data_item['enclosure_url'] = enclosure_url

# aappend the item data to the main data dictinnary
data[itemKey] = data_item
print("\nDATA")
pp(data)


# the location of xbrl files extracted from sec
cik = data[itemKey]['edgar:cikNumber']
filing_type = data[itemKey]['edgar:formType']
xbrl_path = Path.cwd().joinpath('data', 'xbrl', str(period.year),
                                str(period.month).zfill(2), cik, filing_type)
fn = data[itemKey]['enclosure_url'].split('/')[-1]
msg = f"\nPATH & FILE\n"
print(msg)
print(xbrl_path)
print(fn)

# winsound.MessageBeep()
winsound.PlaySound('SystemAsterix', winsound.SND_ALIAS)
