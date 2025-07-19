import scapy.all as scapy
import time
import conf
from wakeonlan import send_magic_packet
import paramiko
import sys
import logging

logging.getLogger("scapy").setLevel(logging.CRITICAL)

class Wolconnectivity:
    def __init__(self):
        self.t_end = time.time() + 60 * 1
        self.username = conf.username
        self.password = conf.password
        self.pc_mac = conf.pc_mac_adress
        self.pc_ip = conf.pc_ip_address
        self.phone_ip = conf.phone_ip_address

    def turn_on_pc(self):
        send_magic_packet(self.pc_mac)
    
        print("sent package")
        time.sleep(15)


    def turn_off_pc(self):
        client = paramiko.SSHClient()
        client.load.system_host_keys()
        client.connect(f"{self.pc_ip}", username=f"{self.username}", password=f"{self.password}")
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("ss -ltn")

        for line in ssh_stdout:
            results.append(line.strip('\n'))
        t_end = time.time() + 60 * 1
        while time.time() < t_end:
            self.phone_found(self.phone)

    def phone_found(self):
        ip = self.phone_ip
        while True:
            ans = scapy.arping(self.phone_ip)
            if ans:
                print("Found the Phone")
                self.turn_on_pc()
            if not ans:
                print("Did not find the phone,\n Waiting for an hour...")
                while self.time.time() < t_end:
                    if ans:
                        self.phone_found()
                    if not ans:
                        self.turn_off_pc()

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
    wol = Wolconnectivity()
    wol.phone_found()



