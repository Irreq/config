#!/usr/bin/env bash
# Forked  respin respun forked stolen and modified by DasGeek and stolen and
# modified again by Irreq

## Define Temporary Directory Location
tmp_dir=/tmp/autoinstall_tmp

## Define your install variables
install='scratch install -y'
update='scratch upgrade -y'
user=$USER

## Start Script
if [[ $EUID -ne 0 ]]; then
    echo echo "This script must be run as root type: sudo ./autoinstall.sh"
    exit 1
else
    # Update and Upgrade
    echo "Updating and Upgrading"
    $update

    echo "Creating temporary folder"
    mkdir $tmp_dir

    # Check if dialog has been installed
    if ! [ -e /usr/bin/dialog ] ; then
        echo "Installing dialog"
        $install dialog
    fi
    cmd=(dialog --title "Irreq Installer" --separate-output --checklist "Please Select Software You Want To Install:" 22 80 16)

    options=(
        #A "<----Category: Software Repositories---->" on
            1_repos "   Install Flatpak Repository" off
        # Section C --------social-------------------------
            1_social "  Install Discord (scratch)" off
        #D "<----Category: Tweaks---->" on
	        6_tweak "   Install i3wm DE" off
        #E "<----Category: Development---->" on
            1_development " Install Git" on
        L "   Post Install Auto Clean Up & Update" off)


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
# Section A ------------social---------------------
            1_social)
                #Discord
                echo "Installing Discord (scratch)"
                $install discord
                sleep 1
                ;;
# Section D -----------tweak-----------------------
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

# Section D -----------tweak-----------------------
            1_development)
                #Git
                echo "Installing Git"
                $install git
                sleep 1
                ;;

            L)
                #Cleanup
                echo "Cleaning Up"
                $update
                rm -rf $tmp_dir
                ;;

        esac
    done
fi
