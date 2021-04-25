from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from urllib.parse import unquote, urlparse

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from markupsafe import escape_silent

from social_links.app import db
from social_links.utils import squeeze
from .icons import LinkIcon

if TYPE_CHECKING:
    from .user import User


class Links(db.Model):
    link_id = sa.Column(sa.BigInteger, primary_key=True)
    user_id = sa.Column(sa.ForeignKey("users.id"), nullable=False, index=True)
    icon_id = sa.Column(sa.ForeignKey("icons.id"))
    description = sa.Column(sa.String(length=100))
    link_url = sa.Column(sa.String(length=256), nullable=True)

    icon = relationship(LinkIcon, uselist=False, lazy="joined")
    __tablename__ = "links"

    @classmethod
    def create_link(cls, user: User, link_url: str, description: Optional[str] = None):
        url_link_unquoted = unquote(link_url)
        parsed_url = urlparse(url_link_unquoted)

        if not parsed_url.scheme and not parsed_url.netloc:
            raise ValueError("Invalid linked url")

        if not description:
            description = parsed_url.netloc

        else:
            description = squeeze(description)
            description = escape_silent(description)
            description = str(description)

        try:
            link_icon_id = LinkIcon.get_or_create_icon(parsed_url).icon_id

        except ValueError:
            link_icon_id = None

        new_link = cls(user_id=user.user_id, link_url=url_link_unquoted, description=description, icon_id=link_icon_id)
        db.commit()

        return new_link
