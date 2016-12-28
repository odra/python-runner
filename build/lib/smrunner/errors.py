import json


class BaseError(Exception):
  def __init__(self, code=None, message=None, data=None):
    super(BaseError, self).__init__(message)
    self.code = code
    self.message = message
    self.data = data

  def __str__(self):
    return '[Error]:%s:%s' % (self.code, self.message)

  def __repr__(self):
    values = (self.__class__.__name__, self.code, self.message, self.data)
    return '<%s(code=%s, message=%s, data=%s)>' % values

  def as_python(self):
    return {
      'code': self.code,
      'message': self.message,
      'data': self.data
    }

  def as_json(self):
    return json.dumps(self.as_python())


class ParseError(BaseError):
  def __init__(self):
    super(ParseError, self).__init__()
    self.code = -32700
    self.message = 'Parse error.'
    self.data = None


class FunctionNotFoundError(BaseError):
  def __init__(self, fn_name):
    super(FunctionNotFoundError , self).__init__()
    self.fn_name = fn_name
    self.code = -32601
    self.message = 'Function not found error.'
    self.data = {
      'function': self.fn_name
    }


class InvalidParamsError(BaseError):
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
  def __init__(self):
    super(InternalError, self).__init__()
    self.code = -32603
    self.message = 'Internal error.'
    self.data = None


class RuntimeError(BaseError):
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
