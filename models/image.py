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

    @hybrid_property
    def total_donation(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            total = total + donation.amount
        return round(total)
