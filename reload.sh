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

yesno () {
	dialog --stdout --title "Confirm?" --yesno "$1" 0 0 2>&1 >/dev/tty

	if [[ $? -eq "0" ]]; then
		result=true;
	else
		# Everything else is false
		result=false;
	fi
	clear
	echo $result
}

# Get input function
retrieve () {
	result=$(dialog --title "$1" --inputbox "$2" 0 0 2>&1 >/dev/tty)
	clear
	echo $result
}

# res="$(yesno "Install Linux?")"
# echo $res

pop=$(retrieve "Install Linux?")
echo $pop

# exit 1

if [[ $pop -eq "yes" ]]; then
	echo yes
else
	echo no
fi

# if [[ "$(yesno "Install Linux?")" -eq "true"]]; then
# 	echo yes
# else
# 	echo no
# fi

# if [[ $res -eq "true" ]]; then
# 	echo yes
# else
# 	echo no
# fi

# echo 88
# # echo $res
# echo 99



## Start Script (checks if user has root privilegies)
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root!"
    exit 1
else
	echo $'Post Install Script\n'
fi

# name="$(retrieve "Would you like to continue?" "Name:")"
# echo $name

echo "Finding Distro Name..."

# Find out what distro is used by finding the first instance of 'NAME='
CODENAME=`cat /etc/*-release | grep -m 1 "NAME="`

# Strip out the name
CODENAME=${CODENAME#*'"'}
CODENAME=${CODENAME%'"'*}

echo "Found: $CODENAME"
# res="$(yesno "Install Linux?")"
#
# echo $res



# if "$(yesno "Install Linux?")"; then
# 	echo "Installing linux"
# else
# 	echo fuck
# fi

# echo $res

# if ! "$(yesno "Install Linux?")"; then
# 	echo "Abborting..."
# 	# exit 1
# fi

exit 1

echo "Performing Distro-Specific Operations..."
case $CODENAME in
  "Venom Linux")
    INSTALL="scratch install -y"
    UPGRADE="scratch upgrade -y"
    UPDATE="scratch sysup -y"
		echo $'\nWill now perform following operations:\n
		* Set keyboard
		* Connect to internet
		* Update repo file
		* Sync repos
		\n'
    if "$(confirm "Would you like to continue?")"; then
			# Setting your keyboard
		  setxkbmap $KEYBOARD

		  # Connect to internet (requires you to use keyboard)
		  nmtui

		  # Update the repo file
		  echo /usr/ports/multilib   https://github.com/venomlinux/ports/tree/2.0/multilib >> /etc/scratchpkg.repo
		  echo /usr/ports/nonfree    https://github.com/venomlinux/ports/tree/2.0/nonfree >> /etc/scratchpkg.repo
		  echo /usr/ports/testing    https://github.com/venomlinux/ports/tree/2.0/testing >> /etc/scratchpkg.repo

		  echo "Performing a system sync"
		  scratch sync
    fi
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

echo "Creating temporary folder"
mkdir -p $tmp_dir
cd $tmp_dir

# Check if dialog has been installed
if ! [ -e /usr/bin/dialog ] ; then
	echo "Installing dialog"
	$install dialog
fi

cmd=(dialog --title "Irreq Installer" --separate-output --checklist "Please Select Software You Want To Install:" 22 80 16)

# Every instance beginning with a small letter is assumed to be installed using the generic
# * option down below. This also assumes that the package is inside the repos.
options=(
	make "Program for compiling packages" on
	cmake "Modern toolset used for generating Makefiles" on
	ninja "Small build system with a focus on speed" on

	opnssh "Free version of the SSH connectivity tools" off
	pavucontrol "PulseAudio Volume Control" on
	pulseaudio-alsa "ALSA Configuration for PulseAudio" on
	ffmpeg "FFmpeg is a solution to record, convert and stream audio and video" on
	firefox "Stand-alone browser based on the Mozilla codebase" off

	neofetch "A command-line system information tool written in bash 3.2+ " off
	alacritty "A cross-platform, GPU-accelerated terminal emulator" off
	Qtile "A full-featured, hackable tiling window manager written and configured in Python" off
	Neovim "Vim-fork focused on extensibility and usability" off
	discord "[repo] All-in-one voice and text chat for gamers that's free and secure" off
	Discord "[tar.gz] All-in-one voice and text chat for gamers that's free and secure" off
	teams "Microsoft Teams for Linux is your chat-centered workspace in Office 365" off
	End "Post Install Auto Clean Up & Update" off)

choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)

clear

for choice in $choices
do
	# Notify User of What Program Being Installed
	echo "Installing $choice"

	case $choice in

	# Social
	Discord)
		$INSTALL wget tar cups
		mkdir -p /home/$user/.local/bin
		wget "https://discord.com/api/download?platform=linux&format=tar.gz"
		tar -xvf 'download?platform=linux&format=tar.gz' -C /home/$user/Programs
		echo "Copying binaries to: ~/.local/bin"
		cp /home/$user/Programs/Discord/Discord /home/$user/.local/bin/discord
		;;
	Qtile)
		cd $tmp_dir
		echo "Installing dependencies"
		$INSTALL python3-pip python3-setuptools python3-wheel python3-dbus python3-gobject pango pango-devel libffi-devel xcb-util-cursor gdk-pixbuf
		pip install xcffib
		pip install --no-cache-dir cairocffi
		# Go to Programs
		cd /home/$user/Programs/
		git clone https://github.com/qtile/qtile.git
		cd qtile
		pip install .
		pip install qtile
		cp bin/qtile /bin/qtile
		cd $tmp_dir
		;;
	Neovim)
		cd $tmp_dir
		echo "Installing dependencies"
		$INSTALL gcc cmake ninja git
		echo "Cloning Neovim"
		cd /home/$user/Programs
		git clone https://github.com/neovim/neovim.git
		cd neovim
		echo "Building Neovim"
		make
    make install
		echo "Moving Neovim to binaries"
		cp build/bin/nvim /home/$user/.local/bin/nvim
		cd $tmp_dir
		;;
	*)
		$INSTALL $choice
		;;
	esac
done

# cmd=(dialog --title "name" --inputbox "Put your name:" 0 0)
# result=$("${cmd[@]}" 2>&1 >/dev/tty)
# result=$(dialog --title "name" --inputbox "Put your name:" 0 0 2>&1 >/dev/tty)
# clear
#
# echo $result
