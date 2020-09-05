from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuth(SessionAuthentication):
    '''
    Can be used for django rest framework views that
    are safe to disable csrf on http://stackoverflow.com/a/30875830
    '''

    def enforce_csrf(self, request):
        return
