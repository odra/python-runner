import json

import pytest

from smrunner import errors


@pytest.fixture
def random_error():
  return errors.BaseError(code=1, message='Random error', data={'a': 1})


@pytest.fixture
def random_error_data(random_error):
  return random_error.as_python()


@pytest.fixture
def random_error_json(random_error):
  return random_error.as_json()


def test_random_error_message(random_error):
  assert str(random_error) == '[Error]:1:Random error'


def test_random_error_repr(random_error):
  assert repr(random_error) == '<BaseError(code=1, message=Random error, data={\'a\': 1})>'


def test_data_key(random_error_data):
  assert random_error_data['data']['a'] == 1


def test_data_code(random_error_data):
  assert random_error_data['code'] == 1


def test_data_message(random_error_data):
  assert random_error_data['message'] == 'Random error'


def test_random_error_json(random_error_data, random_error_json):
  assert random_error_data == json.loads(random_error_json)


def test_parse_error():
  with pytest.raises(errors.ParseError) as err:
    raise errors.ParseError()
  assert err.value.code == -32700
  assert err.value.data is None


def test_function_not_found_error():
  with pytest.raises(errors.FunctionNotFoundError) as err:
    raise errors.FunctionNotFoundError('fn')
  assert err.value.code == -32601
  assert err.value.data['function'] == 'fn'


def test_invalid_params_error():
  with pytest.raises(errors.InvalidParamsError) as err:
    raise errors.InvalidParamsError('fn', ['p1', 2, True])
  assert err.value.code == -32602
  assert err.value.data['function'] == 'fn'
  assert err.value.data['params'] == ['p1', 2, True]


def test_internal_error():
  with pytest.raises(errors.InternalError) as err:
    raise errors.InternalError()
  assert err.value.code == -32603
  assert err.value.data is None


def test_runtime_error():
  with pytest.raises(errors.RuntimeError) as err:
    raise errors.RuntimeError('fn', ['hello world'], 'invalid var')
  assert err.value.code == -32000
  assert err.value.data['function'] == 'fn'
  assert err.value.data['params'] == ['hello world']
  assert err.value.data['trace'] == 'invalid var'

