"""Unit Tests for the View Mixins"""
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from socials.views import LoginProhibitedMixin

class LoginProhibitedMixinTestCase(TestCase):
	"""Unit Tests for the View Mixins"""

	def test_login_prohibited_throws_exception_when_not_configured(self):
		mixin = LoginProhibitedMixin()
		with self.assertRaises(ImproperlyConfigured):
			mixin.get_redirect_when_logged_in_url()