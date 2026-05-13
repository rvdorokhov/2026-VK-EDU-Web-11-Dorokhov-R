from core.models import User
from questions.models import Tag
from django.db.models import Count, Sum, F


def get_popular_tags(limit=5):
    return (
        Tag.objects
        .annotate(question_count=Count('questions', distinct=True))
        .order_by('-question_count')[:limit]
    )

def get_best_members(limit=5):
    return (
        User.objects
        .select_related('profile')
        .annotate(
            question_count=Count('questions', distinct=True),
            answer_count=Count('answers', distinct=True)
        )
        .annotate(rating=F('question_count') + F('answer_count'))
        .order_by('-rating')[:limit]
    )