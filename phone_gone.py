import scapy.all as scapy
import time
from wakeonlan import send_magic_packet
import paramiko
import conf
import logging

# Configure logging to avoid excessive output from Scapy
logging.getLogger("scapy").setLevel(logging.CRITICAL)

class Wolconnectivity:
    def __init__(self):
        self.username = conf.username
        self.password = conf.password
        self.pc_mac = conf.pc_mac_adress
        self.pc_ip = conf.pc_ip_address
        self.phone_ip = conf.phone_ip_address

    def turn_on_pc(self):
        send_magic_packet(self.pc_mac)
        print("Sent magic packet to PC")
        time.sleep(15)

    def turn_off_pc(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.pc_ip, username=self.username, password=self.password)
            logging.info(f"Connected to PC at {self.pc_ip}")
            shutdown_command = 'shutdown /s /t 0'
            
            ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(shutdown_command)
            logging.info(f"Executed command: {shutdown_command}")
            
            stdout = ssh_stdout.read().decode()
            stderr = ssh_stderr.read().decode()
            
            if stdout:
                logging.info(f"SSH Command output:\n{stdout}")
            if stderr:
                logging.error(f"SSH Command Error:\n{stderr}")
        except Exception as e:
            logging.error(f"Error Connecting via SSH: {e}")
        finally:
            client.close()
            logging.info("closed SSH Connection")

    def check_phone_presence(self):
        ans = scapy.arping(self.phone_ip, verbose=False)[0]
        for sent, received in ans.res:
            if received.psrc == self.phone_ip:
                print("Phone found\n", ans)
                return True
        print("Phone not found\n", ans)
        return False 

if __name__ == "__main__":
    wol = Wolconnectivity()
    
    while True:
        if wol.check_phone_presence():
            wol.turn_on_pc()
        else:
            print("Phone not found. Waiting for 1 more hour to confirm absence...")
            time.sleep(30)  # Wait 1 hour before confirming absence
            for i in range(60):
                print(i)
                if wol.check_phone_presence():
                    print("Phone found again, not closing the PC off.")
                    break
            else:
                print("Phone still not found after confirmation period. Turning off PC...")
                wol.turn_off_pc()
        
        time.sleep(30)  # Check every hour
