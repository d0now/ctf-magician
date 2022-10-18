from peewee import IntegerField, CharField, ForeignKeyField
from cmag.database import CMagBaseModel
from cmag.challenge.model import CMagChallengeModel

class CMagFileModel(CMagBaseModel):
    id   = IntegerField(primary_key=True)
    path = CharField(unique=True)
    root = IntegerField()
    type = IntegerField()
    challenge = ForeignKeyField(CMagChallengeModel, backref="files")
