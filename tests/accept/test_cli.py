import os
import imp
import json

import pytest

pyrunner = imp.load_source('pyrunner', os.path.abspath('./bin/pyrunner'))

from smrunner import fn


@pytest.fixture
def func():
  def _fn():
    return 'Hello World'
  return _fn


@pytest.fixture
def parser():
  return pyrunner.parser

@pytest.fixture
def func_path():
  return os.path.abspath('./tests/fixtures/func')


def test_empty_cli(parser):
  args = parser.parse_args([])
  assert args.json == False
  assert len(args.params) == 0
  assert args.file is None
  assert args.data is None


def test_cli_from_data(func, capsys):
  code = fn.Code.from_function(func)
  args = pyrunner.run(['--data', code.as_json()])
  (out, err) = capsys.readouterr()
  assert out == 'Hello World\n'


def test_cli_from_file(func_path, capsys):
  args = pyrunner.run(['--file', func_path])
  (out, err) = capsys.readouterr()
  assert out == 'Hello World\n'


def test_cli_json(func, capsys):
  code = fn.Code.from_function(func)
  args = pyrunner.run(['--data', code.as_json(), '--json'])
  (out, err) = capsys.readouterr()
  data = json.loads(out)
  assert data['result'] == 'Hello World'
