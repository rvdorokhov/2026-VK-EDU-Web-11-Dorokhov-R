from django.conf import settings
from django.db import models

class Question(models.Model):
    title = models.CharField(verbose_name="Заголовок вопроса", max_length=1028)
    description = models.TextField(verbose_name="Описание вопроса")
    creation_time = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    vote_count = models.IntegerField(verbose_name="Рейтинг голосов ↑ / ↓", default=0)
    answers_count = models.PositiveIntegerField(verbose_name="Количество ответов", default=0) 

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="questions"
    )

    tags = models.ManyToManyField(
        "Tag",
        through="QuestionTag",
        related_name="questions",
        blank=True,
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title



class Tag(models.Model):
    name = models.CharField(verbose_name="Название тега", unique=True, max_length=32)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name



class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Связь вопросы-теги"
        verbose_name_plural = "Связи вопросы-теги"
        unique_together = ('question', 'tag')

    def __str__(self):
        return f"{str(self.question)[:50]} - {self.tag}"



class Answer(models.Model):
    answer_text = models.TextField(verbose_name="Текст ответа")
    creation_time = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    is_correct = models.BooleanField(verbose_name="Выбран ли автором как правильный", default=False)
    vote_count = models.IntegerField(verbose_name="Рейтинг голосов ↑ / ↓", default=0)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.answer_text[:50]


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = [
        (UP, "Голос вверх"),
        (DOWN, "Голос вниз"),
    ]

    value = models.IntegerField(verbose_name="Значение голоса", choices=VALUE_CHOICES)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True



class AnswerVote(Vote):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Голос за ответ"
        verbose_name_plural = "Голоса за ответ"
        unique_together = ('answer', 'user')

    def __str__(self):
        return f"{self.answer} - {self.user} - {self.get_value_display()}"



class QuestionVote(Vote):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Голос за вопрос"
        verbose_name_plural = "Голоса за вопрос"
        unique_together = ('question', 'user')

    def __str__(self):
        return f"{self.question} - {self.user} - {self.get_value_display()}"