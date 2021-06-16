#!/usr/bin/env bash
# Forked  respin respun forked stolen and modified by DasGeek and stolen and modified again by Irreq

## Define Temporary Directory Location -
tmp_dir=/tmp/autoinstall_tmp

## Define some variables to make it less typing
install='echo'
update='echo'
user=$USER



## Check if snapd has been installed just in case
check_snap () {
	if ! [ -e /usr/lib/snapd ] ; then
		$install snapd -y
	fi
}

## Start script
if [[ $EUID -ne 0 ]]; then
   	echo "This script must be run as root type: sudo ./installscript"
   	exit 1
else
	#Update and Upgrade
	echo "Updating and Upgrading"
	$update

	echo "Creating temporary folder"
	mkdir $tmp_dir

	$install dialog
	cmd=(dialog --title "Irreq Installer" --separate-output --checklist "Please Select Software You Want To Install:" 22 80 16)
	options=(
		#A "<----Category: Software Repositories---->" on
			1_repos "	Install Flatpak Repository" off
			2_repos "	Install Snaps Repository" off
		#B "<----Category: Notes---->" on 
	        1_notes "	Simplenote (SNAP)" off
	    #C "<----Category: Social---->" on
			1_social "	Mumble Client" off
	        2_social "	Zoom Meeting Client" off
	        3_social "	Telegram (Snap)" off
	        4_social "	Discord (Snap)" off
	        5_social "	Hexchat" off
	        6_social "	Signal (Snap)" off
	        7_social "	Whalebird (Mastodon app)(Snap)" off
	    #D "<----Category: Tweaks---->" on
	        1_tweak "	Elementary Tweaks" off
	        2_tweak "	Ubuntu Restricted Extras" off
	        3_tweak "	Gnome Tweak Tool" off
	        4_tweak "	Xfce Monitor Move Script" off
	        5_tweak "	Midnight Commander" off
	        6_tweak "	Install i3wm DE" off
	    #E "<----Category: Media---->" on  
	        1_media "	SM Player Media Player" off
	        2_media "	Pithos (Pandora)" off
	    	3_media "	Google Desktop Player (SNAP)" off
	    	4_media "	Audio-recorder Flac" off
	    #F "<----Category: Internet---->" on
	        1_internet "	Google Chrome" off
	        2_internet "	Vivaldi" off
	       	3_internet "	Firefox Browser" off     	
	       	4_internet "	get-iplayer (SNAP)" off	
	       	5_internet "	Chromium (SNAP)" off     
	    #G "<----Category: Video, Audio & Pic Editing---->" on
	        1_edit "	Kdenlive" off
	        2_edit "	Shotwell" off
	        3_edit "	GIMP" off
	        4_edit "	OBS-Studio" off
	        5_edit "	OBS-Studio (SNAP)" off
	        6_edit "	Audacity" off
	        7_edit "	ffmpeg (latest) (SNAP)" off
	        8_edit "	OcenAudio" off
		#H "<----Category: Security---->" on
			1_security "	PIA VPN (Network Mgr Version)" off
			2_security "	PIA VPN (GUI Version)" off
		#I "<----Category: Utility---->" on
		    1_utility "	Virtualbox" off
		    2_utility "	KXStudio Jack Setup (Advanced Audio)" off
		    3_utility "	Etcher" off
			4_utility "	Tilix" off
			5_utility "	Terminator" off
			6_utility "	Synology NAS Backup" off
			7_utility "	Gnome-do (Search Tool)" off
            8_utility "	Catfish - (File Search)" off
			9_utility "	Guvcview (webcam settings)" off
			10_utility "	Cheese" off	
			11_utility "	Fish (command line shell)" off
			12_utility "	KVM" off
			13_utility " Docker(CE)" off
		#J "<----Category: Coding & FTP---->" on
			1_coding "	Pycharm Pro (Pycharm Tools SNAP)" off
	    	2_coding "	Sublime Text" off # any option can be set to default to "on"
			3_coding "	Atom" off
			4_coding "	Putty" off
			5_coding "	Visual Studio Code" off
            6_coding "	Gedit" off
	        7_coding "	Filezilla" off
	        8_coding "	Snapcraft (For Snap Dev)" off
		#K "<----Category: Gaming & Fun---->" on
			1_gaming "	Steam (Valve)" off
			2_gaming "	Lutris" off
			3_gaming "	DOSBox-X (SNAP)" off
			4_gaming "	ScummVM (SNAP)" off
			5_gaming "	Gnome Twitch Client" off
			6_gaming "	Paulo Miguel AMD Drivers PPA" off		
		L "Post Install Auto Clean Up & Update" off)
		choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
		clear
		for choice in $choices
		do
		    case $choice in
