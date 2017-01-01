import json
import six
import base64


def fix_tuple_item(s):
  """
  Fix tuple unicode item to be converted in a string (python 2 only) 

  param: s(unicode) - unicode variable to be converted

  Returns:
    A convterted string in utf8
  """
  if six.PY2 is True and type(s) is unicode:
    return s.encode('utf8')
  return s


def json_code_hook(data):
  """
  JSON object_Hook to parse json data to be used in a code object. 

  param: data(dict) - a dictionary to be parsed

  Returns:
    A dict with the parsed json and proper field conversion
  """
  for (k, v) in six.iteritems(data):
    if type(v) is list:
      if six.PY2 is True:
        data[k] = tuple([fix_tuple_item(i) for i in v])
      else:
        data[k] = tuple(v)
    if six.PY2 is True and type(v) is unicode:
        data[k] = data[k].encode('utf8')
  return data


def encode(data):
  """
  Encodes some string or bytes to base64, handles python 3 bytes as well.

  param: data(string or byte) - A string (python2) or byte(python3) to be encoded.

  Returns:
    A string with the encoded value
  """
  if six.PY2 is True:
    return base64.b64encode(data)
  return base64.b64encode(data.encode('utf8')).decode('utf8')


def decode(data):
  """
  Decodes a base64 string(pyhton 2) or byte(python 3).

  param: data(string ot byte) - A string (python) or byte(python 3) to be encoded

  Returns:
    A string with the decoded value
  """
  if six.PY2 is True:
    return base64.b64decode(data)
  return base64.b64decode(data.encode('utf8')).decode('utf8')
