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
    temp_file = 'html/temp_map.html'
    # Save the map to the temporary file
    m.save(temp_file)

    # Copy the temporary file to another location
    shutil.copyfile(temp_file, 'html/temp_map_copy.html')

    # Set Firefox binary location
    options = Options()
    options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    driver = webdriver.Firefox(options=options)

    driver.get('file://' + os.getcwd() + '/html/temp_map_copy.html')
    # Maximize the browser window
    driver.maximize_window()
    # Wait for 5 seconds to ensure the map is fully loaded
    time.sleep(5)
    

    # Take a screenshot of the map and save it with a specified name
    screenshot = driver.save_screenshot(nom)
    # Close the browser and quit the webdriver
    driver.quit()

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
    for doi in xml_dico['dataset']['unit_doi_main']['unit_doi']:
        #print(doi['name'])
        coodinates =[]
        for pos in doi:
            print (pos)
            lat = float(pos['lat'])
            lon = float(pos['lon'])
            coodinates.append((lat, lon))
        print (coodinates)
        generation_image (coodinates, 'doi.png')

def main():
    with open('Artas/4F_O0502.xml', 'r') as file:
        xml_string = file.read()
        
    xml_dict = xmltodict.parse(xml_string)
    #traitement_icca(xml_dict)
    traitement_doi(xml_dict)
    #print (xml_dict)
    




if __name__ == "__main__":
    main()