# Section A ------------repos----------------------
	        1_repos)	
				#Install Flatpak Repo (Software Repository)
				echo "Installing Flatpak Repository"
				$install flatpak -y
				sleep 1
				;;

			2_repos)	
				#Install Snap Repository (Software Repository)
				echo "Installing Snap Repository"
				check_snap
				sleep 1
				;;
# Section B -------notes---------------------------

			1_notes)
			    #Simplenote (SNAP)
				echo "Installing Simplenote"
				check_snap
				snap install simplenote
				sleep 1
				;;
# Section C --------social-------------------------

			1_social)
				#Mumble Client
				echo "Installing Mumble"
				add-apt-repository ppa:mumble/release
				apt update
				$install mumble
				sleep 1
				;;		

			2_social)
				#Zoom
				echo "Installing Zoom Meeting Client"
				echo "Installing dependency first"				
				$install libxcb-xtest0
				wget https://zoom.us/client/latest/zoom_amd64.deb -O $tmp_dir/zoom_install.deb
				dpkg -i $tmp_dir/zoom_install.deb
				sleep 1
				;;
				
			3_social)
				#Telegram
				echo "Telegram Snap"
				check_snap
				snap install telegram-desktop
				sleep 1
				;;

			4_social)
				#Discord
				echo "Installing Discord (SNAP)"
				check_snap
				snap install discord
				sleep 1
				;;

			5_social)	
				#Hexchat
				echo "Installing Hexchat"
				$install hexchat
				sleep 1
				;;
			
			6_social) 
				#Signal (SNAP)
				echo "Installing Signal Messenger (SNAP)"
				check_snap
				snap install signal-desktop
				sleep 1
    			;;

    		7_social)
    			#Whalebird (SNAP)
    			echo "Installing Whalebird Mastodon App (SNAP)"
    			check_snap
    			snap install whalebird
                sleep 1
				;;

# Section D -----------tweak-----------------------

			1_tweak)
				#Elementary OS Tweaks
				echo "Installing Elementary Tweaks"
				$install software-properties-common
				$install elementary-tweaks 
				sleep 1
				;;
			2_tweak)
				#Ubuntu Restricted Extras
				echo "Installing Ubuntu Restricted Extras"
				$install ubuntu-restricted-extras
				sleep 1
				;;
			
			3_tweak)
				#Gnome tweak tool
				echo "Installing Gnome Tweak Tool"
				$install gnome-tweak-tool
				sleep 1
				;;

			4_tweak) 
				#Install monitor move window script Xfce
				echo "Downloading Monitor move window script"
				wget https://raw.githubusercontent.com/dasgeekchannel/move-to-next-monitor/master/move-to-next-monitor -O /home/$USER/Documents/move-to-next-monitor
				chmod +x ~/Documents/move-to-next-monitor
		    	chown -R $USER:$USER ~/Documents/move-to-next-monitor
		    	echo "Script now resides at /home/$USER/Documents/move-to-next-monitor"
				sleep 1
				;;

			5_tweak)
				#Install Midnight Commander
				echo "Install Midnight Commander"
				$install mc
				;;

			6_tweak)
				#Install i3wm
				echo "Installing i3wm & config"
				$install i3 i3status dmenu i3lock xbacklight feh conky
				#Use XFCE panel instead of default i3 and xfce plugins
				$install xfwm4 xfce4-statusnotifier-plugin xfce4-statusnotifier-plugin
				$install xfce4-pulseaudio-plugin xfce4-sensors-plugin xfce4-battery-plugin
				$install xfce4-panel xfce4-clipman-plugin xfce4-session xfce4-whiskermenu-plugin
				$install xfce4-mount-plugin xfce4-kbdleds-plugin
				# Installs compton to prevent screen tearing
				sleep 2
				$install compton unclutter 
				#hides mouse when not in use.
				#customize and theme
				$install lxappearance menulibre 
				sleep 2
				mkdir /home/$USER/.config/i3
				sleep 2
				wget https://github.com/dasgeekchannel/i3wmFedora28Config/raw/master/i3wallpaper.png -O /home/$USER/Pictures/i3wallpaper.png
				wget https://raw.githubusercontent.com/dasgeekchannel/i3wmFedora28Config/master/compton.conf -O /home/$USER/.config/compton.conf
                wget https://raw.githubusercontent.com/dasgeekchannel/i3wmFedora28Config/master/config -O  /home/$USER/.config/i3/config
                		sleep 2
                		wget https://github.com/dasgeekchannel/i3wmFedora28Config/raw/master/xfce4.zip
                		#wget https://github.com/dasgeekchannel/i3wmFedora28Config/archive/master.zip
                		#unzip master.zip
                		unzip xfce4.zip
                		sleep 2
                		#move current xfce settings to xfce4backup
                		mv /home/$USER/.config/xfce4 /home/$USER/.config/xfce4backup
                		#moves downloaded xfce4 config in place
                		sleep 2
                		mv xfce4 /home/$USER/.config/
                sleep 2
                wget https://github.com/dasgeekchannel/i3wmFedora28Config/raw/master/xfce4.zip
                #wget https://github.com/dasgeekchannel/i3wmFedora28Config/archive/master.zip
                #unzip master.zip
                unzip xfce4.zip
                sleep 2
                #move current xfce settings to xfce4backup
                mv /home/$USER/.config/xfce4 /home/$USER/.config/xfce4backup
                #moves downloaded xfce4 config in place
                sleep 2
                mv xfce4 /home/$USER/.config/
				sleep 2
				chown -R $USER:$USER /home/$USER/.config/compton.conf
				chown -R $USER:$USER /home/$USER/Pictures/i3wallpaper.png
				chown -R $USER:$USER /home/$USER/.config/xfce4
				chown -R $USER:$USER /home/$USER/.config/i3
				;;

