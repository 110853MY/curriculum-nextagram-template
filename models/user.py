from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw


class User(UserMixin, BaseModel):
    email = pw.CharField(unique=True)
    username = pw.CharField(unique=True)
    password = pw.CharField(unique=True)
