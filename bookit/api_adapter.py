import re
import logging
import requests

from .exceptions import LoginFailedException


class ApiAdapter(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

		self.logger = logging.getLogger(__name__)

		self._session = requests.Session()
		if self.username and self.password:
			self._do_login()
	
	def _do_login(self):
		login_string = '<Login><username>{}</username><password>{}</password><rememberMe>false</rememberMe><rememberView>-</rememberView></Login>'.format(self.username, self.password)
		login_resp = self.post(endpoint='cire/login.aspx', data=login_string)
		assert login_resp.status_code == 200
		
		match = re.search("\'http://bookit.unimelb.edu.au/(.*)\'", login_resp.text)
		if not match:
			raise Exception('Login failed. Check your username and password')
		verify_url = match.group(1)
		verify_resp = self.get(endpoint=verify_url)
		assert verify_resp.status_code == 200

	def post(self, endpoint, *args, **kwargs):
		return self._request(method=self._session.post, endpoint=endpoint, *args, **kwargs)

	def get(self, endpoint, *args, **kwargs):
		return self._request(method=self._session.get, endpoint=endpoint, *args, **kwargs)

	def _request(self, endpoint, method, *args, **kwargs):
		url = self._get_url(endpoint)
		return method(self._get_url(endpoint), *args, **kwargs)

	def _get_url(self, endpoint):
		return 'https://bookit.unimelb.edu.au/{}'.format(endpoint)

