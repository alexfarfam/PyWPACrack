from os import getcwd

def finder(bssid):
    macer='unknown'
    PATH=getcwd()+'/utils/macers.txt'
    with open(PATH) as file:
        for line in file.read().splitlines():
            MAC, macer= line.split('~')
            
            if MAC.lower().strip().startswith(bssid):
                print(MAC, bssid)
                macer=macer
                break
    return macer
