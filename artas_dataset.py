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
    while zone < 0 or zone > 9:
        print(
          "- 0 => Quitter\n"
          "- 1 => ENRTAs\n"
          "- 2 => TMAs\n"
          "- 3 => SIDs\n"
          "- 4 => STARs\n"
          "- 5 => TRAs\n"
          "- 6 => MAs\n"
          "- 7 => Air Routes\n"
          "- 8 => ICCAs\n"
          "- 9 => All\n")
        try :
            zone = int(input("Veuillez choisir le numero de la zone a tracer ou quittez (0):\n"))
        except:
            print("Erreur : Veuillez saisir un chiffre compris entre 0 et 9 correspondant a la zone SVP")
    match zone:
        case 0:
             exit ()
        case 1:
            traitement_enrta (xml_dico)
        case 2:
            traitement_tma (xml_dico)
        case 3:
            traitement_sid (xml_dico)
        case 4:
            traitement_star (xml_dico)
        case 5:
            traitement_tra (xml_dico)
        case 6:
            traitement_ma (xml_dico)
        case 7:
            traitement_air (xml_dico)
        case 8:
            traitement_icca (xml_dico)
        case 9:
            traitement_all (xml_dico)
        
def  traitement_enrta (xml_dico):
    enrta_list = xml_dico['dataset']['enrta_main']['enrta']
    if isinstance(enrta_list, dict):  # Vérifie si c'est un dictionnaire
        enrta_list = [enrta_list]  # Convertit en une liste avec un seul élément
    for enrta in enrta_list:
        coodinates =[]
        for pos in enrta['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, enrta['name'] + '.png')
    return 0 

def traitement_tma (xml_dico):
    enrta_list = xml_dico['dataset']['tma_main']['tma']
    if isinstance(enrta_list, dict):  # Vérifie si c'est un dictionnaire
        enrta_list = [enrta_list]  # Convertit en une liste avec un seul élément
    for tma in enrta_list:
        coodinates =[]
        for pos in tma['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, tma['name'] + '.png')
    return 0

def traitement_sid (xml_dico):
    sid_list = xml_dico['dataset']['sid_main']['sid']
    if isinstance(sid_list, dict):  # Vérifie si c'est un dictionnaire
        sid_list = [sid_list]  # Convertit en une liste avec un seul élément
    for sid in sid_list:
        coodinates =[]
        for pos in sid['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        generation_image (coodinates, sid['name'] + '.png')
    return 0

def traitement_star (xml_dico):
    return 0
def traitement_tra (xml_dico):
    return 0
def traitement_ma (xml_dico):
    return 0
def traitement_air (xml_dico):
    return 0
def  traitement_all (xml_dico):
    return 0
def traitement_icca (xml_dico):
    for icca in xml_dico['dataset']['icca_main']['icca']:
        print(icca['name'])
        coodinates =[]
        for pos in icca['area']['pos']:
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        print (coodinates)
        generation_image (coodinates, icca['name'] + '.png')


def traitement_doi(xml_dico):
    i=0
    for doi in xml_dico['dataset']['unit_doi_main']['unit_doi']:
        #print(doi['name'])
        coodinates =[]
    
        i=i+1
        print (doi)
        dir = 1 if "doi_long_e" in doi else -1
        lat = dms_to_deg(float(doi['doi_lat_deg']),float(doi['doi_lat_min']),float(doi['doi_lat_sec']),float(doi['doi_lat_n']))
        lon = dms_to_deg(float(doi['doi_long_deg']),float(doi['doi_long_min']),float(doi['doi_long_sec']),dir)
        coodinates.append((lat, lon))
        print (coodinates)
        generation_image (coodinates, 'doi_{}.png'.format(i))

def dms_to_deg(degrees, minutes, seconds,dir):
    # Calcul du degré décimal
    dd = degrees + (minutes / 60) + (seconds / 3600)
    if (dir):
        return dd
    else:
        return -dd

def main():
    data="4F_E0209.xml"
    #data='4F_O0502.xml'
    with open(data, 'r') as file:
        xml_string = file.read()
        
    xml_dico = xmltodict.parse(xml_string)
    
    menu (xml_dico)
    #traitement_icca(xml_dico)
    #traitement_doi(xml_dict)
    #print (xml_dict)
    




if __name__ == "__main__":
    main()
