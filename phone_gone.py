import time
from wakeonlan import send_magic_packet
import paramiko
import conf
import logging
from lights import Light
import subprocess
import threading

# Configure logging to avoid excessive output from Scapy
logging.basicConfig(
    level=logging.DEBUG,
    filename='logs.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('Wolconnectivity')

class Wolconnectivity:
    def __init__(self):
        self.username = conf.username
        self.password = conf.password
        self.pc_mac = conf.pc_mac_adress
        self.pc_ip = conf.pc_ip_address
        self.phone_ip = conf.phone_ip_address
        self.on_off = True
        self.successfull_ping = 0
        self.running = True
        
        # self.on_off = True
        
    def switch_on(self):
        if not self.on_off:
            self.turn_on_pc()
            self.on_off = True
    
    def switch_off(self):
        if self.on_off:
            self.turn_off_pc()
            self.on_off = False

    def turn_on_pc(self):
        send_magic_packet(self.pc_mac)
        logger.info(f"Sent magic packet to PC")
        lights.lights_on()
        # time.sleep(15)
        return True

    def turn_off_pc(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.pc_ip, username=self.username, password=self.password)
            logger.info(f"Connected to PC at {self.pc_ip}")
            shutdown_command = 'shutdown /s /t 0'
            
            ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(shutdown_command)
            logger.info(f"Executed command: {shutdown_command}")
            
            stdout = ssh_stdout.read().decode()
            stderr = ssh_stderr.read().decode()
            
            if stdout:
                logger.info(f"SSH Command output:\n{stdout}")
            if stderr:
                logger.error(f"SSH Command Error:\n{stderr}")
        except Exception as e:
            logger.error(f"Error Connecting via SSH: {e}")
        finally:
            client.close()
            logger.info("closed SSH Connection")

    def ping_phone_to_lights(self):
        self.successfull_ping = 0
        try:
            output = subprocess.run(['ping', '-c', '1', self.phone_ip], stderr=subprocess.STDOUT)
            # print("\n", output.returncode, "\n")
            if output.returncode == 0:
                self.successfull_ping += 1
                return output.returncode
            else:
                for i in range(899):
                    
                    output2 = subprocess.run(['ping', '-c', '1', self.phone_ip], stderr=subprocess.STDOUT)
                    print("repetition: ", i, "return code: ", output2.returncode)
                    time.sleep(1)
                    self.successfull_ping += 1
                    if output2.returncode == 0:
                        return output2.returncode
        
        except subprocess.CalledProcessError as e:
            print(e)

    def ping_phone_to_PC(self):
        self.successfull_ping = 0
        try:
            output = subprocess.run(['ping', '-c', '1', self.phone_ip], stderr=subprocess.STDOUT)
            # print("\n", output.returncode, "\n")
            if output.returncode == 0:
                self.successfull_ping += 1
                return output.returncode
            else:
                for i in range(3599):
                    
                    output2 = subprocess.run(['ping', '-c', '1', self.phone_ip], stderr=subprocess.STDOUT)
                    print("repetition: ", i, "return code: ", output2.returncode)
                    time.sleep(1)
                    self.successfull_ping += 1
                    if output2.returncode == 0:
                        return output2.returncode
        
        except subprocess.CalledProcessError as e:
            print(e)

    def check_lights(self):
        while True:
            return_code = self.ping_phone_to_lights()
            if return_code == 0:
                logger.info(f"\n------\n[Lights]: Phone is reachable. Keep lights on\n{self.ping_phone_to_lights()}\n------")
                lights.switch_on()
                time.sleep(15)
            else:
                logger.info("f[Lights]: Turning them off")
                lights.switch_off()
                time.sleep(15)

    def check_pc(self):
        while True:
            return_code = self.ping_phone_to_PC()
            if return_code == 0:
                logger.info(f"\n------\n[PC]: Phone is reachable. Keep lights on\n{self.ping_phone_to_PC()}\n------")
                self.switch_on()
                time.sleep(15)
            else:
                logger.info("f[PC]: Turning it off")
                self.switch_off()
                time.sleep(15)        
        
if __name__ == "__main__":
    wol = Wolconnectivity()
    lights = Light()
    
    lights_thread = threading.Thread(target=wol.check_lights)
    pc_thread = threading.Thread(target=wol.check_pc)
    
    lights_thread.start()
    pc_thread.start()
