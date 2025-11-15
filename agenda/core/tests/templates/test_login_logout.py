from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.forms import LoginForm
from django.urls import reverse

# -----------------------------------------------------------------
# TESTE DE LOGIN (POST)
# -----------------------------------------------------------------

class Login_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('senha1234')
        new_user.save()

        self.data = {'email':'aluno.fatec@fatec.sp.gov.br', 'senha':'senha1234'}

    def test_response_redirects(self):
        response = self.client.post(r('login'), self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_login_redirects_to_home(self):
        response = self.client.post(r('login'), self.data)
        self.assertRedirects(response, r('home'))

    def test_template_used_after_follow(self):
        response = self.client.post(r('login'), self.data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')


# -----------------------------------------------------------------
# TESTE DE LOGIN (POST FALHA)
# -----------------------------------------------------------------

class Login_Fail_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('SENHA_CORRETA')
        new_user.save()
        
        data = {
            'email':'aluno.fatec@fatec.sp.gov.br', 
            'senha':'senha1234_errada' 
        }
        self.resp = self.client.post(r('login'), data)

    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'login.html')


# -----------------------------------------------------------------
# TESTE DE LOGIN (GET)
# -----------------------------------------------------------------

class Login_GET_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.logout() 
        self.resp = self.client.get(r('login'))

    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'login.html')

    def test_context(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, LoginForm)


# -----------------------------------------------------------------
# TESTE DE LOGOUT (GET)
# -----------------------------------------------------------------
class Logout_Get_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('senha1234')
        new_user.save()
        self.client.login(username="admin", password="senha1234")
        self.resp = self.client.get(r('logout'))

    def test_response(self):
        self.assertEqual(self.resp.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'logout.html')


# -----------------------------------------------------------------
# TESTE DE LOGOUT (POST)
# -----------------------------------------------------------------
class Logout_Post_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='aluno.fatec@fatec.sp.gov.br',username='admin')
        new_user.set_password('senha1234')
        new_user.save()
        self.client.login(username="admin", password="senha1234")
        
    def test_response(self):
        response = self.client.post(r('logout'))
        self.assertEqual(response.status_code , HTTPStatus.OK)
    
    def test_template_used(self):
        response = self.client.post(r('logout'))
        self.assertTemplateUsed(response, 'logout.html')