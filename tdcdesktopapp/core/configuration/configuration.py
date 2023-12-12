__all__ = [
    'load_and_apply',
    'show_css_editor'
]
from tdcdesktopapp.core.configuration.abstract_loader import AbstractConfigurationLoader
from tdcdesktopapp.core.configuration.singleton import ConfigurationSingleton


# FIXME: this belongs to infrastructure
def load_and_apply(loader: AbstractConfigurationLoader) -> None:
    """Loads configuration to `ConfigurationSingleton`"""
    loader.load()
    ConfigurationSingleton().show_css_editor = loader.show_css_editor

    if loader.persistence_name == "ram":
        from tdcdesktopapp.infrastructure.ram.persistence.configuration import RamPersistenceConfiguration
        ConfigurationSingleton().persistence_configuration = RamPersistenceConfiguration()

        from tdcdesktopapp.infrastructure.ram.persistence.expense import RamExpensesPersistence
        ConfigurationSingleton().persistence_expense = RamExpensesPersistence()

        from tdcdesktopapp.infrastructure.ram.persistence.project import RamProjectsPersistence
        ConfigurationSingleton().persistence_project = RamProjectsPersistence()

        from tdcdesktopapp.infrastructure.ram.multiplayer_message_provider import RamMultiplayerMessageProvider
        ConfigurationSingleton().multiplayer_message_provider_client = RamMultiplayerMessageProvider()

        from tdcdesktopapp.infrastructure.ram.authentication import RamSecurityLogin
        ConfigurationSingleton().security_login = RamSecurityLogin(configuration=None)

    elif loader.persistence_name == "http":
        from tdcdesktopapp.infrastructure.http.persistence.configuration import HttpPersistenceConfiguration
        ConfigurationSingleton().persistence_configuration = HttpPersistenceConfiguration()
        ConfigurationSingleton().persistence_configuration.attributes["api_host"] = loader.api_host

        from tdcdesktopapp.infrastructure.http.persistence.expense import HttpExpensesPersistence
        ConfigurationSingleton().persistence_expense = HttpExpensesPersistence()

        from tdcdesktopapp.infrastructure.http.persistence.project import HttpProjectsPersistence
        ConfigurationSingleton().persistence_project = HttpProjectsPersistence()

        from tdcdesktopapp.infrastructure.http.websocket_multiplayer_message_provider import (
            WebSocketMultiplayerMessageProvider)
        ConfigurationSingleton().multiplayer_message_provider_client = WebSocketMultiplayerMessageProvider()

        from tdcdesktopapp.infrastructure.http.authentication import HttpSecurityLogin
        ConfigurationSingleton().security_login = HttpSecurityLogin(configuration=loader.auth0_configuration)


def show_css_editor() -> bool:
    """Returns True if CSS editor should be shown"""
    return ConfigurationSingleton().show_css_editor
