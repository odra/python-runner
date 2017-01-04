from smrunner.helpers import utils


def test_inspect_error():
  try:
    a.append('a')
  except Exception as e:
    err = e
  err = utils.inspect_err(err)
  assert len(err['args']) == 1
  assert err['__name__'] == u'NameError'
  assert err.get('__module__') is None
