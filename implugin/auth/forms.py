from pyramid.security import remember

from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty

from implugin.formskit.models import PostForm


class EmailMustExists(FormValidator):

    message = "EmailMustExists"

    def validate(self):
        email = self.form.get_value('email')
        self.form._user = self.form.drivers.Auth.get_by_email(email)
        return self.form._user is not None


class PasswordMustMatch(FormValidator):

    message = "PasswordMustMatch"

    def validate(self):
        data = self.form.get_data_dict(True)
        return self.form._user.validate_password(data['password'])


class LoginForm(PostForm):

    def create_form(self):
        self.add_field('email', label='E-mail', validators=[NotEmpty()])
        self.add_field('password', label='Hasło', validators=[NotEmpty()])

        self.add_form_validator(EmailMustExists())
        self.add_form_validator(PasswordMustMatch())

    def on_success(self):
        headers = remember(self.request, str(self._user.id))
        self.request.response.headers.extend(headers)
