from logging import getLogger, ERROR
from os import system
from time import sleep

getLogger('scapy.runtime').setLevel(ERROR)
from scapy.config import conf
from colorama import init, Fore
from pyfiglet import figlet_format

init() # windows
conf.verb=0
RED=Fore.LIGHTRED_EX
GREEN=Fore.LIGHTGREEN_EX
YELLOW=Fore.LIGHTYELLOW_EX
CYAN=Fore.LIGHTCYAN_EX
RESET=Fore.RESET

def colorize(msg, level='success', _exit=False, clear=False, timeout=1.5):
    banner=""
    color=''
    if level == 'success':
        banner="[+]"
        color=GREEN
    elif level == 'info':
        banner='[*]'
        color=YELLOW
    elif level == 'error':
        banner='[!]'
        color=RED
    
    print(f"{color}{banner}{msg}{RESET}")
    sleep(timeout)
    if _exit:
        exit(0)
    if clear:
        system('clear')

def banner(string, author, version):
    print("\n"*2)
    print(CYAN+figlet_format(string))
    print(f'Author: {author}    Version: {version}  Institute: SENATI\n\n'+RESET)
