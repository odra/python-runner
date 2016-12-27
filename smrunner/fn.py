import inspect
import types
import json

from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType

from smrunner.helpers.schema import BytesType, TupleType, LazyDictType
from smrunner.helpers import encoders

from smrunner.errors import RuntimeError, ParseError


class Code(Model):
  argcount = IntType(required=True)
  cellvars = TupleType(required=True)
  code = BytesType(required=True)
  consts = TupleType(required=True)
  filename = StringType(required=True)
  firstlineno = IntType(required=True)
  flags = IntType(required=True)
  freevars = TupleType(required=True)
  lnotab = BytesType(required=True)
  name = StringType(required=True)
  names = TupleType(required=True)
  nlocals = IntType(required=True) 
  stacksize = IntType(required=True)
  varnames = TupleType(required=True)
  defaults = TupleType()

  @classmethod
  def from_function(cls, fn):
    code = fn.__code__
    data = {k.replace('co_', ''):getattr(code, k) for k in dir(code) if k.startswith('co_')}
    self = cls(raw_data=data)
    self.parse_args(inspect.getargspec(fn))
    return self

  @classmethod
  def from_json(cls, data):
    parsed_data = json.loads(data, object_hook=encoders.json_code_hook)
    self = cls(raw_data=parsed_data)
    return self

  @classmethod
  def from_file(cls, path):
    return cls.from_json(open(path).read())

  def parse_args(self, spec):
    if spec.defaults is not None:
      self.defaults = spec.defaults

  def as_dict(self):
    return {
      'argcount': self.argcount,
      'nlocals': self.nlocals,
      'stacksize': self.stacksize,
      'flags': self.flags,
      'code': self.code,
      'consts': self.consts,
      'names': self.names,
      'varnames': self.varnames,
      'filename': self.filename.encode('utf8'),
      'name': self.name.encode('utf8'),
      'firstlineno': self.firstlineno,
      'lnotab': self.lnotab,
      'freevars': self.freevars,
      'cellvars': self.cellvars
    }

  def as_json(self):
    return json.dumps(self.as_dict())

  def as_code(self):
    filename = self.filename
    name = self.name
    if type(name) is unicode:
      name = name.encode('utf8')
    if type(filename) is unicode:
      filename = filename.encode('utf8')
    try:
      return types.CodeType(
        self.argcount,
        self.nlocals,
        self.stacksize,
        self.flags,
        self.code,
        self.consts,
        self.names,
        self.varnames,
        filename,
        name,
        self.firstlineno,
        self.lnotab,
        self.freevars,
        self.cellvars
      )
    except TypeError as e:
      raise ParseError()


class Function(Model):
  code =  ModelType(Code, required=True)

  @classmethod
  def from_code(cls, code):
    return cls(raw_data={'code': code})

  def __call__(self, *args, **kwargs):
    return self.run(*args, **kwargs)

  def get_default_env(self):
    _globals = globals()
    env = {
      '__builtins__': _globals['__builtins__']
    }
    return env

  def build_fn(self, **kwargs):
    _globals = kwargs.get('globals', {})
    _globals.update(self.get_default_env())
    name = kwargs.get('name', 'fn')
    argdefs = kwargs.get('argdefs', tuple())
    closure = kwargs.get('closure', tuple())
    code = self.code.as_code()
    return types.FunctionType(code, _globals, name, argdefs, closure)

  def run(self, *args, **kwargs):
    kw = {
      'name': self.code.name.encode('utf8')
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
      raise RuntimeError(kw['name'], params, e.message)
