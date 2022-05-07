from os import makedirs, remove, getcwd, walk, getuid
from os.path import split as split_path, expanduser, join as join_path, getsize
from datetime import datetime

from .colorize import colorize

IS_ROOT=getuid() == 0

def _size(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def _get_response(banner, values, question):
    while True:
        colorize(banner, level='info')
        count=0
        for value in values:
            print(f"[{count}] {value}")
            count+=1

        try:
            response=int(input(question))
            ap_data=values[response]
            return ap_data
        except ValueError:
            colorize('Por favor, eliga un numero!', level='error', clear=True)
        except IndexError:
            colorize('Por favor, seleccione un valor correcto!', level='error', clear=True)

def verify_pathdir():
    while True:
        dateformater=datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        path_cap=expanduser(input(f"Por favor, ingrese una ruta donde guardar los datos o enter[/tmp/capture_{dateformater}]: ").strip()) or f'/tmp/capture_{dateformater}'

        try:
            open(path_cap, "w").write('')
            remove(path_cap)
            return path_cap
        except FileNotFoundError:
            path_dir=split_path(path_cap)[0]

            option=_get_response(f'La ruta {path_cap} no existe. ¿Desea crear la ruta \'{path_dir}\'?: ', ['Si', 'No'], f'Ingrese una opcion: ').lower()
            if option == 'si':
                makedirs(path_dir)
                return path_cap

def _scan(_root):
    possible_wordlists=[]
    for root in walk(expanduser(_root)):
        subroot=root[0]
        files=root[2]

        for file in files:
            path=join_path(subroot, file)
            if "license" in path.lower() or "url" in path.lower() or "index" in path.lower() or "chrome" in path.lower() or "host" in path.lower() or "enlaces" in path.lower() or "proxys" in path.lower() or "test" in path.lower() or "commit" in path.lower() or "notice" in path.lower() or "data" in path.lower() or "log" in path.lower() or "readme" in path.lower():
                continue
            else:
                if "password" in path.lower() or "dict" in path.lower() or "rockyou" in path.lower() or "common" in path.lower():
                    if path.endswith('.txt') or path.endswith('.text'):
                        size=_size(getsize(path))
                        possible_wordlists.append(path+"\t"+size)
    return possible_wordlists

def get_wordlist():
    wordlists=[]
    for possible_path in (getcwd(), getcwd()):
        dicts=_scan(possible_path)
        wordlists.extend(dicts)
    
    _wordlists=set(wordlists)
    _wordlists=list(_wordlists)
    _wordlists.append("Escribir Ruta.")
    _wordlists.append("Usar JSDictor.")
    path_wordlist=_get_response('Diccionarios Disponibles: ', _wordlists, 'Eliga un diccionario: ')
    return path_wordlist