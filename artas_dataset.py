import xmltodict
import os
import folium
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from enum import Enum
import glob

class Type(Enum):
    QUIT = 'q'
    RUNWAY = '1'
    TMA = '2'
    ERA = '3'
    ICCA = '4'
    GMA = '5'
    UNIT = '6'
    USER = '7'
    SERVICE = '8'
    ALL = '9'
    BACK = 'b'

def generation_image(polygon_coords , nom, waitTime=5):
    #Génère une image PNG à partir d'une liste de coordonnées
    # exemple : polygon_coords = [(45.523, -122.675),
    #                   (45.523, -122.655),
    #                   (45.503, -122.655),
    #                   (45.503, -122.675)]

    #inversion lat/lon si nécessaire
    #polygon_coords =  [(t[1], t[0]) for t in polygon_coords]

    # Calculer le centre du polygone
    polygon_center = [sum([c[0] for c in polygon_coords]) / len(polygon_coords),
                      sum([c[1] for c in polygon_coords]) / len(polygon_coords)]

    # Créer une carte folium centrée sur le centre du polygone
    m = folium.Map(location=polygon_center, zoom_start=12)

    # Ajouter le polygone à la carte
    folium.Polygon(locations=polygon_coords, color='red', fill_color='red').add_to(m)

    # Ajuster la carte à la zone géographique du polygone
    m.fit_bounds([polygon_coords])

    # Set the temporary file path
    temp_file = 'temp_map.html'
    # Save the map to the temporary file
    m.save(temp_file)

    # Copy the temporary file to another location
    shutil.copyfile(temp_file, 'temp_map_copy.html')

    # Set Firefox binary location
    options = Options()
    #options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'  # Remplacez '/chemin/vers/firefox-binary' par le chemin complet du binaire Firefox
    driver = webdriver.Firefox(options=options)

    #driver.get('file://' + os.getcwd() + '/html/temp_map_copy.html')
    driver.get('file://' + os.getcwd() + '/temp_map_copy.html')
    # Maximize the browser window
    driver.maximize_window()
    # Wait for 10 seconds to ensure the map is fully loaded
    time.sleep(waitTime)
    

    # Take a screenshot of the map and save it with a specified name
    screenshot = driver.save_screenshot(nom)
    # Close the browser and quit the webdriver
    driver.quit()


def menu(xml_dico):
    zone = -1
    while True:
        print("***** MENU PRINCIPAL ******")
        print(
          "- 1 => Runway\n"
          "- 2 => TMA\n"
          "- 3 => ERA\n"
          "- 4 => ICCA\n"
          "- 5 => GMA\n"
          "- 6 => UNIT DOI\n"
          "- 7 => USER DOI\n"
          "- 8 => USER SERVICES DOI\n"
          "- 9 => ALL\n"
          "- b => Back\n"
          "- q => Quitter\n")
        
        zone = input("Veuillez choisir le numero de la zone à tracer ou quittez (q) ou revenir en arriere (b):\n")
    
        match zone:
            case Type.QUIT.value:
                exit ()
            case Type.RUNWAY.value:
                traitement_runway (xml_dico)
            case Type.TMA.value:
                traitement_tma (xml_dico)
            case Type.ERA.value:
                traitement_era (xml_dico)
            case Type.ICCA.value:
                traitement_icca (xml_dico)
            case Type.GMA.value:
                traitement_gma (xml_dico)
            case Type.UNIT.value:
                traitement_doi (xml_dico)
            case Type.USER.value:
                traitement_user (xml_dico)
            case Type.SERVICE.value:
                traitement_service (xml_dico)
            case Type.ALL.value:
                traitement_all (xml_dico)
            case Type.BACK.value:
                return 'b'
        
