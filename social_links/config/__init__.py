from pathlib import Path

from ConfigFramework import BaseConfig
from ConfigFramework.loaders import YAMLLoader, EnvLoader, CompositeLoader
from ConfigFramework.variables import ConfigVar, BoolVar

yaml_config_loader = YAMLLoader.load("config.yaml")
composite_loader = CompositeLoader.load(yaml_config_loader, EnvLoader.load())


class SocialLinksConfig(BaseConfig):
    debug = BoolVar("debug", yaml_config_loader)
    static_folder = ConfigVar("static_folder", yaml_config_loader, caster=Path)


social_links_config = SocialLinksConfig()
