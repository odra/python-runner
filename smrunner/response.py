import json

from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ModelType
from smrunner.helpers.schema import BytesType, TupleType, LazyDictType, DynamicType


class Error(Model):
  code = IntType(required=True)
  message = StringType(required=True)
  data = LazyDictType()


class Response(Model):
  jsonrpc = StringType(required=True, default='2.0')
  _id = StringType()
  error = ModelType(Error)
  result = DynamicType()

  @classmethod
  def as_result(cls, _id=None, data=None):
    return cls(raw_data={'_id': _id, 'result': data})

  @classmethod
  def as_error(cls, code, message, data=None, _id=None):
    err = Error(raw_data={'code': code, 'message': message, 'data': data})
    return cls(raw_data={'_id': _id, 'error': err})

  def as_dict(self):
    data = {
      'jsonrpc': self.jsonrpc,
      'id': self._id
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
    return json.dumps(self.as_dict())

