from pathlib import Path
from datetime import datetime
from time import mktime  # to convert time.struct_time structure from feed
import feedparser


def parse_rss(file: str, ndx: int = -1, prefix: str = 'item') -> dict:
    fpd = feedparser.parse(file)
    n = len(fp.entries)
    if not n:
        msg = "There is no entry in the feed."
        raise ValueError(msg)
    elif ndx < -1:
        msg = "The ndx must be an integer >= -1. Now it is {ndx}."
        raise ValueError(msg)
    elif n-1 < ndx:
        msg = f"The nb of entries is {n}, ndx must be between 0 and {n-1}."
        raise ValueError(msg)

    # populate the channel data
    data = parse_rss_channel(fpd)

    z = len(str(n))
    if ndx == -1:
        i = 0
        for entry in fpd.entries:
            item = parse_rss_entry(entry=entry)
            data[prefix + str(i).zfill(z)] = item
            i += 1
    else:
        entry = fpd.entries[ndx]
        item = parse_rss_entry(entry=entry)
        data[prefix + str(ndx).zfill(z)] = item

    return data


def parse_rss_channel(fpd: feedparser.util.FeedParserDict) -> dict:
    # convert time stamp to datetime
    pubDate_datetime = datetime.fromtimestamp(
        mktime(fpd.feed['published_parsed']))
    # populate the channel data
    data = {}
    data['channel'] = {'title': fpd.feed['title'],
                       'language': fpd.feed['language'],
                       'pubDate': pubDate_datetime,
                       'items_nb': n}

    return data


def parse_rss_entry(entry: dict) -> dict:
    pubDate_datetime = datetime.fromtimestamp(mktime(item['published_parsed']))
    data = {'title': entry['title'],
            'pubDate': pubDate_datetime,
            'edgar:companyName': entry['edgar_companyname'],
            'edgar:formType': entry['edgar_formtype'],
            'edgar:cikNumber': entry['edgar_ciknumber'],
            'edgar:accessionNumber': entry['edgar_accessionnumber'],
            'edgar:period': entry['edgar_period'],
            'edgar:fiscalyearend': entry['edgar_fiscalyearend']}

    enclosures = [x for x in links if x['rel'] == 'enclosure']
    if len(enclosures):
        enclosure = enclosures[0]
        enclosure_len = enclosure['length']
        enclosure_url = enclosure['href']

    # update data dict with enclosure data
    data['enclosure_len'] = enclosure_len
    data['enclosure_url'] = enclosure_url

    return data
