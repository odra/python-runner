from schematics.types import BaseType
from schematics.exceptions import ValidationError


class TupleType(BaseType):
  def validate_tuple(self, value):
    if not type(value) in (tuple, list):
      raise ValidationError('Type must be a tuple')


class BytesType(BaseType):
  def validate_bytes(self, value):
    if not type(value) in (str, unicode, bytes):
      raise ValidationError('Type must be a valid bytes format')


class LazyDictType(BaseType):
  def validate_bytes(self, value):
    if type(value) is not dict:
      raise ValidationError('Type must be a valid dict')


class LazyDictOrListType(BaseType):
  def validate_bytes(self, value):
    if not type(value) in (dict, list):
      raise ValidationError('Type must be a valid dict or list')



class DynamicType(BaseType):
  def validate_bytes(self, value):
    pass
