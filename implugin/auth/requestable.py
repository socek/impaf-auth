from implugin.sqlalchemy.requestable import SqlalchemyRequestable

from .models import NotLoggedUser


class AuthRequestable(SqlalchemyRequestable):
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
            return self.drivers.Auth.get_by_id(userid)
