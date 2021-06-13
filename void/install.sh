#!/bin/bash

echo Install script for Void Linux


# perform a system update
sudo xbps-install -Su
sudo xbps-install -uy xbps

# install programs
sudo xbps-install -Suy neofetch git firefox python3 python3-pip xorg-minimal xorg-fonts mesa-dri setxkbmap xrandr pavucontrol alsa-utils apulse htop

cd ~/
mkdir github
# Just the regular
mkdir .config
cd github
git clone https://github.com/Irreq/config.git

# fix .bashrc
rm ~/.bashrc
ln ~/github/config/.bashrc ~/.bashrc

# fix neovim
sudo xbps-install -Suy neovim curl
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
pip install neovim
cd .config
mkdir nvim
cd nvim
ln ~/github/config/nvim/init.vim init.vim
cd ~/

# Fix qtile
cd ~/
sudo xbps-install -Suy python3-setuptools python3-wheel python3-dbus python3-gobject pango pango-devel libffi-devel xcb-util-cursor gdk-pixbuf
pip install xcffib
pip install --no-cache-dir cairocffi

git clone git://github.com/qtile/qtile.git
cd qtile
pip install .
pip install qtile
sudo cp bin/qtile /bin/qtile
## some fucking way xterm needs to be installed check .xinitrc
#sudo xbps-install -Suy xterm


cd ~/.config
mkdir qtile
cd qtile
ln ~/github/config/qtile/config.py ~/.config/qtile/config.py

# fonts
cp -r ~/github/config/.fonts ~/.fonts
# mkdir .fonts



# autostart qtile
ln ~/github/config/.xinitrc ~/.xinitrc

# alacritty for void
cd ~/
git clone https://github.com/alacritty/alacritty.git
cd alacritty
# get rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# you need to type '1'

# reload shell
source $HOME/.cargo/env
rustup override set stable
rustup update stable

sudo xbps-install -Suy cmake freetype-devel expat-devel fontconfig-devel libxcb-devel pkg-config gcc
cargo build --release
infocmp alacritty
sudo tic -xe alacritty,alacritty-direct extra/alacritty.info
# Do again if nothing worked
infocmp alacritty

# Necessary??
sudo cp target/release/alacritty /usr/local/bin # or anywhere else in $PATH
sudo cp extra/logo/alacritty-term.svg /usr/share/pixmaps/Alacritty.svg
sudo desktop-file-install extra/linux/Alacritty.desktop
sudo update-desktop-database

# Man page
sudo mkdir -p /usr/local/share/man/man1
gzip -c extra/alacritty.man | sudo tee /usr/local/share/man/man1/alacritty.1.gz > /dev/null

# bash completions
mkdir -p ~/.bash_completion
cp extra/completions/alacritty.bash ~/.bash_completion/alacritty
# already in the .bashrc file from github
# echo "source ~/.bash_completion/alacritty" >> ~/.bashrc

cd ~/.config
mkdir alacritty
cd alacritty
ln ~/github/config/alacritty/alacritty.yml alacritty.yml

# Install flatpak
sudo xbps-install -Suy flatpak
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
# Install Discord
sudo flatpak install flathub com.discordapp.Discord -y
# Install Teams
sudo flatpak install flathub com.microsoft.Teams -y


# Install terminal youtube player

pip3 install --user mps-youtube
pip3 install --user youtube-dl
pip3 install --user youtube-dl --upgrade
pip3 install --user dbus-python pygobject
ln ~/.local/bin/mpsyt /bin/mpsyt
