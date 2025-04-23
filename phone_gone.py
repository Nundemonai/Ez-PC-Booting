import scapy.all as scapy
import socket
import time
import datetime
import calendar
import conf
from wakeonlan import send_magic_packet
import subprocess

end_time = time.time() + 60 * 1


def turn_on_pc():
	send_magic_packet(conf.pc_mac_adress)
	print("sent package")

def turn_off_pc():
	pc = conf.pc_ip_address
	for Computer in pc:
		print(subprocess.getoutput("\nShutdown " + "-m " + "\\\\ " + Computer + " -f -r -t 0"))

def scan(ip):
	checker = []
	while time.time() < end_time:
		ans, _ = scapy.arping(ip)
		if ans:
			checker.append(ans.summary())
		else:
			turn_on_pc()
	
"""def check_weekend_weekday(date):
	try:
		given_date = datetime.datetime.strptime(date, '%d %m %Y')
		day_of_week = (given_date.weekday() + 1) % 7
		
		if day_of_week 5:
			day_type = 'weekday'
			
		else:
			ip = conf.phone_ip_adress
			day_type = 'weekend'
			scan(ip)

	except ValueError as e:
		print("error: ", e)"""

if __name__ == "__main__":
	ip = conf.phone_ip_adress
	last_detected_time = time.time()
	# check_weekend_weekday()
	try:
		while True:
			if not scan(ip):
				current_time = time.time()
				offline_duration = current_time - last_detected_time
				
				if offline_duration >= end_time:
					turn_off_pc()
					print(f"\nPhone has been offline for {offline_duration / 60:.2f} minutes. Shutting down the PC.")
				
				else:
					last_detected_time = time.time()
					turn_on_pc(conf.pc_mac_adress)
				time.sleep(5)
	except Exception as e:
		print("\nEncountered an error: ", e)
