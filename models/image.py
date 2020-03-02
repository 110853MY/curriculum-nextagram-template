from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    image_name = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref="images")

    @hybrid_property
    def user_image_url(self):
        return f"https://110853my-nextagram.s3.amazonaws.com/{self.image_name}"
