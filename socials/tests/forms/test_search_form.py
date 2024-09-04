"""Unit tests for the Search Form."""
from django.test import TestCase
from socials.models import User
from socials.forms import SearchForm
from django import forms

class SearchFormTestCase(TestCase):
    
    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.form_input = {'query' : 'jane'}
        
    def test_form_contains_correct_fields(self):
        form = SearchForm()
        self.assertIn('query', form.fields)
        query = form.fields['query']
        self.assertTrue(isinstance(query.widget,forms.TextInput))
        
    def test_form_accepts_valid_input(self):
        form = SearchForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_query_is_required(self):
        self.form_input['query'] = ''
        form = SearchForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_100_characters_is_accepted(self):
        self.form_input['query'] = 'o' * 100
        form = SearchForm(data = self.form_input)
        self.assertTrue(form.is_valid())
        
    def test_101_characters_is_not_accepted(self):
        self.form_input['query'] = 'o' * 101
        form = SearchForm(data = self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_placeholder_in_widget(self):
        form = SearchForm()
        placeholder = form.fields['query'].widget.attrs.get('placeholder')
        self.assertEqual(placeholder, 'Search...')
        