def  traitement_runway (xml_dico,answer=0):
    print("------------ Tracé des zones Runways ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        runway_list = xml_dico['dataset']['runway_main']['runway']
    except:
        print("Pas de zones definies pour Runway dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
    
    if isinstance(runway_list, dict):  # Vérifie si c'est un dictionnaire
        runway_list = [runway_list]  # Convertit en une liste avec un seul élément
        
    zones_name = [dico["name"] for dico in runway_list]
    
    if answer != "" :
        print('\n'.join(zones_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in zones_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for zone in runway_list:
            coodinates = getCoord(runway_list,zone["name"],Type.RUNWAY)
            generation_image (coodinates, version + "-" + zone["name"] + '.png',10)
    else:
        coodinates =getCoord(runway_list,answer,Type.RUNWAY)
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_runway (xml_dico,answer=0)
        
    return 0 

def traitement_tma (xml_dico,answer=0):
    print("------------ Tracé des zones TMA ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        tma_list = xml_dico['dataset']['tma_main']['tma']
    except:
        print("Pas de zones definies pour TMA dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
        
    if isinstance(tma_list, dict):  # Vérifie si c'est un dictionnaire
        tma_list = [tma_list]  # Convertit en une liste avec un seul élément
        
    zones_name = [dico["name"] for dico in tma_list]
    
    if answer != "" :
        print('\n'.join(zones_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in zones_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for zone in tma_list:
            coodinates = getCoord(tma_list,zone["name"],Type.TMA)
            generation_image (coodinates, version + "-" + answer + '.png')
    else:
        coodinates =getCoord(tma_list,answer,Type.TMA)
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_tma (xml_dico,answer=0)
        
    return 0

def traitement_era (xml_dico,answer=0):
    print("------------ Tracé des zones ERA ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        enrta_list = xml_dico['dataset']['enrta_main']['enrta']
    except:
        print("Pas de zones definies pour ERA dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
        
    if isinstance(enrta_list, dict):  # Vérifie si c'est un dictionnaire
        enrta_list = [enrta_list]  # Convertit en une liste avec un seul élément
        
    zones_name = [dico["name"] for dico in enrta_list]
    
    if answer != "" :
        print('\n'.join(zones_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in zones_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for zone in enrta_list:
            coodinates = getCoord(enrta_list,zone["name"],Type.ERA)
            generation_image (coodinates, version + "-" + zone["name"] + '.png',10)
    else:
        coodinates =getCoord(enrta_list,answer,Type.ERA)
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_era (xml_dico,answer=0)
        
    return 0 

def traitement_icca (xml_dico,answer=0):
    print("------------ Tracé des zones ICCA ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        icca_list = xml_dico['dataset']['icca_main']['icca']
    except:
        print("Pas de zones definies pour ICCA dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
        
    if isinstance(icca_list, dict):  # Vérifie si c'est un dictionnaire
        icca_list = [icca_list]  # Convertit en une liste avec un seul élément
        
    zones_name = [dico["name"] for dico in icca_list]
    
    if answer != "" :
        print('\n'.join(zones_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in zones_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for zone in icca_list:
            coodinates = getCoord(icca_list,zone["name"],Type.ICCA)
            generation_image (coodinates, version + "-" + zone["name"] + '.png',10)
    else:
        coodinates =getCoord(icca_list,answer,Type.ICCA)
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_icca (xml_dico,answer=0)
        
    return 0 

def traitement_gma (xml_dico,answer=0):
    print("------------ Tracé des zones GMA ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        gma_list = xml_dico['dataset']['gma_main']['gma']
    except:
        print("Pas de zones definies pour GMA dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
        
    if isinstance(gma_list, dict):  # Vérifie si c'est un dictionnaire
        gma_list = [gma_list]  # Convertit en une liste avec un seul élément
        
    zones_name = [dico["name"] for dico in gma_list]
    
    if answer != "" :
        print('\n'.join(zones_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in zones_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for zone in gma_list:
            coodinates = getCoord(gma_list,zone["name"],Type.GMA)
            generation_image (coodinates, version + "-" + zone["name"] + '.png',10)
    else:
        coodinates =getCoord(gma_list,answer,Type.GMA)
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_gma (xml_dico,answer=0)
        
    return 0 

def traitement_doi(xml_dico,answer=0):
    print("----------- Tracé de la zone DOI UNIT ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        doi_list = xml_dico['dataset']['unit_main']['unit']
    except:
        print("Pas de zones definies pour DOI UNIT dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
        
    if isinstance(doi_list, dict):  # Vérifie si c'est un dictionnaire
        doi_list = [doi_list]  # Convertit en une liste avec un seul élément
    
    zones_name = [dico["name"] for dico in doi_list]
    
    if answer != "" :
        print('\n'.join(zones_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in zones_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for zone in doi_list:
            coodinates = getCoord(doi_list,zone["name"],Type.UNIT)
            generation_image (coodinates, version + "-" + zone["name"] + '.png',10)
    else:
        coodinates =getCoord(doi_list,answer,Type.UNIT)
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_doi(xml_dico,answer=0)
        
    return 0 

def traitement_user(xml_dico,answer=0):
    print("----------- Tracé de la zone DOI USER ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        user_list = xml_dico['dataset']['broadcast_user_main']['broadcast_user']
    except:
        print("Pas de zones definies pour DOI USER dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
        
    if isinstance(user_list, dict):  # Vérifie si c'est un dictionnaire
        user_list = [user_list]  # Convertit en une liste avec un seul élément
    
    user_name = [dico["name"] for dico in user_list]
    
    if answer != "" :
        print('\n'.join(user_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in user_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for user in user_list:
            print(user["name"])
            coodinates = getCoord(user_list,user["name"],Type.USER)
            if coodinates == -1:
                print("Pas de zone DOI definie pour user " + user["name"] + " dans le dataset fourni !",10)
                continue
            generation_image (coodinates, version + "-" + user["name"] + '.png')
    else:
        coodinates =getCoord(user_list,answer,Type.USER)
        if coodinates == -1:
                print("Pas de zone DOI definie pour user " + answer + " dans le dataset fourni !")
                return 0
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_user(xml_dico,answer=0)
        
    return 0 

def traitement_service(xml_dico,answer=0):
    print("----------- Tracé de la zone DOI USER SERVICE ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        serice_list = xml_dico['dataset']['broadcast_user_main']['broadcast_user']
    except:
        print("Pas de zones definies pour DOI USER dans le dataset fourni !")
        print("Retour au menu principal ...")
        time.sleep(5)
        return -1
        
    if isinstance(serice_list, dict):  # Vérifie si c'est un dictionnaire
        serice_list = [serice_list]  # Convertit en une liste avec un seul élément
    
    user_name = [dico["name"] for dico in serice_list]
    
    if answer != "" :
        print('\n'.join(user_name))
        print("all =>  Tracer tous")
        print("q =>  Quitter")
        answer = input("Veuillez choisir la zone à tracer ou taper q pour quitter (default = all):\n")
    
    if answer == "" : answer = "all"
    
    while answer != "q" and answer != "all" and answer not in user_name :
        print("Votre saisie est incorrecte !!!\n")
        answer = input("Veuillez choisir la zone à tracer dans la liste ci-dessus ou taper q pour quitter:\n")
    
    if answer == "q":
        return 0
    
    elif answer == "all":
        for user in serice_list:
            coodinates = getCoord(serice_list,user["name"],Type.SERVICE)
            if coodinates == -1:
                print("Pas de zone DOI definie pour user " + user["name"] + " dans le dataset fourni !")
                continue
            generation_image (coodinates, version + "-" + user["name"] + '.png',10)
    else:
        coodinates =getCoord(serice_list,answer,Type.SERVICE)
        if coodinates == -1:
                print("Pas de zone DOI definie pour user " + answer + " dans le dataset fourni !")
                return 0
        generation_image (coodinates, version + "-" + answer + '.png')
        traitement_service(xml_dico,answer=0)
        
    return 0 

def  traitement_all (xml_dico):
    print("----------- Tracé de toutes les zones du dataset fourni ------------")
    traitement_user(xml_dico,"")
    traitement_doi(xml_dico,"")
    traitement_tma (xml_dico,"")
    traitement_era (xml_dico,"")
    traitement_icca (xml_dico,"")
    traitement_gma (xml_dico,"")
    traitement_runway (xml_dico,"")
    
    
    return 0

 
def dms_to_deg(degrees, minutes, seconds,dir):
    # Calcul du degré décimal
    dd = degrees + (minutes / 60) + (seconds / 3600)
    if (dir):
        return dd
    else:
        return -dd

def getCoord(zones_list, zone, type):
    
    zone_filtree = filter(lambda dico: dico["name"] == zone, zones_list) # on recupere les données de la zone renseignée dans la variable "zone"
    zone_filtree = list(zone_filtree)[0]
    if type == Type.RUNWAY :
        coord = zone_filtree['points']['pos']
    elif type == Type.UNIT or type == Type.USER:
        if "area" in zone_filtree['doi']:
            coord = zone_filtree['doi']['area']['pos']
        else:
            return -1
    
    elif type == Type.SERVICE:
        coord = zone_filtree['user_services']['service_connection']['service_volume']['area']['pos'] 
        #coord2 = coord['area']['pos']  
        a=2;
    else:
        coord = zone_filtree['area']['pos']
        
    coodinates =[]
    for pos in coord:
        lat = float(pos['lat'])
        lon = float(pos['lon'])
        coodinates.append((lat, lon))
    return coodinates
    
def main():
    
    xml_file = glob.glob("*.xml") # Recuperation de tous les fichiers ayant extension ".xml" dans le rep courant
    print("\n".join(xml_file))
    dataset = input("Veuillez saisir le nom ou le chemin du dataset.xml (version V9.1.0) à traiter (default = 4F_E1000.xml) ou quitter (q):\n")
    
    if dataset == "q":
        exit()
    
    if dataset.strip() == "" :
        dataset = "4F_E1000.xml"
    
    try:    
        with open(dataset, 'r') as file:
            xml_string = file.read()
    except:
        print ("Error: L'ouverture du Fichier {} à echoué, veuillez verifier le nom ou le chemin".format(dataset))
        exit ()
        
    xml_dico = xmltodict.parse(xml_string)
    
    ret = menu (xml_dico)
    
    if ret == 'b':
        main()


if __name__ == "__main__":
    main()
