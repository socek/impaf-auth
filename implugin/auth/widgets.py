from implugin.formskit.widget import FormWidget


class LoginFormWidget(FormWidget):

    _login_form_templates = {
        'password': 'implugin.auth.widgets:/templates/forms/password.jinja2',
        'text': 'implugin.auth.widgets:/templates/forms/text.jinja2',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.templates = dict(super().templates)
        self.templates.update(self._login_form_templates)
