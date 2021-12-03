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

# Regular Colors
black='\u001b[30m'        # Black
red='\u001b[31m'          # Red
green='\u001b[32m'        # Green
yellow='\u001b[33m'       # Yellow
blue='\u001b[34m'         # Blue
purple='\u001b[35m'       # Purple
cyan='\u001b[36m'         # Cyan
white='\u001b[37m'        # White

# Reset
off='\033[0m'       # message Reset

printf """

+-----------------------+
|                       |
| ${blue}Welcome to the script${off} |
|                       |
+-----------------------+

"""

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

# # Example
# if ! "$(confirm "Continue installation?")"; then
# 	read -p "Please enter desired username: " user
# 	echo "New username set to: $user"
# else
# 	echo "fuck off"
# fi
