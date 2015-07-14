from pyramid.security import forget

from implugin.formskit.controller import FormskitController

from .forms import LoginForm
from .widgets import LoginFormWidget
from .requestable import AuthRequestable


class BaseAuthController(FormskitController, AuthRequestable):

    def goto_login(self):
        self.redirect('auth:login')

    def goto_home(self):
        self.redirect('home')

    def get_main_template(self):
        return ''

    def _create_context(self):
        super()._create_context()
        self.context['auth'] = {
            'main_template': self.get_main_template(),
        }


class LoginController(BaseAuthController):

    renderer = 'implugin.auth.controllers:templates/login.jinja2'
    form_widget = LoginFormWidget
    form = LoginForm
    permission = 'guest'
    header_text = 'Login'

    def _create_context(self):
        super()._create_context()
        self.context['auth']['header'] = self.header_text

    def make(self):
        if self.get_user().is_authenticated():
            self.goto_home()
            return

        form = self.add_form(self.form, widgetcls=self.form_widget)
        if form.validate():
            self.goto_home()
            return


class ForbiddenController(BaseAuthController):

    renderer = 'implugin.auth.controllers:templates/forbidden.jinja2'
    header_text = 'Forbidden'

    def _create_context(self):
        super()._create_context()
        self.context['auth']['header'] = self.header_text

    def make(self):
        if not self.get_user().is_authenticated():
            self.goto_login()
            return


class LogoutController(FormskitController, AuthRequestable):
    permission = 'auth'

    def make(self):
        headers = forget(self.request)
        self.request.response.headerlist.extend(headers)
        self.goto_login()
