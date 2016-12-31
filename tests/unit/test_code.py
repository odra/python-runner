import types

import pytest

from smrunner.fn import Code


@pytest.fixture
def fn():
  def fn():
    return 'Hello World!'
  return fn


@pytest.fixture
def fn_global():
  def fn():
    return a
  return fn


@pytest.fixture
def fn_code(fn):
  return fn.__code__


def test_code_object(fn_code):
  props = {p.replace('co_', ''):getattr(fn_code, p) for p in dir(fn_code) if p.startswith('co_')}
  code = Code(raw_data=props)
  for prop in [p for p in dir(fn_code) if p.startswith('co_')]:
    assert getattr(code, prop.replace('co_', '')) == getattr(fn_code, prop)


def test_code_as_dict(fn):
  code = Code.from_function(fn)
  data = code.as_dict()
  for (k, v) in data.items():
    assert v == getattr(fn.__code__, 'co_%s' % k) 


def test_code_from_function(fn):
  code = Code.from_function(fn)
  co = fn.__code__
  for prop in [p for p in dir(co) if p.startswith('co_')]:
    assert getattr(code, prop.replace('co_', '')) == getattr(co, prop)


def test_run_fn_from_code(fn):
  code = Code.from_function(fn)
  co = code.as_code()
  function = types.FunctionType(co, {}, co.co_name, None)
  assert function() == 'Hello World!'


def test_fn_with_global(fn_global):
  code = Code.from_function(fn_global)
  co = code.as_code()
  function = types.FunctionType(co, {'a': 1}, co.co_name, None)
  assert function() == 1
