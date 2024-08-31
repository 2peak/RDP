import subprocess,time,os 

def WelcomeMessage():
   print("Welcome to the Andrew's VDI Launcher System")
   print("Select your PC Network Location")
   print("1. Intranet")
   print("2. WAN")   
   
def VPNConnect():
   subprocess.call([r'C:\\Program Files\\VDILauncher\\connect.bat'])
   #os.system(r'"C:\\Program Files\\VDILauncher\\connect.bat"') 
   time.sleep(15)
   print("Connect OpenVPN")

def GamingMultimon():
   print("MultiMonitor Select")
   print("1. Multi")
   print("2. Single") 
   Multi= int(input("Your Answer: "))
   if Multi == 1:
      os.system('cmdkey /generic:gaming.com /user:Andrew')
      os.system('mstsc /multimon /v gaming.com:2560')
   if Multi == 2:
      os.system('cmdkey /generic:gaming.com /user:Andrew')
      os.system('mstsc /v gaming.com:2560')

def FinanceMultimon():
   print("MultiMonitor Select")
   print("1. Multi")
   print("2. Single") 
   Multi= int(input("Your Answer: "))
   if Multi == 1:
      os.system('cmdkey /generic:finance.com /user:Andrew')
      os.system('mstsc /multimon /v finance.com:2560')
   if Multi == 2:
      os.system('cmdkey /generic:finance.com /user:Andrew')
      os.system('mstsc /v finance.com:2560')

def RDPIF():
   print("Choose the VDI Server")
   print("1. Gaming VDI")
   print("2. Finance VDI")
   VDI = int(input("Your Answer: "))
   if VDI == 1:
     GamingMultimon()
   elif VDI == 2:
      FinanceMultimon()      
   else:
      print("Answer Not inputed. Script Stopped.")

WelcomeMessage()
Network = int(input("Your Answer: "))
print(Network)
if Network == 1:
   RDPIF()
elif Network == 2:
   VPNConnect()
   RDPIF()
else:
   print("Answer Not inputed. Script Stopped.")
