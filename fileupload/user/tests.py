from django.test import TestCase
from .models import Question
# Create your tests here.
class QuestionTestCase(TestCase):
    def setUp(self):
        Question.objects.create(title='title')
        Question.objects.create(subject='subject')
        Question.objects.create(body='body')

    def test_question_test(self):
        obj1 = Question.objects.get(title='title')
        obj2 = Question.objects.get(subject='subject')
        obj3 = Question.objects.get(body='body')
        self.assertEqual(obj1.title, "title")
        self.assertEqual(obj2.subject, "subject")
        self.assertEqual(obj3.body, "body")

