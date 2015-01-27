# Test
from django.test import TestCase, Client

# App
from base.forms import AddProjectForm

# Utility
from django.core.urlresolvers import reverse

def form_errors(response):
    return response.context['form'].errors

class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()


    @classmethod
    def get(view_name, *args, **kwargs):
        return self.client.get(reverse(view_name), *args, **kwargs)

    @classmethod
    def post(view_name, *args, **kwargs):
        return self.client.post(reverse(view_name), *args, **kwargs)


    def test_front_page(self):
        response = self.client.get('/', follow=True)
        assert 'base/index.html' in response.template_name


    def test_project_page(self):
        response = self.client.post(reverse('base:add_project'),
            follow=True)
        assert 'base/add_project.html' in response.template_name


    def test_add_project_no_name(self):
        response = self.client.post(reverse('base:add_project'),
            {'description': 'cats cats cats',
             'icon': 'fa-arrows'}, follow=True)
        assert 'This field is required.' in form_errors(response)['name']


    def test_add_project_no_description(self):
        response = self.client.post(reverse('base:add_project'),
            {'name': 'CATS!',
             'icon': 'fa-arrows'}, follow=True)
        assert 'This field is required.' in form_errors(response)['description']


    def test_add_project(self):
        response = self.client.post(reverse('base:add_project'),
            {'name': 'CATS!',
             'description': 'cats cats cats',
             'icon': 'fa-arrows'}, follow=True)
        assert 'base/index.html' in response.template_name
        assert b'CATS!' in response.content


class TestForms(TestCase):

    def test_project_form(self):
        form_data = {
            'name': 'CATS!',
            'description': 'cats cats cats',
            'icon': 'fa-arrows'}
        form = AddProjectForm(data=form_data)
        assert form.is_valid()

