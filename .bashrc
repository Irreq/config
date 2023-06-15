# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# don't overwrite GNU Midnight Commander's setting of `ignorespace'.
HISTCONTROL=$HISTCONTROL${HISTCONTROL+:}ignoredups
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
#[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac


if [ "$TERM" = "linux" ]; then
    # Cool oldschool font PxPlus HP located in /usr/share/kbd/consolefonts
    # color_prompt=yes
    #setfont ruscii_8x16.psfu.gz
	echo -en "\e]P0000000" # 0 Black
	echo -en "\e]P1960000" # 1 Red
	echo -en "\e]P2248902" # 2 Green
	echo -en "\e]P3fC8414" # 3 Orange
	echo -en "\e]P41459FC" # 4 Blue
	echo -en "\e]P56A00FF" # 5 Purple
	echo -en "\e]P606989A" # 6 Turqoise
	echo -en "\e]P7D3D7CF" # 7 Light Gray
	echo -en "\e]P8555753" # 8 Dark Gray
    echo -en "\e]P9FF0000" # 9 Bright Red
    echo -en "\e]PA22D81C" # 10 Dark Green
    echo -en "\e]PBFFFF00" # 11 Yellow
    echo -en "\e]PC32AFFF" # 12 Light Blue
    echo -en "\e]PDFD55FF" # 13 Pink
    echo -en "\e]PE34E2E2" # 14 Cyan
    echo -en "\e]PFFFFFFF" # 15 White
	clear # for background artifacting

    # export COLOR_NC='\e[0m' # No Color
    # export COLOR_BLACK='\e[0;30m'
    # export COLOR_GRAY='\e[1;30m'
    # export COLOR_RED='\e[0;31m'
    # export COLOR_LIGHT_RED='\e[1;31m'
    # export COLOR_GREEN='\e[0;32m'
    # export COLOR_LIGHT_GREEN='\e[1;32m'
    # export COLOR_BROWN='\e[0;33m'
    # export COLOR_YELLOW='\e[1;33m'
    # export COLOR_BLUE='\e[0;34m'
    # export COLOR_LIGHT_BLUE='\e[1;34m'
    # export COLOR_PURPLE='\e[0;35m'
    # export COLOR_LIGHT_PURPLE='\e[1;35m'
    # export COLOR_CYAN='\e[0;36m'
    # export COLOR_LIGHT_CYAN='\e[1;36m'
    # export COLOR_LIGHT_GRAY='\e[0;37m'
    # export COLOR_WHITE='\e[1;37m'

fi

#if [ "$TERM" = "linux" ]; then
#    echo -en "\e]P0232323" #black
#    echo -en "\e]P82B2B2B" #darkgrey
#    echo -en "\e]P1D75F5F" #darkred
#    echo -en "\e]P9E33636" #red
#    echo -en "\e]P287AF5F" #darkgreen
#    echo -en "\e]PA98E34D" #green
#    echo -en "\e]P3D7AF87" #brown
#    echo -en "\e]PBFFD75F" #yellow
#    echo -en "\e]P48787AF" #darkblue
#    echo -en "\e]PC7373C9" #blue
#    echo -en "\e]P5BD53A5" #darkmagenta
#    echo -en "\e]PDD633B2" #magenta
#    echo -en "\e]P65FAFAF" #darkcyan
#    echo -en "\e]PE44C9C9" #cyan
#    echo -en "\e]P7E5E5E5" #lightgrey
#    echo -en "\e]PFFFFFFF" #white
#    clear #for background artifacting
#fi

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
# force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

red='\[\e[0;31m\]'
RED='\[\e[1;31m\]'
blue='\[\e[0;34m\]'
BLUE='\[\e[1;34m\]'
cyan='\[\e[0;36m\]'
CYAN='\[\e[1;36m\]'
green='\[\e[0;32m\]'
GREEN='\[\e[1;32m\]'
yellow='\[\e[0;33m\]'
YELLOW='\[\e[1;33m\]'
PURPLE='\[\e[1;35m\]'
purple='\[\e[0;35m\]'
nc='\[\e[0m\]'

if [ "$UID" = 0 ]; then
    PS1="$red\u$nc@$red\H$nc:$CYAN\w$nc\\n$red#$nc "
else
    PS1="$RED[$yellow\u$YELLOW@$GREEN\H$blue # $PURPLE\w$RED]$nc$ "
fi
# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    #alias fgrep='fgrep --color=auto'
    #alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# Default parameter to send to the "less" command
# -R: show ANSI colors correctly; -i: case insensitive search
LESS="-R -i"

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

# Add sbin directories to PATH.  This is useful on systems that have sudo
echo $PATH | grep -Eq "(^|:)/sbin(:|)"     || PATH=$PATH:/sbin
echo $PATH | grep -Eq "(^|:)/usr/sbin(:|)" || PATH=$PATH:/usr/sbin
echo $PATH | grep -Eq "(^|:)$HOME/.local/bin(:|)" || PATH=$PATH:$HOME/.local/bin
echo $PATH | grep -Eq "(^|:)/usr/local/texlive/2021/bin/x86_64-linux(:|)" || PATH=$PATH:/usr/local/texlive/2021/bin/x86_64-linux

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then exec startx -display :7; fi

alias config='cd ~/github/config'
alias cls='clear'
alias sudo='doas'
export EDITOR='nvim'

complete -cf doas

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion



# Auto completion
# Use bash-completion, if available
[[ $PS1 && -f /usr/share/bash-completion/bash_completion ]] && \
    . /usr/share/bash-completion/bash_completion

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/irreq/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/irreq/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/irreq/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/irreq/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


[ -f ~/.fzf.bash ] && source ~/.fzf.bash
