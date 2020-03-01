from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
from playhouse.hybrid import hybrid_property


class User(UserMixin, BaseModel):
    email = pw.CharField(unique=True)
    username = pw.CharField(unique=True)
    password = pw.CharField(unique=True)
    profile_image = pw.CharField(null=True)

    @hybrid_property
    def profile_image_url(self):
        return f"https://110853my-nextagram.s3.southeast-1.amazonaws.com(self.profile_image)"

    # def is_authenticated(self):
    #     return True

    # def is_active(self):
    #     return True

    # def validate(self):
    #     print(f'Validation implemented on (str(type(self)))')

    #     existing_username = User.get_or_none(User.username == self.username)
    #     if existing.username and not existing_username.id == self.id:
    #         self.errors.append('Username already taken')

    #     existing_email = User.get_or_none(User.email == self.email)
    #     if existing.email and not existing_email.id == self.id:
    #         self.errors.append('Email already taken')

    #     if not self.id and(len(self.password) < 6 or len(self.password) > 13):
    #         self.errors.append('Password must be between 6-13')
    #     else:
    #         if not self.id:
    #             self.password = generate_password_hash(self.password)

    #     return True
