import copy

import pytest

from smrunner.fn import Code, Function

from smrunner.errors import RuntimeError, ParseError


@pytest.fixture
def fn():
  def fn(o):
    return 'Hello %s!' % o
  return fn


def test_no_args_error(fn):
  func = Function.from_code(Code.from_function(fn))
  with pytest.raises(RuntimeError) as err:
    func()
  assert err.value.code == -32000


def test_code_error(fn):
  code = Code.from_function(fn)
  code.argcount = None
  with pytest.raises(ParseError) as err:
    code.as_code()
  assert err.value.code == -32700
