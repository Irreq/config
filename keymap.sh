#!/bin/sh
(setxkbmap -query | grep -q 'variant:\s\+svdvorak') && setxkbmap -layout se || setxkbmap -layout se -variant svdvorak
