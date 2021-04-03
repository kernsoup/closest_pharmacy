import re
import requests


def get_url(link):
    contents = requests.get(link).json()
    if 'thecatapi' in link:
        url = contents[0]['url']
    else:
        url = contents['url']
    return url

def get_image_url(link):
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url(link)
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url