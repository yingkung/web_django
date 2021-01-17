from polls.models import Choice, Question
import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

class QuestionMoelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() return False for questions whose pub_date is in the future.
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)  # 创建一个出版时间在未来的Question
        self.assertIs(future_question.was_published_recently(), False)  # 对于出版时间在外来的记录，返回值应该是False

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() return False for questions whose pub_date is in the future.
        :return:
        """
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)  # 创建一个出版时间超过1天的Question
        self.assertIs(old_question.was_published_recently(), False)  # 对于出版时间超过1天的记录，返回值应该是False

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day
        :return:
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    '''
    创建一个question记录
    :param question_text:
    :param days:
    :return:
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """如果没有question，页面显示提示"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['last_question_list'], [])

    def test_past_question(self):
        """针对过去时间的question"""
        create_question('Past Question.', days=-30)  # 创建一个过去的问题
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['last_question_list'], ['<Question: Past Question.>'])

    def test_future_question(self):
        """针对未来时间的question"""
        create_question('Future Question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['last_question_list'], [])  # 如果创建时间为未来，则不会被筛选出来

    def test_future_question_and_past_question(self):
        """如果同时存在past question 和 future question， 只有past question 可以被筛选出来"""
        create_question('Past Question.', days=-30)
        create_question('Future Question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['last_question_list'], ['<Question: Past Question.>'])

    def test_two_past_questions(self):
        """存在多个符合要求的question"""
        create_question('Past Question1.', days=-30)
        create_question('Past Question2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['last_question_list'], ['<Question: Past Question2.>', '<Question: Past Question1.>'])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """如果出版日期在未来则返回404页面"""
        future_question = create_question('Future Question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """如果出版日期是在过去，则正常显示"""
        past_question = create_question('Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)