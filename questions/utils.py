from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage
from django.http import Http404

PAGE_SIZE = 10

def paginate(objects_list, request, per_page=PAGE_SIZE):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return page_obj

def get_filtred_questions(questions, filter_tag):
    new_questions = []

    for question in questions:
        for tag in question['tags']:
            if tag['name'] == filter_tag:
                new_questions.append(question)
                break

    return new_questions

def find_tag_by_name(tags, tag_name):
    for tag in tags:
        if tag['name'] == tag_name:
            return tag

    raise Http404("Такого тега не существует")

def find_question_by_id(questions, question_id):
    for question in questions:
        if question['id'] == question_id:
            return question

    raise Http404("Такого вопроса не существует")

