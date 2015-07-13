from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

# from implugin.beaker import BeakerApplication
# from implugin.haml import HamlApplication
# from implugin.sqlalchemy.application import SqlAlchemyApplication

# from implugin.fanstatic import FanstaticApplication
from impaf.application import Application


class AuthApplication(Application):

    def _get_config_kwargs(self):
        data = super()._get_config_kwargs()

        # TODO: this should be configurable
        data['authentication_policy'] = AuthTktAuthenticationPolicy(
            'somesecret',
            hashalg='sha512',
        )
        data['authorization_policy'] = ACLAuthorizationPolicy()

        return data
