#!/usr/bin/env sh

######################################################################
# @author      : irreq (irreq@protonmail.com)
# @file        : venom
# @created     : Thursday Sep 30, 2021 01:55:06 CEST
#
# @description : Install script for Flatpak
######################################################################

git clone https://github.com/flatpak/flatpak.git
cd flatpak
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
./autogen.sh
./configure
make
make install