# Section E -------------media---------------------

			1_media)
				#SMPlayer
				echo "Installing SMPlayer"
				$install smplayer 
				sleep 1
				;;

			2_media) 
				#Pithos
				echo "Installing Pithos"
				$install pithos 
				sleep 1
				;;

			3_media) 
				#Google Desktop Player (SNAP)
				echo "Installing Google Desktop Player (SNAP)"
				check_snap
				snap install google-play-music-desktop-player
				sleep 1
				;;

			4_media)
				#Audio-recorder
				echo "Installing Audio-recorder"
				apt-add-repository ppa:audio-recorder/ppa
				apt update
				$install audio-recorder 
				sleep 1
				;;
# Section F -------------internet--------------------
			1_internet)
				#Chrome
				echo "Installing Google Chrome"
				if ! [ -e /etc/apt/sources.list.d/google-chrome.list ]; then
					wget -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
					echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
				fi
				apt update 
				$install google-chrome-stable 
				;;

			2_internet)
				#Vivaldi
				echo "Installing Vivaldi"			
				wget https://downloads.vivaldi.com/stable/vivaldi-stable_1.15.1147.64-1_amd64.deb -O /tmp/ais/vivaldi.deb
				dpkg -i /tmp/ais/vivaldi.deb
				$install -f 
				;;

			3_internet)
				#Firefox Browser
				echo "Firefox"
				$install firefox 
				;;

			4_internet) 
				#get-iplayer (SNAP)
				echo "Installing get-iplayer (SNAP)"
				check_snap
				snap install get-iplayer
				;;

			5_internet) 
				#Chromium (SNAP)
				echo "Installing Chromium"
				check_snap
				snap install Chromium
				sleep 1
			;;

	# Section G -------------edit(Video/Audio/Pic)---------------------	
			1_edit)
				#Kdenlive
				echo "Installing Kdenlive"
				$install kdenlive breeze-icon-theme vlc frei0r-plugins dvdauthor 
				sleep 1
				;;
				
			2_edit)	
				#Shotwell
				echo "Installing Shotwell"
				$install shotwell 
				sleep 1
				;;            
    		
			3_edit)
				#GIMP (SNAP)
				echo "Installing GIMP"
				check_snap
				snap install gimp --edge
				sleep 1
				;;

			4_edit)
				#OBS Studio
				echo "Installing OBS Studio"
				$install ffmpeg 
				add-apt-repository ppa:obsproject/obs-studio
 				apt update
				$install obs-studio 
				sleep 1
				;;

			5_edit)
				#OBS Studio (SNAP)
				echo "Installing OBS Studio (SNAP)"	
				check_snap
				snap install obs-studio
				;;

			6_edit) 
				#Audacity
				echo "installing Audacity"
				$install audacity 
				sleep 1
				;;

			7_edit) 
				#ffmpeg (latest) (SNAP)
				echo "Installing ffmpeg"
				apt remove ffmpeg -y
				check_snap
				snap install ffmpeg --classic
				sleep 1
				;;
			
			8_edit)
				#OcenAudio Editor
				echo "Installing OcenAudio"
				wget -O $tmp_dir/ocenaudio.deb https://www.ocenaudio.com/downloads/ocenaudio_debian9_64.deb
				dpkg -i $tmp_dir/ocenaudio.deb
				sleep 1
				;;

	# Section H -----------security-----------------------	
			1_security)	
				#PIA VPN NM Version
				echo "Installing PIA VPN Network Manager Version"				
				wget https://www.privateinternetaccess.com/installer/install_ubuntu.sh -O $tmp_dir/install_ubuntu.sh
				$tmp_dir/install_ubuntu.sh
				echo "After entering username, go to network manager and turn on VPN and select from PIA locations, enter password and boom!"
				sleep 1
				;;

			2_security)	
				#PIA VPN GUI
				## I'm not officially sure if this will work. Will need to test it.
				## TODO: ensure this works
				echo "PIA VPN GUI VERSION"
				wget -nc https://installers.privateinternetaccess.com/download/pia-v81-installer-linux.tar.gz -O $tmp_dir/piavpn.tar.gz
				tar -xzf piavpn.tar.gz
				mv pia-v81-installer-linux.sh piavpn.sh
				chmod +x piavpn.sh
				chown -R $USER:$USER $tmp_dir/.pia_manager
				$tmp_dir/piavpn.sh
				sleep 5
				#rm -rf piavpn.tar.gz
				;;
	
	# Section I ----------utility------------------------	

    		1_utility)	
    			#Virtualbox
				echo "Installing Virtualbox"
				$install virtualbox 
				sleep 1
				;;

			2_utility) 
				#Advanced Jack Audio Setup
				## TODO: Clean this up -> the debs need to be labeled for easier understanding
				## and all of the "$install" lines should be collapsed into one single line. Unable to test at
				## current moment.
				echo "Installing KXStudio Jack"
				# Install required dependencies if needed
				$install apt-transport-https software-properties-common libglibmm
				# Download the files
				cd $tmp_dir
				wget https://launchpad.net/~kxstudio-debian/+archive/kxstudio/+files/kxstudio-repos_9.5.1~kxstudio3_all.deb
				wget https://launchpad.net/~kxstudio-debian/+archive/kxstudio/+files/kxstudio-repos-gcc5_9.5.1~kxstudio3_all.deb
				# Install it
				dpkg -i kxstudio-repos_9.5.1~kxstudio3_all.deb
				dpkg -i kxstudio-repos-gcc5_9.5.1~kxstudio3_all.deb
				usermod -a -G audio $USER
				$update
				$install jackd2 jackd2-firewire carla-git cadence non-mixer pulseaudio-module-jack mididings 
				# Download auto script github
				mkdir ~/jacksetup
				wget -O ~/jacksetup/start_jack.sh https://raw.githubusercontent.com/Skrappjaw/audio-scripts/master/start_jack.sh
				chmod +x ~/jacksetup/start_jack.sh
				chown -R $USER:$USER ~/jacksetup
				# Optional to put script into autostart
				#cd ~/
				#cp ~/jacksetup/start_jack.sh /etc/init.d/
				#update-rc.d start_jack.sh defaults
				;; 

			3_utility) 
				#Etcher ISO Creator
				## TODO: Add menu .desktop icon for easier accessibility
				echo "Installing Etcher"
				$install unzip -y
				wget -O ~/Downloads/etcher.zip https://github.com/resin-io/etcher/releases/download/v1.4.4/etcher-electron-1.4.4-linux-x64.zip
				unzip ~/Downloads/etcher.zip
				mv etcher-*.AppImage etcher.AppImage
				chmod +x ~/Downloads/etcher.AppImage
				ln -s /home/$USER/Downloads/etcher.AppImage /usr/local/bin/etcher
				sleep 1
				;;

			4_utility) 
				#Tilix (Tiling Terminal)
				echo "Installing Tilix"
				$install tilix 
				sleep 1
				;;

			5_utility)
				#Skynet/Terminator
				echo "Installing Terminator"
				$install terminator 
				sleep 1
				;;

			6_utility) 
				#Synology NAS Assistant & Backup
				echo "Installing Syn Assist and CloudStation Backup"
				wget -O $tmp_dir/synassistant.deb https://global.download.synology.com/download/Tools/Assistant/6.1-15163/Ubuntu/x86_64/synology-assistant_6.1-15163_amd64.deb
				wget -O $tmp_dir/cloudback.deb https://global.download.synology.com/download/Tools/CloudStationBackup/4.2.6-4408/Ubuntu/Installer/x86_64/synology-cloud-station-backup-4408.x86_64.deb
				dpkg -i $tmp_dir/synassistant.deb
				dpkg -i $tmp_dir/cloudback.deb
				$install -f 
				sleep 1
				;;

			7_utility) 
				#Gnome-do
				echo "Installing GnomeDo"
				$install gnome-do gnome-do-plugins
				sleep 1
				;;

			8_utility) 
				#Install Catfish
				echo "Installing Catfish"
				$install catfish

				sleep 1
				;;

			9_utility) 
				#Guvcview
				echo "Installing Guvcview"
				$install libgsl2 libguvcview guvcview 
				sleep 1
				;;

			10_utility) 
				#Cheese
				echo "Installing Cheese"
				$install cheese 
				sleep 1
				;;
			
			11_utility) 
				#Fish
				echo "Installing Fish"
				$install fish 
				sleep 1
				;;

			12_utility)
				#kvm
				echo "Installing KVM"
				$install qemu-kvm libvirt-bin bridge-utils virt-manager virtinst virt-viewer firewalld ebtables iptables qemu libspice-client-gtk-3.0-dev  
				sleep 1
				addgroup libvirtd
				adduser $USER libvirtd
				systemctl restart libvirtd
				sleep 1
				;;
				
			13_utility) #Docker
				echo "Installing Docker"
				$install apt-transport-https ca-certificates curl software-properties-common
				wget -O - https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
				echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
				apt update
				$install docker-ce 
				;;
        
	# Section J -----------coding-----------------------	

			1_coding) 	
				#Python Tools (Dev Testing)
				echo "Installing Python Tools"
				#Install PIP, packages, dev tools, and Pycharm
				$install python3-pip build-essential libssl-dev libffi-dev python-dev openjdk-8-jdk python3-setuptools 

				#Install SNAP
				check_snap
				snap install pycharm-professional
				sleep 1
				;;

	        2_coding)
	            #Install Sublime Text*
				echo "Installing Sublime Text"
				wget -O - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
				$install apt-transport-https
				echo "deb https://download.sublimetext.com/ apt/stable/" > /etc/apt/sources.list.d/sublime-text.list
				apt update
				$install sublime-text
				sleep 1
				;;

			3_coding)	
				#Atom
				echo "Installing Atom"							
				wget -O $tmp_dir/atom-amd64.deb https://atom.io/download/deb			
				dpkg -i $tmp_dir/atom-amd64.deb
				$install -f
				apm install atom-html-preview
				sleep 1
				;;

			4_coding)	
				#Putty
				echo "Installing Putty"
				$install putty
				sleep 1
				;;

			5_coding)
				#Visual Studio Code
				echo "Visual Studio Code"
				wget -O $tmp_dir/visualstudio.deb https://go.microsoft.com/fwlink/?LinkID=760868
				dpkg -i $tmp_dir/visualstudio.deb
				sleep 1
				;;
	
			6_coding)	
				#Install Gedit
				echo "Gedit"
				$install gedit
				sleep 1
				;;
			
			7_coding)
				#Filezilla (not related to Godzilla)
				echo "Installing Filezilla"
				$install filezilla 
				sleep 1
				;;

			8_coding)
				#SnapCraft
				$install snapcraft build-essential 
				mkdir -p ~/mysnaps
				chown -R $USER:$USER ~/mysnaps
				;;

			1_gaming)
				#Steam
				echo "Installing Steam"				
				$install steam 
				sleep 1
				;;

			2_gaming)
				#Lutris
				echo "Installing Lutris"
				wget -O - http://download.opensuse.org/repositories/home:/strycore/xUbuntu_$ver/Release.key | sudo apt-key add -
				ver=$(lsb_release -sr); if [ $ver != "17.10" -a $ver != "17.04" -a $ver != "16.04" ]; then ver=16.04; fi
				echo "deb http://download.opensuse.org/repositories/home:/strycore/xUbuntu_$ver/ ./" > /etc/apt/sources.list.d/lutris.list
				apt update
				$install lutris 
				;;

			3_gaming) 
				#DOSBox-X (SNAP)
				echo "Installing DOSBox-X"
				check_snap
				snap install dosbox-x
				;;
			
			4_gaming)
				#ScummVM (SNAP)
				echo "Installing ScummVM"
				check_snap
				snap install scummvm
				;;

			5_gaming) 
				#Gnome Twitch Client
				echo "Installing Gnome Twitch client"
				$install gnome-twitch 
				;;
			
			6_gaming)
				#Install AMD Drivers from PPA
				echo "Installing PPA AMD Drivers for Proton"
				add-apt-repository ppa:paulo-miguel-dias/mesa
				apt dist-upgrade
				$install mesa-vulkan-drivers mesa-vulkan-drivers:i386 
				;;
			
			L)  
				#Clean up
				echo "Cleaning up"
				$update
				rm -rf $tmp_dir
				;;
	
	    esac
	done
fi

