from datetime import datetime, timedelta
from django.conf import settings
# from django.contrib import auth
from base.auth import Auth


class AutoLogout:
    def process_request(self, request):
        if Auth.is_login(request):
            # Can't log out if not logged in
            try:
                if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                    Auth.logout(request)
                    return
            except KeyError:
                pass

        request.session['last_touch'] = datetime.now()
