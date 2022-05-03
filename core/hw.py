from subprocess import getoutput
from os import system
from string import hexdigits
from random import choice

MONITOR_MODE_COMMAND='sudo ifconfig {} down && sudo iwconfig {} mode monitor && sudo ifconfig {} up'
MANAGEMEND_MODE_COMMAND='sudo ifconfig {} down && sudo iwconfig {} mode managed && sudo ifconfig {} up'
CHANGE_CHANNEL='sudo iwconfig {} channel {}'

START_NETWORK_MANAGER="sudo service NetworkManager start"
STOP_NETWORK_MANAGER="sudo service NetworkManager stop"

START_WPA_SUPPLICANT="sudo service wpa_supplicant start"
STOP_WPA_SUPPLICANT="sudo service wpa_supplicant stop"

RESTART_NETWORK_MANANGER="sudo service NetworkManager restart"
RESTART_WPA_SUPPLICANT="sudo service wpa_supplicant restart"

GET_MAC="ip link show %s | awk '/ether/ {print $2}' "
CHANGE_MAC="sudo macchanger --mac {} {}"

OLD_MAC=lambda iw : getoutput(GET_MAC%(iw)).strip()

def get_iws():
    ifaces=[]
    raw_ifaces=getoutput('nmcli dev').splitlines()[1:]
    raw_drivers=getoutput('inxi -N').splitlines()
    x=0
    for iface in raw_ifaces:
        if 'wifi' in iface:
            iface=iface.split()
            try:
                ifaces.append({'iw_name': iface[0], 'driver': raw_drivers[x].split()[-1]})
            except IndexError:
                pass
            x+=1
    return ifaces

def monitor_mode(iw):
    system('sudo airmon-ng check kill')
    output=getoutput(MONITOR_MODE_COMMAND.format(iw, iw, iw))
    if output.strip() == '':
        return True
    else:
        return False

def managed_mode(iw):
    system(f'sudo airmon-ng stop {iw}')
    system(RESTART_NETWORK_MANANGER)
    return True

def change_channel(iw, ch):
    return getoutput(CHANGE_CHANNEL.format(iw, ch))

def change_mac(iw, new_mac):
    return getoutput(CHANGE_MAC.format(new_mac, iw))

def gen_random_mac():
    base=""
    count=0
    for x in range(12):
        base+=choice(hexdigits)
        if (count % 2 != 0) and count != 11:
            base+=':'
        count+=1
    return base
