from django.shortcuts import render

from core.models import User


def profile(request):
    user_obj = ( # пока что так, пока нет полноценной авторизации
        User.objects
        .select_related("profile")
        .filter(profile__isnull=False)
        .order_by("id")
        .first()
    )

    return render(
        request,
        'core/profile.html',
        context= {
            'user': user_obj,
        }
        )

def login(request):
    return render(
        request,
        'core/login.html',
        context={

        }
        )

def signup(request):
    return render(
        request,
        'core/signup.html',
        context={

        }
        )
