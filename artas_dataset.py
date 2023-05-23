import xmltodict
import os
import folium
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


def generation_image(polygon_coords , nom):
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
    # Wait for 5 seconds to ensure the map is fully loaded
    time.sleep(5)
    

    # Take a screenshot of the map and save it with a specified name
    screenshot = driver.save_screenshot(nom)
    # Close the browser and quit the webdriver
    driver.quit()
def menu(xml_dico):
    zone = -1
    while zone < 0 or zone > 6:
        print(
          "- 0 => Quitter\n"
          "- 1 => Runway\n"
          "- 2 => TMA\n"
          "- 3 => ERA\n"
          "- 4 => ICCA\n"
          "- 5 => UNIT DOI\n"
          "- 6 => All\n")
        try :
            zone = int(input("Veuillez choisir le numero de la zone a tracer ou quittez (0):\n"))
        except:
            print("Erreur : Veuillez saisir un chiffre compris entre 0 et 5 correspondant a la zone SVP")
    match zone:
        case 0:
             exit ()
        case 1:
            traitement_runway (xml_dico)
        case 2:
            traitement_tma (xml_dico)
        case 3:
            traitement_era (xml_dico)
        case 4:
            traitement_icca (xml_dico)
        case 5:
            traitement_doi (xml_dico)
        case 6:
            traitement_all (xml_dico)
        
def  traitement_runway (xml_dico):
    print("------------ Tracé des zones Runways ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        runway_list = xml_dico['dataset']['runway_main']['runway']
    except:
        print("Pas de zones definies pour Runway dans le dataset fourni !")
        return -1
    
    if isinstance(runway_list, dict):  # Vérifie si c'est un dictionnaire
        runway_list = [runway_list]  # Convertit en une liste avec un seul élément
        
    for runway in runway_list:
        coodinates =[]
        for pos in runway['points']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, version + "-" + runway['name'] + '.png')
    return 0 

def traitement_tma (xml_dico):
    print("------------ Tracé des zones TMA ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        tma_list = xml_dico['dataset']['tma_main']['tma']
    except:
        print("Pas de zones definies pour TMA dans le dataset fourni !")
        return -1
        
    if isinstance(tma_list, dict):  # Vérifie si c'est un dictionnaire
        tma_list = [tma_list]  # Convertit en une liste avec un seul élément
        
    for tma in tma_list:
        coodinates =[]
        for pos in tma['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, version + "-" + tma['name'] + '.png')
    return 0

def traitement_era (xml_dico):
    print("------------ Tracé des zones ERA ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        enrta_list = xml_dico['dataset']['enrta_main']['enrta']
    except:
        print("Pas de zones definies pour ERA dans le dataset fourni !")
        return -1
        
    if isinstance(enrta_list, dict):  # Vérifie si c'est un dictionnaire
        enrta_list = [enrta_list]  # Convertit en une liste avec un seul élément
        
    for enrta in enrta_list:
        coodinates =[]
        for pos in enrta['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, version + "-" + enrta['name'] + '.png')
    return 0 

def traitement_icca (xml_dico):
    print("------------ Tracé des zones ICCA ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        icca_list = xml_dico['dataset']['icca_main']['icca']
    except:
        print("Pas de zones definies pour ICCA dans le dataset fourni !")
        return -1
        
    if isinstance(icca_list, dict):  # Vérifie si c'est un dictionnaire
        icca_list = [icca_list]  # Convertit en une liste avec un seul élément
        
    for icca in icca_list:
        coodinates =[]
        for pos in icca['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, version + "-" + icca['name'] + '.png')
    return 0 

def traitement_doi(xml_dico):
    print("----------- Tracé de la zone DOI UNIT ------------")
    
    version = xml_dico['dataset']['mutex_main']['mutex']['version_tag']
    
    try :
        doi_list = xml_dico['dataset']['unit_main']['unit']
    except:
        print("Pas de zones definies pour DOI UNIT dans le dataset fourni !")
        return -1
        
    if isinstance(doi_list, dict):  # Vérifie si c'est un dictionnaire
        doi_list = [doi_list]  # Convertit en une liste avec un seul élément
    for doi in doi_list:
        coodinates =[]
        for pos in doi['doi']['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, version + "-" + doi['name'] + '.png')
    return 0 

def  traitement_all (xml_dico):
    print("----------- Tracé de toutes les zones de le dataset fourni ------------")
    traitement_runway (xml_dico)
    traitement_tma (xml_dico)
    traitement_era (xml_dico)
    traitement_icca (xml_dico)
    traitement_doi(xml_dico)
    
    return 0

def dms_to_deg(degrees, minutes, seconds,dir):
    # Calcul du degré décimal
    dd = degrees + (minutes / 60) + (seconds / 3600)
    if (dir):
        return dd
    else:
        return -dd

def main():
    dataset = input("Veuillez saisir le nom ou le chemin du dataset.xml (version V9.0.2) à traiter (default = 4F_E0702.xml) :\n")
    
    if dataset.strip() == "" :
        dataset = "4F_E0702.xml"
    
    try:    
        with open(dataset, 'r') as file:
            xml_string = file.read()
    except:
        print ("Error: L'ouverture du Fichier {} à echoué, veuillez verifier le nom ou le chemin".format(dataset))
        exit ()
        
    xml_dico = xmltodict.parse(xml_string)
    
    menu (xml_dico)


if __name__ == "__main__":
    main()
