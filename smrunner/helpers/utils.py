import inspect

import six


def is_valid_prop(k):
  """
  Checks if it is a valid exception property to be serialized.

  param: n(str) - exception property name

  Returns:
    True if it does not start/end with "__".
    Returns false for "with_traceback" property in python 3.
  """
  if six.PY3 and n == 'with_traceback':
    return False
  if k.startswith('__') and k.endswith('__'):
    return False
  return True


def inspect_err(e):
  """
  Inspects an Exception object to retrieve its information.

  param: e(Exception) - exception instance

  Returns:
    A dictionary containing the exception module, name and properties.
  """
  props = dir(e)
  module = inspect.getmodule(e)
  data = {k:getattr(e, k) for k in props if is_valid_prop(k)}
  data['__name__'] = e.__class__.__name__
  if module is not None:
    data['__module__'] = module.__name__
  return data
