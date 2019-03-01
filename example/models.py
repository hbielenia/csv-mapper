from .fields import *
from .mapper import Model


class Person(Model):
  name = StringField()
  height_cm = IntegerField()
  salary = DecimalField()
