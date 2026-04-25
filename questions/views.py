from django.shortcuts import render
from .utils import paginate
from .utils import find_tag_by_name
from .utils import find_question_by_id
from .utils import get_filtred_questions
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

QUESTIONS = [
    {
        'id': i,
        'title': f'Вопрос {i}',
        'text': f'Текст {i}',
        'vote_count': i,
        'number_of_answers': f'ответов: {i}',
        'date': '16 марта 12:40',
        'user': MEMBERS[i % 5],
        'tags': [TAGS[i % 5], TAGS[(i + 1) % 5], TAGS[(i + 2) % 5]]
    }

    for i in range(100)
]

ANSWERS = [
    {
        'id': i,
        'text': f'Ответ {i}',
        'vote_count': i,
        'date': '16 марта 12:40',
        'is_correct': False,
        'user': MEMBERS[i % 5]
    }

    for i in range(100)
]

def index(request):
    page_obj = paginate(QUESTIONS, request)

    return render(
        request,
        'questions/index.html',
        context={
            'questions': page_obj.object_list,
            'page_obj': page_obj,
            'tags': TAGS,
            'members': MEMBERS
        }
        )

def hot(request):
    page_obj = paginate(QUESTIONS, request)

    return render(
        request,
        'questions/hot.html',
        context={
            'questions': page_obj.object_list,
            'page_obj': page_obj,
            'tags': TAGS,
            'members': MEMBERS
        }
        )


def ask(request):
    return render(
        request,
        'questions/ask.html',
        context={
            'questions': QUESTIONS[::10],
            'tags': TAGS,
            'members': MEMBERS
        }
        )

def tag(request, tag_name):
    filtered_questions = get_filtred_questions(QUESTIONS, tag_name)

    cur_tag = find_tag_by_name(TAGS, tag_name)

    page_obj = paginate(filtered_questions, request)

    return render(
        request,
        'questions/tag.html',
        context={
            'questions': page_obj.object_list,
            'page_obj': page_obj,
            'tag_name': tag_name,
            'tags': TAGS,
            'members': MEMBERS
        }
        )

def question(request, question_id):
    page_obj = paginate(QUESTIONS, request)

    question = find_question_by_id(QUESTIONS, question_id)

    return render(
        request,
        'questions/question.html',
        context={
            'tags': TAGS,
            'members': MEMBERS,
            'question': question,
            'answers': page_obj.object_list,
            'page_obj': page_obj,
        }
        )