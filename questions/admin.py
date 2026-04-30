from django.contrib import admin

from questions.models import Question, Tag, QuestionTag, Answer, AnswerVote, QuestionVote


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "short_description",
        "creation_time",
        "vote_count",

        "user__id",
        "user__email",
    )

    list_select_related = (
        "user",
    )

    raw_id_fields = (
        "user",
    )

    search_fields = (
        "id",
        "title",
        "description",

        "user__id",
        "user__email",
    )

    list_filter = (
        "creation_time",
    )

    class AnswerInline(admin.TabularInline):
        model = Answer

        fields = (
            "answer_text",
            "user",
            "is_correct",
            "vote_count",
            "creation_time",
        )

        readonly_fields = (
            "vote_count",
            "creation_time",
            "user",
        )

        raw_id_fields = (
            "question",
            "user",
        )

        extra = 0

    inlines = (AnswerInline, )

    @admin.display(description="Описание вопроса")
    def short_description(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + "..."
        return obj.description



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "id",
        "name",
    )



@admin.register(QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    list_display = (
        "id",

        "question__id",
        "question",

        "tag__id",
        "tag",
    )

    list_select_related = (
        "question",
        "tag",
    )

    raw_id_fields = (
        "question",
        "tag",
    )

    search_fields = (
        "id",

        "question__id",
        "question__title",

        "tag__id",
        "tag__name",
    )



@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_answer_text",
        "creation_time",
        "is_correct",
        "vote_count",

        "user__id",
        "user__email",

        "question__id",
        "question",
    )

    list_select_related = (
        "user",
        "question",
    )

    raw_id_fields = (
        "question",
        "user",
    )

    search_fields = (
        "id",
        "answer_text",

        "user__id",
        "user__email",

        "question__id",
        "question__title",
    )

    list_filter = (
        "is_correct",
        "creation_time",
    )

    @admin.display(description="Текст ответа")
    def short_answer_text(self, obj):
        if len(obj.answer_text) > 50:
            return obj.answer_text[:50] + "..."
        return obj.answer_text



@admin.register(AnswerVote)
class AnswerVoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "value",

        "user__id",
        "user__email",

        "answer__id",
        "answer__answer_text",
    )

    list_select_related = (
        "user",
        "answer",
    )

    raw_id_fields = (
        "user",
        "answer",
    )

    search_fields = (
        "id",

        "user__id",
        "user__email",

        "answer__id",
        "answer__answer_text",
    )

    list_filter = (
        "value",
    )



@admin.register(QuestionVote)
class QuestionVoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "value",

        "user__id",
        "user__email",

        "question__id",
        "question",
    )

    list_select_related = (
        "user",
        "question",
    )

    raw_id_fields = (
        "user",
        "question",
    )

    search_fields = (
        "id",

        "user__id",
        "user__email",

        "question__id",
        "question__title",
    )

    list_filter = (
        "value",
    )