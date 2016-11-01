
class Auth(object):
    @staticmethod
    def require_login(request):
        if 'is_login' in request.session:
            return request.session['user']

    @staticmethod
    def is_login(request):
        if 'is_login' in request.session:
            return True
        return False

    @staticmethod
    def login(request, user):
        request.session['is_login'] = True
        # request.session['user'] = user
        request.session['user_unique_id'] = user.unique_id

    @staticmethod
    def logout(request):
        if 'is_login' in request.session:
            del request.session['is_login']
        if 'user' in request.session:
            del request.session['user']
        if 'user_unique_id' in request.session:
            del request.session['user_unique_id']
        if 'account_type' in request.session:
            del request.session['account_type']

    # Web
    @staticmethod
    def get_login_user_instance(request):
        if 'is_login' in request.session:
            # uid = request.session['user']['pk']
            uid = request.session['user_unique_id']
            account_type = request.session['account_type']
        return None
