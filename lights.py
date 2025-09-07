from tuya_connector import TuyaOpenAPI
from requests import get, post
from conf import tuya_ACCESS_ID, tuya_ACCESS_KEY, tuya_ENDPOINT, tuya_USERNAME, tuya_PASSWORD, tuya_DEVICE1, tuya_DEVICE2, tuya_DEVICE3, tuya_DEVICE4

ACCESS_ID = tuya_ACCESS_ID
ACCESS_KEY = tuya_ACCESS_KEY

ENDPOINT = tuya_ENDPOINT

USERNAME = tuya_USERNAME
PASSWORD = tuya_PASSWORD


DEVICE1 = tuya_DEVICE1
DEVICE2 = tuya_DEVICE2
DEVICE3 = tuya_DEVICE3
DEVICE4 = tuya_DEVICE4

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

class Light:
	def __init__(self):
		self.lights = False
		
	def switch_on(self):
		if not self.lights:
			self.lights = True
			self.lights_if_on()

	def switch_off(self):
		if self.lights:
			self.lights = False
			self.lights_if_off()
			
	def lights_if_on(self):
		if self.lights:
			commands = {'commands': [{'code': 'switch_led', 'value': True}]}
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE1}/commands", commands)
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE2}/commands", commands)
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE3}/commands", commands)
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE4}/commands", commands)

	def lights_if_off(self):
		if not self.lights:
			commands = {'commands': [{'code': 'switch_led', 'value': False}]}
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE1}/commands", commands)
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE2}/commands", commands)
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE3}/commands", commands)
			openapi.post(f"/v1.0/iot-03/devices/{DEVICE4}/commands", commands)
