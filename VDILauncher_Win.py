import sys
import subprocess
import os
import urllib.request
import webbrowser
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class VDILauncherWin(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dialog_open = False
        self.initUI()
        
        # 1. Check immediately upon startup
        QTimer.singleShot(100, self.check_network_status)

        # 2. Periodic monitoring (every 10 seconds)
        self.monitor_timer = QTimer(self)
        self.monitor_timer.setInterval(10000)
        self.monitor_timer.timeout.connect(self.check_network_status)
        self.monitor_timer.start()

    def initUI(self):
        self.setWindowTitle('AYLABS VDI Launcher')
        self.setGeometry(300, 300, 400, 350)
        self.setFixedSize(400, 350)

        # Layout Setup
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # 1. Network Status Label
        self.status_label = QLabel("Checking network status...", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.status_label.setStyleSheet("background-color: #DDDDDD; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.status_label)

        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # 2. User Input Fields
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Username")
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit(self)
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pass_input)

        # 3. Buttons
        self.btn_lab = QPushButton("1. Connect to LAB VM", self)
        self.btn_lab.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        self.btn_lab.clicked.connect(lambda: self.launch_rdp("LAB"))
        layout.addWidget(self.btn_lab)

        self.btn_finance = QPushButton("2. Connect to Finance VDI", self)
        self.btn_finance.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        self.btn_finance.clicked.connect(lambda: self.launch_rdp("Finance"))
        layout.addWidget(self.btn_finance)

        self.btn_exit = QPushButton("3. Exit", self)
        self.btn_exit.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 8px;")
        self.btn_exit.clicked.connect(self.close_app)
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)

    def ping_check(self, ip_address):
        """
        Check network using Windows ping command
        """
        try:
            # Windows command: ping -n 1 (1 count) -w 1000 (1000ms wait)
            creationflags = 0
            # Prevent console window from flashing (useful when distributed via pyinstaller)
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            subprocess.run(
                ['ping', '-n', '1', '-w', '1000', ip_address],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                creationflags=creationflags
            )
            return True
        except subprocess.CalledProcessError:
            return False
        except Exception as e:
            print(f"Ping Check Error: {e}")
            return False

    def check_captive_portal(self):
        target_url = "http://www.msftconnecttest.com/redirect"
        try:
            with urllib.request.urlopen(target_url, timeout=3) as response:
                final_url = response.geturl()
                if "msn.com" not in final_url and "msftconnecttest.com" not in final_url:
                    self.show_captive_portal_dialog(final_url)
                    return True
        except Exception:
            pass
        return False

    def show_captive_portal_dialog(self, portal_url):
        if self.is_dialog_open:
            return

        self.is_dialog_open = True
        self.activateWindow()
        self.raise_()

        msg = (f"Public Network Login (Captive Portal) detected.\n\n"
               f"Do you want to open the login page to use the network?\n\n"
               f"Detected URL: {portal_url[:50]}...")
               
        reply = QMessageBox.question(self, 'Network Login Required', msg,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.Yes)
        
        if reply == QMessageBox.StandardButton.Yes:
            webbrowser.open(portal_url)
        
        self.is_dialog_open = False

    def check_network_status(self):
        target_host = "hypervisor" # Needs to be registered in Windows hosts file or DNS
        
        if self.is_dialog_open:
            return

        is_internal_connected = self.ping_check(target_host)

        if is_internal_connected:
            self.status_label.setText("Internal Network Connected")
            self.status_label.setStyleSheet("background-color: #DFF2BF; color: #4F8A10; padding: 10px; border-radius: 5px;")
            self.enable_controls(True)
        else:
            self.status_label.setText("Network Not Detected (Verifying...)")
            self.status_label.repaint()
            
            is_captive = self.check_captive_portal()
            
            if is_captive:
                self.status_label.setText("Network Login Required (Captive Portal)")
                self.status_label.setStyleSheet("background-color: #FFF4E5; color: #663C00; padding: 10px; border-radius: 5px;")
            else:
                self.status_label.setText("Internal Network Not Detected (Check VPN)")
                self.status_label.setStyleSheet("background-color: #FFBABA; color: #D8000C; padding: 10px; border-radius: 5px;")

    def enable_controls(self, enabled):
        self.btn_lab.setEnabled(enabled)
        self.btn_finance.setEnabled(enabled)

    def launch_rdp(self, vdi_type):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        target_vdi = ""
        if vdi_type == "LAB":
            target_vdi = "developvdi"
        elif vdi_type == "Finance":
            target_vdi = "financevdi"

        try:
            print(f"Connecting to {vdi_type} ({target_vdi})...")
            
            # 1. Register credentials in Windows Credential Manager (cmdkey)
            # Must register as generic:TERMSRV/hostname for mstsc to recognize it
            cmdkey_cmd = f"cmdkey /generic:TERMSRV/{target_vdi} /user:{username} /pass:{password}"
            subprocess.run(cmdkey_cmd, shell=True, check=True)

            # 2. Execute mstsc
            mstsc_cmd = f"mstsc /v:{target_vdi}"
            subprocess.Popen(mstsc_cmd, shell=True)

        except subprocess.CalledProcessError:
             QMessageBox.critical(self, "Error", "Failed to register credentials.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during execution:\n{str(e)}")

    def close_app(self):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.instance().quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VDILauncherWin()
    ex.show()
    sys.exit(app.exec())