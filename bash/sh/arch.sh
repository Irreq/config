# Minimized install script for Arch Linux


# Inside CHROOT
pacman -S vim git openssh ufw
timedatectl set-timezone Europe/Stockholm
echo arch-test > /etc/hostname
touch /etc/hosts
vim /etc/hosts


pacman -S grub os-prober
grub-install /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg

# Install is finished
pacman -S xorg-server xorg-xinit xf86-video-amdgpu xf86-video-ati xf86-video-intel
