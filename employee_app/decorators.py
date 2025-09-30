from django.contrib.auth.decorators import login_required, user_passes_test

def staff_required(view_func):
    """
    Ensures the user is both authenticated and is a staff member.
    """
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_staff)(view_func))
    return decorated_view_func
