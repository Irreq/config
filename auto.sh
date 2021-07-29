#!/usr/bin/env bash
# Forked by respin respun forked stolen and modified by DasGeek and stolen and modified again by Irreq
#
# Requirements:
# git
# Correct SSH-keys located prefferably in /home/USERNAME/.ssh/
# 
# Execute using this command in your terminal:
#
# curl https://raw.githubusercontent.com/Irreq/config/main/postautoinstall.sh | sudo bash
#

## Define variables
tmp_dir=/tmp/postautoinstall_tmp
user='irreq'

## Distro specific variables (Venom Linux)
INSTALL="scratch install -y"
UPGRADE="scratch upgrade -y"
UPDATE="scratch sysup -y"
REMOVE="scratch remove -y"


# Confirming function
confirm () {
	while true; do
		read -p "$1 Please confirm (Y/N) " yn
		case $yn in
			[Yy]* ) local result=true; break;;
			[Nn]* ) local result=false; break;;
			*);;
		esac
	done
	echo $result
}

## Start Script
if [[ $EUID -ne 0 ]]; then
	echo "This script must be run as root."
	echo "Type: sudo ./postautoinstall.sh"
	echo "Or type this one-liner:"
	echo "curl https://raw.githubusercontent.com/Irreq/config/main/postautoinstall.sh | sudo bash"
	exit 1
else
	echo "Post Install Script"
fi

echo "Finding distro name..."

# Find out what distro is used by finding the first instance of 'NAME='
CODENAME=`cat /etc/*-release | grep -m 1 "NAME="`

# Strip out the name
CODENAME=${CODENAME#*'"'}
CODENAME=${CODENAME%'"'*}

echo "Found: $CODENAME"

echo "Performing Distro-Specific Operations..."

case $CODENAME in
	"test_Venom Linux")
		INSTALL="scratch install -y"
	  	UPGRADE="scratch upgrade -y"
	  	UPDATE="scratch sysup -y"
		REMOVE="scratch remove -y"

		# Setting Swedish keyboard
		setxkbmap se

		# Connect to internet (Requires a keyboard)
		nmtui

		if "$(confirm "Do you want to update the repo-file? Make sure that there aren't any other duplicates. Have a look at: /etc/scratchpkg.repo before continuing.")"; then
			echo /usr/ports/multilib   https://github.com/venomlinux/ports/tree/2.0/multilib >> /etc/scratchpkg.repo

	  		echo /usr/ports/nonfree    https://github.com/venomlinux/ports/tree/2.0/nonfree >> /etc/scratchpkg.repo

	  		echo /usr/ports/testing    https://github.com/venomlinux/ports/tree/2.0/testing >> /etc/scratchpkg.repo
		fi
	  	echo "Performing a system sync"
	  	scratch sync
	  	;;

	pattern-1)
		;;
	pattern-2|pattern3)
		;;
	pattern-N)
		;;
	*)
		# No distro was found
		if ! "$(confirm "No distro was found, do you still want to proceed, install method might not work...")"; then
			exit 1
		fi
		;;
esac


for COMMAND in git ssh dialog
do
if ! command -v $COMMAND &> /dev/null then
    echo "$COMMAND could not be found."
	echo "Installing $COMMAND..."
	$INSTALL $COMMAND
fi

done

if ! "$(confirm "Is your username: $user?")"; then
	read -p "Please enter desired username: " user
	echo "New username set to: $user"
fi

cmd=(dialog --title "$user Installer" --separate-output --checklist "Please Select Software You Want To Install:" 22 00 16)

# Every instance beginning with a small case letter is assumed to be installed
# using the generic '*' option below. This assumes that the package is in
# the repos.

options=(
	Make "Program for compiling packages" on
	CMake "Modern toolset used for generating Makefiles" on
	Ninja "Small build system with focus on speed" on
	
	openssh "Free version of the SSH connectivity tools" off
	pavucontrol "Pulseaudio volume control" off
	pulseaudio-alsa "ALSA configuration for PulseAudio" on
	ffmpeg "FFmpeg is a solution to record, convert and stream audio and video" on
	firefox "Stand-alone browser based on the Mozilla codebase" off
	neofetch "A command-line system information tool written in bash 3.2+" off
	alacritty "A cross-platform, GPU-accelerated terminal emulator" off
	Qtile "A full-featured, hackable tiling window manager written and configured in Python" off
    Neovim "Vim-fork focused on extensibility and usability" off
    discord "[repo] All-in-one voice chat for gamers that's free and secure" off
    Discord "[tar.gz] All-in-one voice chat for gamers that's free and secure" off
    End "Post install auto cleanup and update" off)

choices=$("$cmd[@]" "${options[@]}" 2>&1 >/dev/tty)

for choice in $choices
do
    # Notify which program that is being installed
    echo "Installing $choice"

    case $choice in
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





