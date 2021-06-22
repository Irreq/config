#!/usr/bin/env bash
# Forked  respin respun forked stolen and modified by DasGeek and stolen and
# modified again by Irreq


#    $HOME/bin Local binaries
#    $HOME/etc Host-specific system configuration for local binaries
#    $HOME/games Local game binaries
#    $HOME/include Local C header files
#    $HOME/lib Local libraries
#    $HOME/lib64 Local 64-bit libraries
#    $HOME/man Local online manuals
#    $HOME/sbin Local system binaries
#    $HOME/share Local architecture-independent hierarchy
#    $HOME/src Local source code


# Run this command in your terminal:
#
# curl https://raw.githubusercontent.com/Irreq/config/main/postautoinstall.sh | sudo bash
#

## Define Temporary Directory Location
tmp_dir=/tmp/postautoinstall_tmp

root_config_git="https://github.com/Irreq/config.git"

root_config="/home/github/config"

user='irreq'

home=/home/$user

## Start Script
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root type: sudo ./postautoinstall.sh"   
    exit 1
else
	echo "Post Install Script"
fi

KEYBOARD="se"
INSTALL="scratch install -y"
UPGRADE="scratch upgrade -y"
UPDATE="scratch sync"




echo "Finding Distro Name..."

# Find out what distro is used by finding the first instance of 'NAME='
CODENAME=`cat /etc/*-release | grep -m 1 "NAME="`

# Strip out the name
CODENAME=${CODENAME#*'"'}
CODENAME=${CODENAME%'"'*}

echo "Found: $CODENAME"

echo "Performing Distro-Specific Operations..."
case $CODENAME in
     "Venom Linux") 
          INSTALL="scratch install -y"
	  UPGRADE="scratch upgrade -y"
	  UPDATE="scratch sysup -y"
	
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
          ;;
     "Demo_Venom Linux")
          echo "Developing mode, toggle the right one later"
          ;;
     pattern-3|pattern-4|pattern-5)
          commands
          ;;
     pattern-N)
          commands
          ;;
     *)
          echo "echo No Distro found, Abborting"
	  exit 1
          ;;
esac

echo "Creating file-system"
mkdir -p $home/Programs
mkdir -p $home/github



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
	Make "Program for compiling packages" on
	CMake "Modern toolset used for generating Makefiles" on
	Ninja "Small build system with a focus on speed" on
	
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
	Make)
		$INSTALL make
		;;
	CMake)
		$INSTALL cmake
		;;
	Ninja)
		$INSTALL ninja
		;;


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
		echo "Moving Neovim to binaries"
		cp build/bin/nvim /home/$user/.local/bin/nvim
		cd $tmp_dir
		;;
	*)
		$INSTALL $choice
		;;
	esac
done

echo "Performing cleanup afterwards"

chown -R $user /home/$user/*
chown -R $user /home/$user/.local
echo "Please install ssh and ssh keys..."

while true; do
	read -p "Do you wish to setup config files automatically? [Y]es or [N]o " yn
	case $yn in
		[Yy]* ) echo "Will install config files"; break;;
		[Nn]* ) exit;;
		* ) echo "Please answer yes or no.";;
	esac
done

echo "Installing config files..."

mkdir -p /home/$user/github
cd /home/$user/github
# git clone git@github.com:Irreq/config.git
# chmod 600 ~/.ssh/*
cd config

echo "Setting up alacritty"
mkdir -p /home/$user/.config/alacritty
rm /home/$user/.config/alacritty/alacritty.yml
ln alacritty/alacritty.yml /home/$user/.config/alacritty/alacritty.yml

echo "Setting up Qtile"
mkdir -p /home/$user/.config/qtile
rm /home/$user/.config/qtile/config.py
ln qtile/config.py /home/$user/qtile/config.py

echo "Setting up Neovim"
mkdir -p /home/$user/.config/nvim
rm /home/$user/.config/nvim/init.vim
ln nvim/init.vim /home/$user/init.vim

echo "Setting up regular scripts"

# .bashrc
rm /home/$user/.bashrc
ln .bashrc /home/$user/.bashrc

# .xinitrc
rm /home/$user/.xinitrc
ln .xinitrc /home/$user/.xinitrc

# .gitconfig
rm /home/$user/.gitconfig
ln .gitconfig /home/$user/.gitconfig


# .fonts
mkdir -p /home/$user/.fonts
cp .fonts/* /home/$user/.fonts/*

# Cleanup again
echo "Changing ownership of files"
chown -R $user /home/$user/*
chown -R $user /home/$user/.local
chown -R $user /home/$user/.config

echo "Installation finished, please reboot now"

