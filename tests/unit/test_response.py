from smrunner.response import Response


def test_result_response():
  res = Response.as_result(_id='12345', data='hello')
  assert res.as_dict()['result'] == 'hello'
  assert type(res.as_json()) is str


def test_error_response():
  res = Response.as_error(-32404, 'not found', data={'file': 'not found'}, _id='12345')
  assert res.as_dict()['error']['code'] == -32404
  assert type(res.as_json()) is str
