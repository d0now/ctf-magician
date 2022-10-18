from peewee import CharField, IntegerField
from cmag.database import CMagBaseModel

class CMagChallengeModel(CMagBaseModel):
    id   = IntegerField(primary_key=True)
    name = CharField()
    desc = CharField(null=True)
