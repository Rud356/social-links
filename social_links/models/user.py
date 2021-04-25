import sqlalchemy as sa
from sqlalchemy.orm import relationship
from markupsafe import escape_silent

from social_links.app import db
from social_links.utils import squeeze, whitespace_re
from .services_links import Links


class User(db.Model):
    user_id = sa.Column(sa.String(length=50), nullable=False, primary_key=True)
    name = sa.Column(sa.String(length=50), nullable=False)
    description = sa.Column(sa.String(length=2048), nullable=True)
    banned_picture_id = sa.Column(sa.ForeignKey("banner_pictures.id"))
    profile_picture_id = sa.Column(sa.ForeignKey("profile_pictures.id"))

    links = relationship(Links, lazy="dynamic")
    __tablename__ = "users"

    @classmethod
    def create_user(cls, user_id: str, name: str):
        if not whitespace_re.search(name):
            raise cls.exc.InvalidNameError("Invalid name")

        user_id = squeeze(user_id)
        user_id = escape_silent(user_id)
        user_id = str(user_id)

        if len(user_id) == 0:
            raise cls.exc.InvalidIDError("Invalid user_id length after cleaning")

        new_user = cls(user_id=user_id)
        db.commit()

        return new_user

    def update_description(self, text: str) -> None:
        self.description = str(escape_silent(text))
        db.commit()

    def update_user_name(self, name: str) -> None:
        name = squeeze(name)
        name = escape_silent(name)
        name = str(name)
        if len(name) == 0:
            raise ValueError("Invalid name length")

        # TODO: remove cached page and update image
        self.name = name
        db.commit()

    class exc:
        class InvalidNameError(ValueError):
            pass

        class InvalidIDError(ValueError):
            pass
