#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

programs='

'
installer='scratch search'

echo Performing installation of the following software:
while read -r p ; do echo "${installer} $p" ; ${installer} $p ;  done < <(cat << "EOF"
    xorg-server
    git
    python3
    fire
    ffff
    ffmpeg
EOF
)

exit 1

#a='Hello'
#b='World'
#c="${a} ${b}"
#echo "${c}"

installer='echo'
code="${installer} ${b}"
$code
#> Hello World

#HELLO=(install this package)
HELLO=hello
ts=$(echo)
function hello {
    local HELLO=World
    echo $HELLO
}
$ts lol me
echo $HELLO
hello
echo $HELLO

exit 1
sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

echo installing the must-have pre-requisites
exit 1
while read -r p ; do sudo apt-get install -y $p ; done < <(cat << "EOF"
    perl
    zip unzip
    exuberant-ctags
    mutt
    libxml-atom-perl
    postgresql-9.6
    libdbd-pgsql
    curl
    wget
    libwww-curl-perl
EOF
)

echo installing the nice-to-have pre-requisites
echo you have 5 seconds to proceed ...
echo or
echo hit Ctrl+C to quit
echo -e "\n"
sleep 6

sudo apt-get install -y tig
