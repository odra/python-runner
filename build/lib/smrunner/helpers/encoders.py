import json


def json_code_hook(data):
  for (k, v) in data.iteritems():
    if type(v) is list:
      data[k] = tuple(v)
    if type(v) is unicode:
      data[k] = v.encode('utf8')
  return data

