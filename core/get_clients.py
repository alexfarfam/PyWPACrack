from time import sleep
from threading import Thread

from scapy.layers.l2 import ETHER_BROADCAST
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, Dot11FCS
from scapy.sendrecv import sniff

from core.hw import change_channel

clients=[]
networks=[]
_bssids=[]

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        if not bssid in _bssids:
            # get the name of it
            ssid = packet[Dot11Elt].info.decode()
            try:
                dbm_signal = packet.dBm_AntSignal
            except:
                dbm_signal = "N/A"
            # extract network stats
            stats = packet[Dot11Beacon].network_stats()
            # get the channel of the AP
            channel = stats.get("channel")
            # get the crypto
            crypto = str(stats.get("crypto")).replace('{', '').replace('}', '')

            #and crypto.upper().startswith('WPA')
            if ssid.strip() != '':
                data={'bssid': bssid, 'data':  (ssid, dbm_signal, channel, crypto)}
                networks.append(data)
                _bssids.append(bssid)

def cc(iface, timeout):
    ch = 1
    x=0
    while x != (timeout * 2):
        change_channel(iface, ch)
        # switch channel from 1 to 14 each 0.6s
        ch = ch % 14 + 1
        sleep(0.6)
        x+=1

def get_aps(iface, timeout=10):
    channel_changer = Thread(target=cc, args=(iface, timeout))
    channel_changer.daemon = True
    channel_changer.start()

    sniff(prn=callback, iface=iface, timeout=timeout)
    return networks

def get_aps_recursive(iface_name):
    aps=get_aps(iface_name)

    if len(aps) == 0:
        return get_aps_recursive(iface_name)
    else:
        return aps


####################################
def _sniff_clients(pk):
    try:
        data=pk[Dot11FCS]
        addr2=data.addr2

        ap_bssid=globals().get('ap_bssid')
        if addr2 == ap_bssid:
            addr1=data.addr1
            if not addr1 in clients and not addr1 == ETHER_BROADCAST.lower():
                clients.append(addr1)
    except Exception as e:
        pass

def get_clients(iface, _ap_bssid,timeout=20):
    global ap_bssid
    ap_bssid=_ap_bssid

    sniff(prn=_sniff_clients, iface=iface, timeout=timeout, monitor=True)
    return clients