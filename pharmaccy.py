import requests
import distance
import pygame
import os


def get_the_coords(geocoder_request):
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        main = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if main != []:
            coords = main[0]["GeoObject"]["Point"]["pos"]
            return ','.join(coords.split())
        else:
            print("Неверный адрес")
            sys.exit()


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "a6b269da-f239-4d73-9d85-ab0d4c8f0375"

address_ll = get_the_coords(f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={input()}/&format=json")

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]


point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

map_params = {
    "l": "map",
    "pt": f"{org_point},pmb~{address_ll},pma"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

print(org_name, org_address["address"], org_address["Hours"]["text"], sep='\n')
print(f"Расстояние: {int(distance.lonlat_distance(list(map(float, address_ll.split(','))), point))} метров")

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)