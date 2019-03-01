from decimal import Decimal


class BaseField:

  def __init__(self):
    self.value = self.data_type(False)
  
  def __call__(self, value):
    self.value = self.data_type(value)
    return self
  
  def __repr__(self):
    if hasattr(self, 'value'):
      return repr(self.value)
    else:
      return super().__repr__()

class DecimalField(BaseField):
  data_type = Decimal

class IntegerField(BaseField):
  data_type = int

class StringField(BaseField):
  data_type = str
