#!/usr/bin/env bash

# Cheat-sheet for bash scripting

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

# Example
if ! "$(confirm "Continue installation?")"; then
	read -p "Please enter desired username: " user
	echo "New username set to: $user"
else
	echo "fuck off"
fi
