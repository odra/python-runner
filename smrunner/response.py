import json

from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType
from smrunner.helpers.schema import BytesType, TupleType, LazyDictType, DynamicType


class Error(Model):
  """
  JSONRPC error schematics model.
  """
  code = IntType(required=True)
  message = StringType(required=True)
  data = LazyDictType()


class Response(Model):
  """
  JSONRPC schematics model to be used in json responses.
  """
  jsonrpc = StringType(required=True, default='2.0')
  error = ModelType(Error)
  result = DynamicType()

  @classmethod
  def as_result(cls, _id=None, data=None):
    """
    Class method that builds the Response class as a result response.

    param: _id(str) - optional rpc id
    param: data(list or dict) - list or dict to be used as response data

    Returns:
      A new instance of Response
    """
    return cls(raw_data={'result': data})

  @classmethod
  def as_error(cls, code, message, data=None, _id=None):
    """
    Class method that builds the Response class as an error response.

    param: code(int) - error code to be used
    param: message(str) - error string message
    param: _id(str) - optional rpc id
    param: data(list or dict) - specific error data/information

    Returns:
      A new instance of Response
    """
    err = Error(raw_data={'code': code, 'message': message, 'data': data})
    return cls(raw_data={'error': err})

  def as_dict(self):
    """
    Parses the model fields as a dict.

    Returns:
      A dict with the model properties and its values.
    """
    data = {
      'jsonrpc': self.jsonrpc
    }
    if self.error is not None:
      data['error'] = {
        'code': self.error.code,
        'message': self.error.message,
        'data': self.error.data
      }
    else:
      data['result'] = self.result
    return data

  def as_json(self):
    """
    Parses the Model as a json string.

    Returns:
      A string with the model json reprensentation.
    """
    return json.dumps(self.as_dict())

