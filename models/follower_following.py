from models.base_model import BaseModel
from models.user import User
import peewee as pw


class FollowerFollowing(BaseModel):
    fans = pw.ForeignKeyField(User, backref="idols")
    idols = pw.ForeignKeyField(User, backref="fans")

    # @hybrid_property
    # def followers(self):
    #     from models.follower_following import FollowerFollowing
    #     return [user.idol for user in FollowerFollowing.select().where(FollowerFollowing.fan_id == self.id)]

    # @hybrid_property
    # def following(self):
    #     from models.follower_following import FollowerFollowing
    #     return [user.fan for user in FollowerFollowing.select().where(FollowerFollowing.idol_id == self.id)]

    # @hybrid_method
    # def is_following(self, user):
    #     from models.follower_following import FollowerFollowing
    #     return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id)) else False

    # @hybrid_method
    # def is_followed_by(self, user):
    #     from models.follower_following import FollowerFollowing
    #     return True if FollowerFollowing.get_or_none((FollowerFollowing.fan_id == user.id) & (FollowerFollowing.idol_id == self.id)) else False
