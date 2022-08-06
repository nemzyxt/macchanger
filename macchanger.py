# Author : Nemuel Wainaina

import os
import subprocess
import sys

INTERFACE = ""
NEW_MAC = ""

# check whether the supplied interface exists
def interface_exists(interface):
	output = subprocess.getoutput(f"ifconfig {interface}")
	
	if "not found" in output:
		return False
	else: return True

def main():
	# check to ensure that the script is running as root
	if os.geteuid() != 0:
		print("\n[!] Script needs root privileges to run")
		exit()
	
	print("[*] Shutting down " + INTERFACE)
	subprocess.run(["ifconfig", INTERFACE, "down"])
	print("[*] Changing MAC Address of " + INTERFACE)
	
	output = subprocess.getoutput(f"ifconfig {INTERFACE} hw ether {NEW_MAC}")
	if "invalid ether address" in output:
		print(f"\n[!] {NEW_MAC} is an invalid MAC Address")
		print("[-] Changing MAC failed !")
		exit()
		
	print("[*] Bringing " + INTERFACE + " back up")
	subprocess.run(["ifconfig", INTERFACE, "up"])
	print("[+] Done !")
	print(f"\n[+] NEW MAC : {NEW_MAC}")
	
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("[!] Too few arguments\nFormat: python3 macchanger.py <INTERFACE> <NEW_MAC>")
		
	INTERFACE = sys.argv[1]
	NEW_MAC = sys.argv[2]
	
	if interface_exists(INTERFACE):
		main()
	else:
		print(f"\n[!] Interface {INTERFACE} not found")
		exit()
