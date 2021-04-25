import imghdr
from typing import Optional
from pathlib import Path
from hashlib import sha256
from urllib.parse import ParseResult, urljoin

import requests
import sqlalchemy as sa

from social_links.app import db
from social_links.config import social_links_config


class LinkIcon(db.Model):
    icon_id = sa.Column(sa.String(length=256), primary_key=True)
    icon_name = sa.Column(sa.String(length=64), nullable=False)

    @classmethod
    def get_or_create_icon(cls, parsed_url: ParseResult):
        icon = db.query(cls).filter_by(icon_id=parsed_url.netloc).one_or_none()

        if not icon:
            icon_name = cls._fetch_icon(parsed_url)

            if icon_name is None:
                raise ValueError("can't fetch icon")

            icon = cls(icon_name=icon_name)
            db.commit()

        return icon

    @staticmethod
    def _fetch_icon(parsed_url: ParseResult) -> Optional[str]:
        site_url_hash = sha256(parsed_url.scheme + parsed_url.netloc).hexdigest()

        try:
            fetched_icon = requests.get(
                urljoin(parsed_url.scheme + parsed_url.netloc, "favicon.ico"),
                timeout=1
            )

        except requests.exceptions.RequestException:
            return

        # Limit icon size to 2512kb
        if int(fetched_icon.headers.get('Content-Length')) > 512 * 1024:
            return None

        if not imghdr.what("", h=fetched_icon.raw):
            return None

        else:
            icon_name = site_url_hash + ".ico"
            icons_dir: Path = social_links_config.static_folder.value / "icons"
            (icons_dir / icon_name).write_bytes(fetched_icon.raw)

        return icon_name

    @property
    def icon_file(self):
        return social_links_config.static_folder.value / "icons" / self.icon_name
