from http.client import HTTPSConnection, HTTPS_PORT
from subprocess import Popen, PIPE

def has_connection():
    try:
        client=HTTPSConnection(host='google.com', port=HTTPS_PORT)
        client.request(method='GET', url='/')
        return True
    except:
        return False

def _get_ouput(cmd):
    p=Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data=p.communicate()
    output=data[0].decode(encoding='ascii', errors='replace')
    err=data[1].decode(encoding='ascii',  errors='replace')
    if output or (output == '' and not err):
        return True, output
    elif err:
        return False, err

def upgrade():
    cmd1="sudo apt update -y && sudo apt-get upgrade -y"
    cmd2='echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" | sudo tee /etc/apt/sources.list && echo "deb http://http.kali.org/kali kali-last-snapshot main contrib non-free" | sudo tee /etc/apt/sources.list'

    output1=_get_ouput(cmd1)
    output2=_get_ouput(cmd2)
    return output1, output2

def install_essentials():
    cmd1="sudo apt-get install linux-headers-$(uname -r)"
    cmd2="sudo apt install bc && sudo apt-get install build-essential && sudo apt-get install libelf-dev && sudo apt install dkms"
    output1=_get_ouput(cmd1)
    output2=_get_ouput(cmd2)
    return output1, output2

def install_driver():
    cmd1="echo 'blacklist r8188eu'|sudo tee -a '/etc/modprobe.d/realtek.conf'"
    cmd2="cd /tmp/ && git clone https://github.com/aircrack-ng/rtl8188eus.git && cd rtl8188eus && make  && sudo make install"
    cmd3="cd /var/lib/shim-signed/mok && sudo /usr/src/linux-headers-$(uname -r)/scripts/sign-file sha256 ./MOK.priv ./MOK.der $(modinfo -n 8188eu)"
    cmd4="sudo modprobe 8188eu"

    output1=_get_ouput(cmd1)
    output2=_get_ouput(cmd2)
    output3=_get_ouput(cmd3)
    output4=_get_ouput(cmd4)
    return output1, output2, output3, output4