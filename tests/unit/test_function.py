import types

import pytest

from smrunner.fn import Code, Function, errors


@pytest.fixture
def fn_error():
  def fn():
    return a
  return fn


@pytest.fixture
def fn():
  def fn():
    return 'Hello World!'
  return fn


@pytest.fixture
def fn_arg():
  def fn(o):
    return 'Hello %s!' % o
  return fn


@pytest.fixture
def fn_kw():
  def fn(o='bob'):
    return 'Hello %s!' % o
  return fn


@pytest.fixture
def fn_two_args():
  def fn(quote, target):
    return '%s %s!' % (quote, target)
  return fn

@pytest.fixture
def fn_two_kw():
  def fn(quote='Hello', target='bob'):
    return '%s %s!' % (quote, target)
  return fn


@pytest.fixture
def fn_one_arg_and_one_kw():
  def fn(name, age=32):
    return 'Hello, my name is %s and I am %s years old!' % (name, age)
  return fn


@pytest.fixture
def fn_many_kw():
  def fn(**kwargs):
    return 'I am from %s' % kwargs['country']
  return fn


@pytest.fixture
def fn_all():
  def fn(name, age=32, **kwargs):
    country = kwargs.get('country', 'Brazil')
    return 'My name is %s, I am %s years old and located at %s' % (name, age, country)
  return fn


@pytest.fixture
def fn_dynamic():
  def fn(*args, **kwargs):
    return 'Name "%s" and age "%s"' % (args[0], kwargs['age'])
  return fn


def test_hello_world_function(fn):
  func = Function.from_code(Code.from_function(fn))
  func.validate()
  assert func() == 'Hello World!'


def test_error_function(fn_error):
  func = Function.from_code(Code.from_function(fn_error))
  func.validate()
  with pytest.raises(errors.RuntimeError) as err:
    func()
  assert err.value.as_python()['data']['trace']['__name__'] == 'NameError'


def test_arg_function(fn_arg):
  func = Function.from_code(Code.from_function(fn_arg))
  func.validate()
  assert func('dude') == 'Hello dude!'


def test_kw_function(fn_kw):
  func = Function.from_code(Code.from_function(fn_kw))
  func.validate()
  assert func() == 'Hello bob!'
  assert func(o='ted') == 'Hello ted!'
  assert func('nobody') == 'Hello nobody!'


def test_two_args_function(fn_two_args):
  func = Function.from_code(Code.from_function(fn_two_args))
  func.validate()
  assert func('Hello', 'bob') == 'Hello bob!'
  assert func('Ted', 'long time') == 'Ted long time!'


def test_two_kw_function(fn_two_kw):
  func = Function.from_code(Code.from_function(fn_two_kw))
  func.validate()
  assert func() == 'Hello bob!'
  assert func(quote='Hi') == 'Hi bob!'
  assert func(target='ted') == 'Hello ted!'
  assert func(target='det', quote='Hi') == 'Hi det!'
  assert func('Heya', target='ted') == 'Heya ted!'


def test_one_arg_one_kw_function(fn_one_arg_and_one_kw):
  func = Function.from_code(Code.from_function(fn_one_arg_and_one_kw))
  func.validate()
  assert func('Leo') == 'Hello, my name is Leo and I am 32 years old!'
  assert func('Dark Kyle', age=1000) == 'Hello, my name is Dark Kyle and I am 1000 years old!'


def test_many_kw_function(fn_many_kw):
  func = Function.from_code(Code.from_function(fn_many_kw))
  func.validate()
  assert func(country='Brazil') == 'I am from Brazil'


def test_all_function(fn_all):
  func = Function.from_code(Code.from_function(fn_all))
  func.validate()
  assert func('Leo') == 'My name is Leo, I am 32 years old and located at Brazil'
  assert func('Leo', country='Brazil') == 'My name is Leo, I am 32 years old and located at Brazil'
  assert func('Odra', age=20) == 'My name is Odra, I am 20 years old and located at Brazil'
  assert func('Dark Kyle', age=1000, country='Void') == 'My name is Dark Kyle, I am 1000 years old and located at Void'


def test_dyanmic_function(fn_dynamic):
  func = Function.from_code(Code.from_function(fn_dynamic))
  func.validate()
  assert func('Leo', age=32) == 'Name "Leo" and age "32"'
