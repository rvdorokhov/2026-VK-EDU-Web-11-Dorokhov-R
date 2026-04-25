from django.shortcuts import render
from django.templatetags.static import static

TAGS = [
    {
        'id': i,
        'name': f'tag{i}',
    }

    for i in range(5)
]

MEMBERS = [
    {
        'id': i,
        'name': f'User {i}',
        'url': 'http://127.0.0.1:8000/',
        'photo': static('core/img/user_placeholder.webp'),
    }

    for i in range(5)
]

def profile(request):
    return render(
        request,
        'core/profile.html',
        context={
            'tags': TAGS,
            'members': MEMBERS
        }
        )

def login(request):
    return render(
        request,
        'core/login.html',
        context={
            'tags': TAGS,
            'members': MEMBERS
        }
        )

def signup(request):
    return render(
        request,
        'core/signup.html',
        context={
            'tags': TAGS,
            'members': MEMBERS
        }
        )
