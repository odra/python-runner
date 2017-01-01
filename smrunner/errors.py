import json


class BaseError(Exception):
  """
  Base error class to be used by other error classes.
  """
  def __init__(self, code=None, message=None, data=None):
    super(BaseError, self).__init__(message)
    self.code = code
    self.message = message
    self.data = data

  def __str__(self):
    """
    String to be returned by the "str()" function.

    Returns:
      A string with the error code and message.
    """
    return '[Error]:%s:%s' % (self.code, self.message)

  def __repr__(self):
    """
    Value to be returns by the "repr()" function.

    Returns:
      A string containing the error code, message and data.
    """
    values = (self.__class__.__name__, self.code, self.message, self.data)
    return '<%s(code=%s, message=%s, data=%s)>' % values

  def as_python(self):
    """
    Retreieves the error fields in a dict.

    Returns:
      A dict with the error code, message and data.
    """
    return {
      'code': self.code,
      'message': self.message,
      'data': self.data
    }

  def as_json(self):
    """
    Retrieves the error fields in a json string.

    Returns:
      A json string with the error code, message and data.
    """
    return json.dumps(self.as_python())


class ParseError(BaseError):
  """
  Error to be raised when parsing code objects, function objects, etc.
  """
  def __init__(self):
    super(ParseError, self).__init__()
    self.code = -32700
    self.message = 'Parse error.'
    self.data = None


class FunctionNotFoundError(BaseError):
  """
  Raised when function object or code data is not found.
  """
  def __init__(self, fn_name):
    super(FunctionNotFoundError , self).__init__()
    self.fn_name = fn_name
    self.code = -32601
    self.message = 'Function not found error.'
    self.data = {
      'function': self.fn_name
    }


class InvalidParamsError(BaseError):
  """
  Raised when wrong number (missing, kwargs, etc) is used in the function call.
  """
  def __init__(self, fn_name, fn_params):
    super(InvalidParamsError, self).__init__()
    self.fn_name = fn_name
    self.fn_params = fn_params
    self.code = -32602
    self.message = 'Invalid params error.'
    self.data = {
      'function': self.fn_name,
      'params': self.fn_params
    }


class InternalError(BaseError):
  """
  Random and unkown internal error.
  """
  def __init__(self):
    super(InternalError, self).__init__()
    self.code = -32603
    self.message = 'Internal error.'
    self.data = None


class RuntimeError(BaseError):
  """
  Raised by function execution when something goes wrong.
  """
  def __init__(self, fn_name, fn_params=None, fn_trace=None):
    super(RuntimeError, self).__init__()
    self.fn_name = fn_name
    self.fn_params = fn_params
    self.fn_trace = fn_trace
    self.code = -32000
    self.message = 'Runtime error.'
    self.data = {
      'function': self.fn_name,
      'params':self.fn_params,
      'trace': self.fn_trace
    }
