from ping3 import ping
import subprocess, time, os, os.path, getpass

def ping_check(ip_address):
    response = ping(ip_address)
    if response is not None:
        return True
    else:
        return False

def CheckNetwork():
   AD = "ad.ayinfra.com"
   response = ping_check(AD)
   if response == True:
       print("Internal Network Coneected. This Script will choose the RDP.")
       RDPIF()
   else:
       print("It detected wasn't Internal Network. We'll Connect the VPN.")
       VPN()

def VPN():
    file_response = os.path.isfile("/opt/homebrew/etc/wireguard/wg0.conf")
    if file_response == False:
        print("Wireguard Configuration File wasn't Founded. This Script Will be shutdown.")
    else:
        os.system('wg-quick up wg0')
        time.sleep(10)
        CheckNetwork()

def RDPIF():
    print("Choose the VDI Server")
    print("1. LAB VM")
    print("2. Finance VDI")
    VDI = int(input("Your Answer : "))
    if VDI == 1:
        LAB()
    if VDI == 2:
        Finance()

def LAB():
    username = input("Enter the Username :")
    password = getpass.getpass("Enter The Password. :")
    os.system(f'xfreerdp /u:{username} /p:{password} /d:ayinfra.com /v:lab.external.com')
    
def Finance(): 
    username = input("Enter the Username :")
    password = getpass.getpass("Enter The Password. :")
    os.system(f'xfreerdp /u:{username} /p:{password} /d:ayinfra.com /v:finance.external.com')
    
CheckNetwork()
