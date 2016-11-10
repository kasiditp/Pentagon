import hashlib

from django.http import request
from django.test import TestCase

from base.auth import Auth
from member.models import User
from django.test import Client
# Create your tests here.


class UserLoginTestCase(TestCase):
    def setUp(self):
        User.objects.create(unique_id='000001', username='test',
                            password=hashlib.md5('123456').hexdigest(),
                            email='test@hotmail.com', sex='1', birth_date='1999-01-01', first_name='aaaa',
                            last_name='bbbb', address='123/222',
                            image='member/images/default_user_profile.jpg', type=1)
        User.objects.create(unique_id='000001', username='admin',
                            password=hashlib.md5('123456').hexdigest(),
                            email='test@hotmail.com', sex='1', birth_date='1999-01-01', first_name='aaaa',
                            last_name='bbbb', address='123/222',
                            image='member/images/default_user_profile.jpg', type=2)
        self.client = Client()

    def test_user_can_login(self):
        print 'Test User Login'
        response = self.client.post('/member/login/', {"username": 'test', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='test', password=hashlib.md5('123456').hexdigest())
        self.assertEqual(user.unique_id, '000001')

    def test_admin_login(self):
        print 'Test Admin Login'
        user = User.objects.get(username='admin', password=hashlib.md5('123456').hexdigest())
        self.assertEqual(user.unique_id, '000001')


class RegisterTestCase(TestCase):

    def test_register(self):
        print 'Test Register'
        user = User.objects.create(unique_id='000001', username='test',
                            password=hashlib.md5('123456').hexdigest(),
                            email='test@hotmail.com', sex='1', birth_date='1999-01-01', first_name='aaaa',
                            last_name='bbbb', address='123/222',
                            image='member/images/default_user_profile.jpg', type=1)
        self.assertEqual(user.unique_id, '000001')