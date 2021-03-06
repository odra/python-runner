import inspect
import types
import json

from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType
import six

from smrunner.helpers.schema import BytesType, TupleType, LazyDictType
from smrunner.helpers import encoders
from smrunner import errors


CODE_HELPER_PROPS = ('defaults',)

class Code(Model):
  """
  Class to store code object properties (schematics model) and merthods.
  """
  argcount = IntType(required=True, default=0)
  kwonlyargcount = IntType(default=0)
  cellvars = TupleType(required=True)
  code = BytesType(required=True)
  consts = TupleType(required=True)
  filename = StringType(required=True)
  firstlineno = IntType(required=True)
  flags = IntType(required=True)
  freevars = TupleType(required=True)
  lnotab = BytesType(required=True)
  name = StringType(required=True, default='<string>')
  names = TupleType(required=True)
  nlocals = IntType(required=True) 
  stacksize = IntType(required=True)
  varnames = TupleType(required=True)
  defaults = TupleType()

  def __init__(self, *args, **kwargs):
    super(Code, self).__init__(*args, **kwargs)
    self.fix_props()

  def fix_props(self):
    """
    Fix properties for usage in both python2 and python3.
    """
    if six.PY3 is True and type(self.code) is str:
      self.code = self.code.encode('utf8')
    if six.PY3 is True and type(self.lnotab) is str:
      self.lnotab = self.lnotab.encode('utf8')
    if six.PY2 is True and type(self.name) is unicode:
      self.name = self.name.encode('utf8')
    if six.PY2 is True and type(self.filename) is unicode:
      self.filename = self.filename.encode('utf8')

  @classmethod
  def from_function(cls, fn):
    """
    Creates a new Code instance based on a function.

    param: fn(Function) - fucntion to be used.

    Returns:
      A new Code object.
    """
    code = fn.__code__
    data = {k.replace('co_', ''):getattr(code, k) for k in dir(code) if k.startswith('co_')}
    self = cls(raw_data=data)
    self.parse_args(inspect.getargspec(fn))
    return self

  @classmethod
  def from_json(cls, data):
    """
    Creates a new Code object from a given json string.

    param: data(str) - Json string to be used

    Returns:
      A new Code object. 
    """
    try:
      parsed_data = json.loads(data, object_hook=encoders.json_code_hook)
    except ValueError as e:
      raise errors.ParseError()
    self = cls(raw_data=parsed_data)
    return self

  @classmethod
  def from_file(cls, path):
    """
    Creates a new Code object based from a json string written a file.

    param: path(srt) - json file path to be loaded.

    Returns:
      A new Code instance.
    """
    try:
      return cls.from_json(open(path).read())
    except IOError as e:
      raise errors.FunctionNotFoundError(path)

  def parse_args(self, spec):
    """
    Sets defaults args in Code instance based on specs object (from inspect module).

    param: spec(inspect.getargspec) - spec object returned by inspect module.
    """
    if spec.defaults is not None:
      self.defaults = spec.defaults

  def as_dict(self, only_code=True):
    """
    Parses code object as dict.

    param: only_code(bool) - Flag to indicate if it should retrieve all fields or only those that belong to __code__.

    Returns:
      A dict with the instance code fields.
    """
    data = {
      'argcount': self.argcount,
      'nlocals': self.nlocals,
      'stacksize': self.stacksize,
      'flags': self.flags,
      'code': self.code,
      'consts': self.consts,
      'names': self.names,
      'varnames': self.varnames,
      'filename': self.filename,
      'name': self.name,
      'firstlineno': self.firstlineno,
      'lnotab': self.lnotab,
      'freevars': self.freevars,
      'cellvars': self.cellvars
    }
    if six.PY2 is False:
      data['kwonlyargcount'] = self.kwonlyargcount
    if only_code is False:
      [data.update({key:getattr(self, key)}) for key in CODE_HELPER_PROPS]
    return data

  def as_json(self, only_code=True):
    """
    Parses the Code object as a json string.

    param: only_code(bool) - Flag to indicate if it should retrieve all fields or only those that belong to __code__

    Returns:
      A json string with the code object fields.
    """
    BYTES_PROPS = ('code', 'lnotab')
    data = self.as_dict()
    if six.PY3 is True:
      for bp in BYTES_PROPS:
        data[bp] = data[bp].decode('utf8')
    return json.dumps(data, only_code)

  def as_code(self):
    """
    Parses the Code object as a new CodeType object.

    Returns:
      A new types.CodeType object.
    """
    self.fix_props()
    data = [self.argcount]
    if six.PY2 is False:
      data.append(self.kwonlyargcount)
    data.extend([
      self.nlocals,
      self.stacksize,
      self.flags,
      self.code,
      self.consts,
      self.names,
      self.varnames,
      self.filename,
      self.name,
      self.firstlineno,
      self.lnotab,
      self.freevars,
      self.cellvars
    ])
    try:
      return types.CodeType(*data)
    except TypeError as e:
      raise errors.ParseError()


class Function(Model):
  """
  Class to store fucntion and its related code. It also runs the functon call.
  """
  code =  ModelType(Code, required=True)

  @classmethod
  def from_code(cls, code):
    """
    creates a new Function object from a code object.

    param: code(Code) - Code object to be used.

    Returns:
      A new Function object.
    """
    return cls(raw_data={'code': code})

  def __call__(self, *args, **kwargs):
    """
    Callable python interface, executes the object "run" method.
    """
    return self.run(*args, **kwargs)

  def get_default_env(self):
    """
    Define default globals and insert python builtins into the function.

    Returns:
      A dict with the function globals.
    """
    _globals = globals()
    env = {
      '__builtins__': _globals['__builtins__']
    }
    return env

  def build_fn(self, **kwargs):
    """
    Builds the function object (types.FunctionType) based on the instance code property.

    Returns:
      A new types.FunctionType object.
    """
    _globals = kwargs.get('globals', {})
    _globals.update(self.get_default_env())
    name = kwargs.get('name', 'fn')
    if six.PY2 is True:
      name = name.encode('utf8')
    argdefs = kwargs.get('argdefs', tuple())
    closure = kwargs.get('closure', tuple())
    code = self.code.as_code()
    return types.FunctionType(code, _globals, name, argdefs, closure)

  def run(self, *args, **kwargs):
    """
    Runs the function object and returns the response.

    Also, it passes and args and kwargs to the function call.

    Returns:
      The function response.
    """
    kw = {
      'name': self.code.name
    }
    if self.code.defaults is not None:
      kw['argdefs'] = self.code.defaults
    fn = self.build_fn(**kw)
    try:
      return fn(*args, **kwargs)
    except TypeError as e:
      params = {
        'args': args,
        'kwargs': kwargs
      }
      raise errors.RuntimeError(kw['name'], params, str(e))
