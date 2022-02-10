#!/usr/bin/env sh

######################################################################
# @author      : irreq (irreq@protonmail.com)
# @file        : install
# @created     : Sunday Jan 09, 2022 20:00:16 CET
#
# @description : Installation script for neovim plugins
######################################################################

sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
pip install yapf, pylint, pynvim, jedi


