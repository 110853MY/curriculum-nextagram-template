from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    email = pw.CharField(unique=True)
    username = pw.CharField(unique=True)
    password = pw.CharField(unique=True)
