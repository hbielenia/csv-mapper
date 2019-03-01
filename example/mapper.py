import csv

from .fields import BaseField

class BaseModel(type):
  
  def __new__(cls, *args, **kwargs):
    new_cls = super().__new__(cls, *args, **kwargs)

    # Don't process the immediate subclass
    if new_cls.__name__ == 'Model':
      return new_cls

    fields = {}
    for attrname in dir(new_cls):
      attr = getattr(new_cls, attrname)
      if issubclass(attr.__class__, BaseField):
        fields[attrname] = attr
    new_cls.fields = fields

    new_cls._filename = new_cls.__name__ + '.csv'
    open(new_cls._filename, 'a').close() ## Ensure that file exists

    with open(new_cls._filename, 'r') as csvfile:
      reader = csv.DictReader(csvfile, fieldnames=fields.keys())
      new_cls.objects = [new_cls(**row) for row in reader]

    return new_cls


class Model(metaclass=BaseModel):

  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)
  
  def __setattr__(self, name, value):
    if name in self.fields:
      value = self.fields[name](value).value
    return super().__setattr__(name, value)
  
  def __iter__(self):
    return iter(
      [(f, getattr(self, f)) for f in self.fields])
  
  def save(self):
    with open(self._filename, 'a') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fields.keys())
      writer.writerow(dict(self))
      if self not in self.objects:
        self.objects.append(self)
