#!/usr/bin/env bash
#
# Bash install script
#
# Run this command in your terminal:
# #######################################################################################
# curl https://raw.githubusercontent.com/Irreq/config/main/postautoinstall.sh | sudo bash
# #######################################################################################
#

# Define variables
tmp_dir=/tmp/cool_name_here
user="irreq" # Your name here
INSTALL=""
UPGRADE=""
UPDATE=""

# Confirming function
confirm () {
	while true; do
		read -p "$1 Confirm (y/n) " yn
		case $yn in
			[Yy]* ) local result=true; break;;
			[Nn]* ) local result=false; break;;
			*);;
		esac
	done
	echo $result
}

## Start Script (checks if user has root privilegies)
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root!"
    exit 1
else
	echo "Post Install Script"
fi

echo "Finding Distro Name..."

# Find out what distro is used by finding the first instance of 'NAME='
CODENAME=`cat /etc/*-release | grep -m 1 "NAME="`

# Strip out the name
CODENAME=${CODENAME#*'"'}
CODENAME=${CODENAME%'"'*}

echo "Found: $CODENAME"

echo "Performing Distro-Specific Operations..."
case $CODENAME in
  "tVenom Linux")
    INSTALL="scratch install -y"
    UPGRADE="scratch upgrade -y"
    UPDATE="scratch sysup -y"
    ;;
  "Debian Linux")
    INSTALL="apt-get install -y"
    UPGRADE="apt-get upgrade -y"
    UPDATE="apt-get update -y"
    ;;
  *)
    echo "No Distro-specific details has been set."
    if ! "$(confirm "Would you like to continue?")"; then
      echo "Abborting..."
      exit 1
    fi
    ;;
esac
