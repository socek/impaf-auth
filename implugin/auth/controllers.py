from impaf.controller import Controller

# from .forms import LoginForm
# from .helpers import LoginFormWidget
from .requestable import AuthRequestable


# class LoginController(Controller, AuthRequestable):

#     template = 'auth:login.jinja2'

#     def make(self):
#         if self.user.is_logged():
#             self.redirect(self.settings['auth_redirect'])
#             return

#         form = self.add_form(LoginForm, widget=LoginFormWidget)
#         if form.validate() is True:
#             self.redirect(self.settings['auth_redirect'])
#             return

#         self.data['login_header'] = self.settings.get(
#             'login_header',
#             'Hatak Auth'
#         )


# class ForbiddenController(AuthController):

#     template = 'auth:forbidden.jinja2'

#     def make(self):
#         if not self.user.is_logged():
#             self.redirect('auth:login')


# class LogoutController(AuthController):

#     permissions = [('base', 'view'), ]

#     def make(self):
#         self.redirect('auth:login')
#         self.session.clear()
