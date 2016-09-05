import re
import logging
import datetime

from lxml.html import fromstring

from .api_adapter import ApiAdapter


class ApiClient(object):
	def __init__(self, username, password, logger=None):
		self.adapter = ApiAdapter(username, password)
		self.logger = logger if logger else logging.getLogger(__name__)

	def describe_resource_by_id(self, resource_id):
		resp = self.adapter.get(
			endpoint='MyPC/Front.aspx',
			params={
				'page': 'booking',
				'command': 'add',
				'userId': '',
				'resourceId': resource_id,
				'date': str(datetime.datetime.now().date()),
				'startTime': '00:00',
				'dialogId': 'dialog0'
			}
		)

		matches = fromstring(resp.text).xpath('//*[@id="startTime"]')
		children = [child.text for child in matches[0].getchildren()]
		
		return children

	def describe_resource_by_name(self, resource_name):
		pass

	def list_bookings(self):
		resp = self.adapter.get(
			endpoint='MyPC/Front.aspx',
			params={
				'page': 'search'
			}
		)
		tree = fromstring(resp.text)
		matches = tree.xpath('//*[@class="oddRow"]|//*[@class="evenRow"]')

		keys = ['booking_date', 'start_time', 'end_time', 'duration', 'site', 'location', 'resource', 'booking_id']
		bookings = []
		for match in matches:
			children = [child.text for child in match.getchildren()][:-1]
			booking_url = match.getchildren()[-1].getchildren()[0].attrib['href']
			booking_id = re.search('bookingId=(.*)&', booking_url).group(1)
			children.append(booking_id)

			booking = {}
			for i in range(len(children)):
				booking[keys[i]] = children[i]
			bookings.append(booking)

		return bookings

	def delete_booking(self, booking_id, email_receipt):
		resp = self.adapter.post(
			endpoint='MyPC/Front.aspx',
			params={
				'selfBooking': True,
				'page': 'booking',
				'command': 'delete',
				'bookingId': booking_id,	# Integer eg 2570658
				'emailReceipt': email_receipt	# Boolean
			}
		)

		# Get errors if they exist
		matches = fromstring(resp.text).xpath('//*[@class="expectedException"]')
		errors = [match.text for match in matches]

		if errors:
			raise Exception('Delete failed. Error: {}'.format(', '.join(errors)))
		# Success response javascript:refreshBookingStrip(210, false);HideDialog();
		if 'javascript:refreshBookingStrip' not in resp.text:
			raise Exception('Unexpected error: {}'.format(resp.text))

		return True

	def create_booking(self, start_time, end_time, booking_date, resource_id, email_receipt):
		resp = self.adapter.post(
			endpoint='MyPC/Front.aspx',
			params={
				'selfBooking': True,
				'startTime': start_time,	# Timestamp eg 00:00:00
				'endTime': end_time,		# Timestamp eg 00:00:00
				'emailReceipt': email_receipt,	# Boolean
				'date': booking_date,		# Date eg 20/08/2016
				'resourceId': resource_id,	# Integer eg 210
				'page': 'booking',
				'command': 'create',
			}
		)

		# Get errors if they exist
		matches = fromstring(resp.text).xpath('//*[@class="expectedException"]')
		errors = [match.text for match in matches]

		if errors:
			raise Exception('Booking failed. Error: {}'.format(', '.join(errors)))
		# Success response javascript:refreshBookingStrip(210, false);HideDialog();
		if 'javascript:refreshBookingStrip' not in resp.text:
			raise Exception('Unexpected error: {}'.format(resp.text))

		return True

	def server_status(self):
		resp = self.adapter.get(
			endpoint='MyPC/Front.aspx?page=getResourceStatesAPI'
		)

		return resp.status_code != 200 or not self._to_json(resp.text)

	def _to_json(self, text):
		try:
			return json.loads(text)
		except:
			return None

