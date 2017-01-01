import json
import six
import base64


def fix_tuple(s):
  if six.PY2 is True and type(s) is unicode:
    return s.encode('utf8')
  return s


def json_code_hook(data):
  for (k, v) in six.iteritems(data):
    if type(v) is list:
      if six.PY2 is True:
        data[k] = tuple([fix_tuple(i) for i in v])
      else:
        data[k] = tuple(v)
    if six.PY2 is True and type(v) is unicode:
        data[k] = data[k].encode('utf8')
  return data


def encode(data):
  if six.PY2 is True:
    return base64.b64encode(data)
  return base64.b64encode(data.encode('utf8')).decode('utf8')


def decode(data):
  if six.PY2 is True:
    return base64.b64decode(data)
  return base64.b64decode(data.encode('utf8')).decode('utf8')
