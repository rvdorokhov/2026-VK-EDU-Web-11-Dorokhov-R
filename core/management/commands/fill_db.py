import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from faker import Faker

from core.models import User, Profile
from questions.models import (
    Answer,
    AnswerVote,
    Question,
    QuestionTag,
    QuestionVote,
    Tag,
)


class Command(BaseCommand):
    help = "Fill database with fake test data"

    LIMIT = 1000
    BATCH_SIZE = 2500

    QUESTIONS_COEF = 10
    ANSWERS_COEF = 10
    TAGS_COEF = 1
    VOTES_COEF = 200

    TAGS_PER_QUESTION = 5

    UP_PROBABILITY = 0.7
    DOWN_PROBABILITY = 0.3

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        ratio = options["ratio"]

        if options["clear"]:
            self.clear_database()

        fake = Faker("ru_RU")

        for start in range(0, ratio, self.LIMIT):
            end = min(start + self.LIMIT, ratio)

            self.stdout.write(f"Создаю данные: {start}..{end}")

            created_users = self.fill_users(fake, start, end)
            self.fill_profiles(fake, created_users)

            created_tags = self.fill_tags(fake, start, end)

            created_questions = self.fill_questions(fake, created_users)
            self.fill_question_tags(created_questions, created_tags)

            created_answers = self.fill_answers(fake, created_questions, created_users)

            self.fill_question_votes(created_questions, created_users)
            self.fill_answer_votes(created_answers, created_users)

        self.stdout.write(self.style.SUCCESS("База успешно заполнена"))

    def fill_users(self, fake, start, end):
        password_hash = make_password("vk_education")

        users_to_create = []

        for i in range(start, end):
            users_to_create.append(
                User(
                    username=f"user_{i}",
                    email=f"user_{i}@mail.ru",
                    password=password_hash,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    is_active=True,
                )
            )

        return User.objects.bulk_create(
            users_to_create,
            batch_size=self.BATCH_SIZE,
        )

    def fill_profiles(self, fake, users):
        profiles_to_create = []

        for user in users:
            profiles_to_create.append(
                Profile(
                    user=user,
                    nickname=f"{fake.user_name()}_{user.id}"[:64],
                    avatar="avatars/user_placeholder.webp",
                )
            )

        return Profile.objects.bulk_create(
            profiles_to_create,
            batch_size=self.BATCH_SIZE,
        )

    def fill_tags(self, fake, start, end):
        tags_to_create = []

        for i in range(start, end):
            for j in range(self.TAGS_COEF):
                fake_part = fake.word()[:12]
                tag_name = f"tag_{i}_{j}_{fake_part}"[:32]

                tags_to_create.append(
                    Tag(
                        name=tag_name,
                    )
                )

        return Tag.objects.bulk_create(
            tags_to_create,
            batch_size=self.BATCH_SIZE,
        )

    def fill_questions(self, fake, users):
        questions_to_create = []

        for user in users:
            for _ in range(self.QUESTIONS_COEF):
                questions_to_create.append(
                    Question(
                        title=fake.sentence(nb_words=8)[:1028],
                        description=fake.paragraph(nb_sentences=5),
                        user=user,
                        answers_count=self.ANSWERS_COEF, # в будущем это поле будет инкреметиться при добавлении ответа на уровне бэка, пока так
                    )
                )

        return Question.objects.bulk_create(
            questions_to_create,
            batch_size=self.BATCH_SIZE,
        )

    def fill_question_tags(self, questions, tags):
        question_tags_to_create = []

        tags_count = len(tags)

        if tags_count == 0:
            return []

        tags_per_question = min(tags_count, self.TAGS_PER_QUESTION)

        for question in questions:
            for i in range(tags_per_question):
                tag = tags[(question.id + i) % tags_count]

                question_tags_to_create.append(
                    QuestionTag(
                        question=question,
                        tag=tag,
                    )
                )

        return QuestionTag.objects.bulk_create(
            question_tags_to_create,
            batch_size=self.BATCH_SIZE,
        )

    def fill_answers(self, fake, questions, users):
        answers_to_create = []

        users_count = len(users)

        if users_count == 0:
            return []

        for question in questions:
            for i in range(self.ANSWERS_COEF):
                user = users[(question.id + i) % users_count]

                answers_to_create.append(
                    Answer(
                        answer_text=fake.paragraph(nb_sentences=4),
                        is_correct=(i == 0),
                        user=user,
                        question=question,
                    )
                )

        return Answer.objects.bulk_create(
            answers_to_create,
            batch_size=self.BATCH_SIZE,
        )

    def fill_question_votes(self, questions, users):
        question_votes_to_create = []
        questions_to_update = []

        users_count = len(users)

        if users_count == 0:
            return

        votes_per_question = min(
            self.get_votes_per_question(),
            users_count,
        )

        for question in questions:
            current_vote_count = 0

            for i in range(votes_per_question):
                user = users[(question.id + i) % users_count]

                value = random.choices(
                    [QuestionVote.UP, QuestionVote.DOWN],
                    weights=[self.UP_PROBABILITY, self.DOWN_PROBABILITY],
                    k=1,
                )[0]

                current_vote_count += value

                question_votes_to_create.append(
                    QuestionVote(
                        question=question,
                        user=user,
                        value=value,
                    )
                )

                if len(question_votes_to_create) >= self.BATCH_SIZE:
                    QuestionVote.objects.bulk_create(
                        question_votes_to_create,
                        batch_size=self.BATCH_SIZE,
                    )
                    question_votes_to_create.clear()

            question.vote_count = current_vote_count
            questions_to_update.append(question)

            if len(questions_to_update) >= self.BATCH_SIZE:
                Question.objects.bulk_update(
                    questions_to_update,
                    ["vote_count"],
                    batch_size=self.BATCH_SIZE,
                )
                questions_to_update.clear()

        if question_votes_to_create:
            QuestionVote.objects.bulk_create(
                question_votes_to_create,
                batch_size=self.BATCH_SIZE,
            )

        if questions_to_update:
            Question.objects.bulk_update(
                questions_to_update,
                ["vote_count"],
                batch_size=self.BATCH_SIZE,
            )

    def fill_answer_votes(self, answers, users):
        answer_votes_to_create = []
        answers_to_update = []

        users_count = len(users)

        if users_count == 0:
            return

        votes_per_answer = min(
            self.get_votes_per_answer(),
            users_count,
        )

        for answer in answers:
            current_vote_count = 0

            for i in range(votes_per_answer):
                user = users[(answer.id + i) % users_count]

                value = random.choices(
                    [AnswerVote.UP, AnswerVote.DOWN],
                    weights=[self.UP_PROBABILITY, self.DOWN_PROBABILITY],
                    k=1,
                )[0]

                current_vote_count += value

                answer_votes_to_create.append(
                    AnswerVote(
                        answer=answer,
                        user=user,
                        value=value,
                    )
                )

                if len(answer_votes_to_create) >= self.BATCH_SIZE:
                    AnswerVote.objects.bulk_create(
                        answer_votes_to_create,
                        batch_size=self.BATCH_SIZE,
                    )
                    answer_votes_to_create.clear()

            answer.vote_count = current_vote_count
            answers_to_update.append(answer)

            if len(answers_to_update) >= self.BATCH_SIZE:
                Answer.objects.bulk_update(
                    answers_to_update,
                    ["vote_count"],
                    batch_size=self.BATCH_SIZE,
                )
                answers_to_update.clear()

        if answer_votes_to_create:
            AnswerVote.objects.bulk_create(
                answer_votes_to_create,
                batch_size=self.BATCH_SIZE,
            )

        if answers_to_update:
            Answer.objects.bulk_update(
                answers_to_update,
                ["vote_count"],
                batch_size=self.BATCH_SIZE,
            )

    def get_votes_per_answer(self):
        objects_per_user = self.QUESTIONS_COEF + self.QUESTIONS_COEF * self.ANSWERS_COEF

        return max(1, self.VOTES_COEF // objects_per_user)

    def get_votes_per_question(self):
        votes_per_answer = self.get_votes_per_answer()

        answers_per_user = self.QUESTIONS_COEF * self.ANSWERS_COEF
        remaining_votes = self.VOTES_COEF - answers_per_user * votes_per_answer

        return max(1, remaining_votes // self.QUESTIONS_COEF)

    def clear_database(self):
        AnswerVote.objects.all().delete()
        QuestionVote.objects.all().delete()
        Answer.objects.all().delete()
        QuestionTag.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()