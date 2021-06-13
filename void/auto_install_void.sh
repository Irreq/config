#!/bin/bash

echo Welcome to the installation Void-Linux base glibc

echo Performing syncing of libraries
xbps-install -Suy
xbps-install -uy xbps

echo Installing git and setting up main directories
sudo xbps-install 

echo Will now install main programs such as browser and fetching tools
sudo xbps-install -Suy neofetch git firefox python3 python3-pip xorg-minimal xorg-fonts mesa-dri setxkbmap xrandr pavucontrol alsa-utils apulse htop


echo Installation finished, please reboot now
