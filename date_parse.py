import dateparser
from datetime import datetime
import re

parse_config = {'PREFER_DATES_FROM': 'future'}

pat = re.compile(r'(.*)в ([\d]{1,2})\D?([\d]{1,2})*')


def preparse(inp):
    if re.findall(pat, inp):
        pre = re.findall(pat, inp)[0]
        return pre[0] + pre[1] + ':' + pre[2] + bool(not (pre[2])) * '00'
    else:
        return inp


def date_parse(dstring: str):
    parsed = dateparser.parse(preparse(dstring), settings=parse_config)
    if parsed < datetime.now():
        return date_parse('завтра' + dstring)
    return parsed
