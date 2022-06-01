#!/usr/bin/env sh

######################################################################
# @author      : irreq (irreq@protonmail.com)
# @file        : install
# @created     : Sunday Jan 09, 2022 20:00:16 CET
#
# @description : Installation script for neovim plugins
######################################################################

#sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       #https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
#pip install yapf, pylint, pynvim, jedi

# c/c++ Support
mkdir -p ~/Programs
cd ~/Programs
git clone --depth=1 https://github.com/llvm/llvm-project.git
cd llvm-project
mkdir build && cd build
cmake -DLLVM_ENABLE_PROJECTS=clang -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release  ../llvm
make -j$(nproc)

# Add the binaries
export PATH="$HOME/Programs/llvm-project/build/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/Programs/llvm-project/build/lib:$LD_LIBRARY_PATH"
