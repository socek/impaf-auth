from mock import MagicMock
from mock import patch
from mock import sentinel

from formskit import Form
from pytest import fixture
from pytest import yield_fixture

from implugin.sqlalchemy.testing import SqlalchemyRequestFixture

from ..forms import EmailMustExists
from ..forms import EmailMustNotExists
from ..forms import LoginMixin
from ..forms import PasswordsMustMatch
from ..forms import ValidateUserPassword


class TestLoginMixin(SqlalchemyRequestFixture):
    _testable_cls = LoginMixin

    @yield_fixture
    def mremember(self):
        patcher = patch('implugin.auth.forms.remember')
        with patcher as mock:
            yield mock

    def test_force_login(self, testable, mrequest, mremember, registry):
        testable.request = mrequest
        testable._force_login('user_id')

        mremember.assert_called_once_with(mrequest, 'user_id')
        headers = mremember.return_value
        mrequest.response.headers.extend.assert_called_once_with(headers)


class FormValidatorFixtures(object):

    @fixture
    def form(self):
        return Form()

    @fixture
    def testable(self, form):
        model = self._testable_cls()
        model.set_form(form)
        return model


class TestEmailMustExists(FormValidatorFixtures):
    _testable_cls = EmailMustExists

    @fixture
    def form(self):
        form = super().form()
        form.add_field('email')
        form.drivers = MagicMock()
        return form

    def test_success(self, testable, form):
        form.parse_dict({
            'email': 'test@app.com',
        })
        form.drivers.Auth.get_by_email.return_value = sentinel.user

        assert testable.validate() is True
        assert form._user == sentinel.user
        form.drivers.Auth.get_by_email.assert_called_once_with('test@app.com')

    def test_fail(self, testable, form):
        form.parse_dict({
            'email': 'test@app.com',
        })
        form.drivers.Auth.get_by_email.return_value = None

        assert testable.validate() is False
        assert form._user is None
        form.drivers.Auth.get_by_email.assert_called_once_with('test@app.com')


class TestEmailMustNotExists(FormValidatorFixtures):
    _testable_cls = EmailMustNotExists

    @fixture
    def form(self):
        form = super().form()
        form.add_field('email')
        form.drivers = MagicMock()
        return form

    def test_success(self, testable, form):
        form.parse_dict({'email': 'test@app.com'})
        form.drivers.Auth.get_by_email.return_value = sentinel.user

        assert testable.validate() is False
        assert form._user == sentinel.user
        form.drivers.Auth.get_by_email.assert_called_once_with('test@app.com')

    def test_fail(self, testable, form):
        form.parse_dict({'email': 'test@app.com'})
        form.drivers.Auth.get_by_email.return_value = None

        assert testable.validate() is True
        assert form._user is None
        form.drivers.Auth.get_by_email.assert_called_once_with('test@app.com')


class TestValidateUserPassword(FormValidatorFixtures):
    _testable_cls = ValidateUserPassword

    @fixture
    def form(self):
        form = super().form()
        form.add_field('password')
        return form

    def test_validate(self, testable, form):
        form.parse_dict({'password': sentinel.password})
        form._user = MagicMock()

        assert (
            testable.validate() == form._user.validate_password.return_value
        )
        form._user.validate_password.assert_called_once_with(sentinel.password)


class TestPasswordsMustMatch(FormValidatorFixtures):
    _testable_cls = PasswordsMustMatch

    @fixture
    def form(self):
        form = super().form()
        form.add_field('password')
        form.add_field('confirm_password')
        return form

    def test_success(self, testable, form):
        form.parse_dict({
            'password': 'one',
            'confirm_password': 'one',
        })

        assert testable.validate()

    def test_fail(self, testable, form):
        form.parse_dict({
            'password': 'one',
            'confirm_password': 'two',
        })

        assert not testable.validate()
