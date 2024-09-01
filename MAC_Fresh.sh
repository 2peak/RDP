#!/bin/bash
# This Script was based on MAC Operating System. 
INSTALL_LOG="Fresh.log"
if [[ `sw_vers` == *"Product"* ]]; then
        echo "MacOS Detected. Script Will be started on."    
else
	echo "Another OS Detected. Script Will be shut down"
	exit 1
fi

if [[ `which brew` == *"homebrew"* ]] ; then
	echo "Brew was Installed. We'll skip this Process"
else
	echo "Brew will be Installed."
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	if [[ $? -ne 0 ]]; then
		echo "Brew Installation was Failed. This Script will be shut down."
		exit 1
	else
	 	echo "Brew Installation was completed."
		if test -d /opt/homebrew/; then
 			echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
			source ~/.zprofile
		elif test -d /usr/local/homebrew/ ; then
			echo 'eval "$(/usr/local/homebrew/bin/brew shellenv)"' >> ~/.zprofile
			source ~/.zprofile
		else
			echo "AutoEnroll Was failed. This Script Will be Shutdown."
			exit 1;
		fi
	fi
fi

if [[ `which python3` == *"python3"* ]]; then
	echo "Python was Installed."
else
	echo "Python was not installed. We'll Installed"
	brew install python >> ${INSTALL_LOG}>&1
	if [[ $? -ne 0 ]]; then
		echo "Python Can't be installed. Please do Manually."
		exit 1
	else
	 	echo "Python was installed"
	fi
fi

if test -d /opt/X11; then
	echo "Xquartz was Installed"
else 
	echo "Xquartz wasn't Installed. This Script will be installed now"
	brew install --cask xquartz
	if [[ $? -ne 0 ]]; then
		echo "Xquartz Can't be installed. Please do Manually."
		exit 1
	else
	 	echo "Xquartz was installed"
	fi
fi

if test -f /opt/homebrew/bin/xfreerdp; then
	echo "FreeRDP was Installed"
elif test -f /usr/local/homebrew/bin/xfreerdp; then
	echo "Intel FreeRDP was Installed"
else
	echo "FreeRDP Wasn't Founded. We'll Installed freerdp."
	brew install freerdp
	if [[ $? -ne 0 ]]; then
		echo "FreeRDP Can't be installed. Please do Manually."
		exit 1
	else
	 	echo "FreeRDP was installed"
	fi
fi

echo "We'll Installed pythonping package"
pip3 install pythonping
if [[ $? -ne 0 ]]; then
	echo "Extension wasn't be installed"
	exit 1
else
	echo "Extension was Installed"
	echo "Free Install was completed"
	exit 1
fi
 
