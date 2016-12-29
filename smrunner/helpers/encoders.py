import json


def fix_tuple(s):
  if type(s) is unicode:
    return s.encode('utf8')
  return s


def json_code_hook(data):
  for (k, v) in data.iteritems():
    if type(v) is list:
      data[k] = tuple([fix_tuple(i) for i in v])
    if type(v) is unicode:
      data[k] = v.encode('utf8')
  return data

