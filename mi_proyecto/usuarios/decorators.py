from django.contrib.auth.decorators import user_passes_test

def rango_superior_required(login_url=None):
    return user_passes_test(
        lambda u: u.is_authenticated and u.rango == 'superior', login_url=login_url
    )
