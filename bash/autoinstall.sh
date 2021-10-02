#!/usr/bin/env bash
# Forked  respin respun forked stolen and modified by DasGeek and stolen and
# modified again by Irreq



# Run this command in your terminal:
#
# curl https://raw.githubusercontent.com/Irreq/config/main/autoinstall.sh | sudo bash


## Define Temporary Directory Location
tmp_dir=/tmp/autoinstall_tmp

## Define your install variables
install='scratch install -y'
update='scratch upgrade -y'
#user=$USER
user='irreq'

home=/home/$user

## Start Script
if [[ $EUID -ne 0 ]]; then
    echo echo "This script must be run as root type: sudo ./autoinstall.sh"
    exit 1
else
    # Update and Upgrade
    echo "Updating and Upgrading"
    $update

    echo "Creating file-system"
    mkdir -p $home/Programs
    # mkdir -p $home/github



    echo "Creating temporary folder"
    mkdir $tmp_dir
    cd $tmp_dir

    # Check if dialog has been installed
    if ! [ -e /usr/bin/dialog ] ; then
        echo "Installing dialog"
        $install dialog
    fi
    cmd=(dialog --title "Irreq Installer" --separate-output --checklist "Please Select Software You Want To Install:" 22 80 16)

    options=(
            1_build "Make: Program for compiling packages" on
            2_build "CMake: Modern toolset used for generating Makefiles" on
            3_build "Ninja: Small build system with a focus on speed" on

            1_essentials "Git: Version control system" on
            2_essentials "Wget: The non-interactive network downloader" on
            3_essentials "Xorg-minimal" on
            4_essentials "Ninja: Small build system with a focus on speed" on
            5_essentials "CMake: Modern toolset used for generating Makefiles" on
            6_essentials "Make: Program for compiling packages" on
        #A "<----Category: Software Repositories---->" on
            1_repos "Flatpak (Repo)" off
            2_repos "Tar: An archiving program" on
        # Section C --------social-------------------------
            1_social "Discord (scratch)" off
            2_social "Discord (tar.gz)" off
        #D "<----Category: Tweaks---->" on
        #D "<----Category: Tweaks---->" on
	        1_internet "Firefox" on

            1_tweak "Qtile" off
            2_tweak "Neofetch" off
            6_tweak "Install i3wm DE" off
        #E "<----Category: Development---->" on
            1_development "Install Git" off
            2_development "Neovim" off
        L "Post Install Auto Clean Up & Update" off)


        choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
        clear
        for choice in $choices
        do
            case $choice in
            1_build)
                #Make
                echo "Installing Make"
                $install make
                sleep 1
                ;;
            2_build)
                #Cmake
                echo "Installing CMake"
                $install cmake
                sleep 1
                ;;
            3_build)
                #Ninja
                echo "Installing Ninja"
                $install ninja
                sleep 1
                ;;

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
            2_social)
                #Discord
                echo "Installing Discord (tar.gz)"
                cd $tmp_dir
                mkdir -p /home/$user/.local/bin
                wget "https://discord.com/api/download?platform=linux&format=tar.gz"
                ls -la
                tar -xvf 'download?platform=linux&format=tar.gz' -C /home/$user/.local/bin
                sleep 1
                ;;

            1_internet)
                #Firefox
                echo "Installing Firefox"
                cd $tmp_dir
                $install firefox
                sleep 1
                ;;
# Section D -----------tweak-----------------------
            1_tweak)
                echo "Installing Qtile (source)"
                sleep 1
                ;;

            2_tweak)
                #Qtile (xbps)
                echo "Installing Qtile (xbps)"
                sleep 1
                ;;
            3_tweak)
                #Alacritty
                echo "Installing Alacritty"
                echo "Installing building tools for rust"
                curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
                echo "Performing Rustup check"
                rustup override set stable
                rustup update stable
                cd /home/$user/Programs
                git clone https://github.com/alacritty/alacritty.git
                cd alacritty
                sleep 1
                ;;

            6_tweak)
				#Install i3wm
				echo "Installing i3wm & config"
				chown -R $USER:$USER /home/$USER/.config/i3
				;;

# Section D -----------tweak-----------------------
            1_development)
                #Git
                echo "Installing Git"
                $install git
                sleep 1
                ;;
            2_development)
                #Neovim
                echo "Installing Neovim"
                cd $tmp_dir
                echo "Installing dependencies"
                $install gcc cmake ninja
                echo "Cloning Neovim"
                cd $home/Programs
                git clone https://github.com/neovim/neovim.git
                cd neovim
                echo "Building Neovim"
                make
                echo "Moving Neovim to binaries"
                cp build/bin/nvim /bin/nvim
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
