from mock import patch
from mock import sentinel

from pytest import fixture
from pytest import yield_fixture

from impaf.application import Application

from ..application import AuthApplication


class MockedAuthApplication(Application):

    def _get_config_kwargs(self):
        self._data = {}
        return self._data


class ExampleAuthApplication(
    AuthApplication,
    MockedAuthApplication,
):
    pass


class TestAuthApplication(object):

    @fixture
    def testable(self):
        return ExampleAuthApplication('module')

    @yield_fixture
    def mAuthTktAuthenticationPolicy(self):
        patcher = patch(
            'implugin.auth.application.AuthTktAuthenticationPolicy'
        )
        with patcher as mock:
            yield mock

    def test_get_config_kwargs(self, testable, mAuthTktAuthenticationPolicy):
        testable.settings = {
            'auth_secret': 'secret',
        }
        testable._authorization_policy = sentinel.ACLAuthorizationPolicy

        data = testable._get_config_kwargs()

        assert data == {
            'authentication_policy': mAuthTktAuthenticationPolicy.return_value,
            'authorization_policy': sentinel.ACLAuthorizationPolicy,
        }
        mAuthTktAuthenticationPolicy.assert_called_once_with(
            'secret',
            hashalg='sha512',
        )
