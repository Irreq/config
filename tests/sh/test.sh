#!/usr/bin/env bash
#
# Bash install script
#
# Run this command in your terminal:
# #######################################################################################
# curl https://raw.githubusercontent.com/Irreq/config/main/postautoinstall.sh | sudo bash
# #######################################################################################
#

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

yesno () {
	dialog --stdout --title "Confirm?" --yesno "$1" 0 0


	if [[ $? -eq "0" ]]; then
		# local result=true;
    clear
    # local result="true";
    echo true
	else
    clear
    echo false
		# Everything else is false
		# local result=false;
    # local result="false";
	fi
	# echo $result
}

# Get input function
retrieve () {
	local result=$(dialog --title "$1" --inputbox "$2" 0 0 2>&1 >/dev/tty)
	clear
	echo $result
}
echo  "Install Linux?"
pop=$(yesno)
# echo $pop
echo "fuckss"
dis="fuck $pop hello"

echo $dis

if $pop; then
  echo lol
fi

# exit 1

# if [[ $pop -eq "yes" ]]; then
# 	echo yes
# else
# 	echo no
# fi
