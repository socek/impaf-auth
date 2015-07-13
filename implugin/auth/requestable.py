from impaf.requestable import Requestable

from .models import NotLoggedUser


class AuthRequestable(Requestable):
    _not_logged_user_cls = NotLoggedUser

    def get_user(self):
        if not getattr(self, '_user', None):
            self._user = self._generate_user()
        return self._user

    def _generate_user(self):
        userid = self.request.unauthenticated_userid
        if userid is None:
            return self._not_logged_user_cls()
        else:
            self.Auth.get_by_id(userid)
