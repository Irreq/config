#!/usr/bin/env sh

######################################################################
# @author      : irreq (irreq@protonmail.com)
# @file        : install
# @created     : Wednesday Jun 01, 2022 16:05:34 CEST
#
# @description : 
######################################################################


sudo pacman -Syu \
	cmake git openssh opendoas yay bash alacritty \
	openssh networkmanager wget curl\
	vim neovim vim-jedi python-jedi \
	htop neofetch cmatrix feh \
	alsa-lib alsa-utils pulseaudio pulsemixer \
	texlive-bin texlive-core texlive-science mupdf \
	clang llvm \
	discord audacity atom mps-youtube-git \
	-y

# Compiling
#cmake git \

# Development
 #llvm clang \
	#-y
# Install AUR
cd /opt
git clone https://aur.archlinux.org/yay-git.git
chown -R irreq:irreq ./yay-git
cd yay-git
makepkg -si -y
