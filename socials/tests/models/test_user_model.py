"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from socials.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'socials/tests/fixtures/default_user.json',
        'socials/tests/fixtures/other_users.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username = 'johndoe')
        self.other = User.objects.get(username = 'janedoe')
        
    def test_valid_user(self):
        self._assert_user_is_valid()
        
    def test_invalid_user(self):
        self.user.username = '@kjdskfk'
        self._assert_user_is_invalid()
        
    def test_unique_username(self):
        self.user.username = 'janedoe'
        self._assert_user_is_invalid()
        
    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()
        
    def test_username_only_includes_alphanumericals_and_select_symbols(self):
        self.user.username = '-ksgA80138KM__'
        self._assert_user_is_valid()
        
    def test_username_does_not_include_invalid_symbols(self):
        self.user.username = '#jkAp@*jghdg16'
        self._assert_user_is_invalid()
        
    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()
        
    def test_first_name_only_includes_alphabets(self):
        self.user.first_name = 'Bob'
        self._assert_user_is_valid()
        
    def test_first_name_cannot_include_symbols_or_numbers(self):
        self.user.first_name = 'Bob123##'
        
    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()
        
    def test_last_name_only_includes_alphabets(self):
        self.user.last_name = 'Smith'
        self._assert_user_is_valid()
        
    def test_last_name_canot_include_symbols_or_numbers(self):
        self.user.last_name = 'SMITH123##'
        self._assert_user_is_invalid()
        
    def test_email_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()
        
    def test_email_must_be_unique(self):
        self.user.email = self.other.email
        self._assert_user_is_invalid()
        
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()