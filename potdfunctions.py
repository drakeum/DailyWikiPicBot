import requests as requests
import htmlparser

SESSION = requests.Session()
ENDPOINT = "https://en.wikipedia.org/w/api.php"
ENDPOINT2 = "https://commons.wikimedia.org/w/api.php"


# Retrieves the current POTD from Wikipedia and returns a JSON containing
# the filename, POTD page url, file page url, image upload date, and the image's blurb
def fetch_potd(current_date):
    date_i = current_date.isoformat()
    title = "Template:POTD_protected/" + date_i

    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "images",
        "titles": title
    }

    response = SESSION.get(url=ENDPOINT, params=params)
    data = response.json()
    filename = data["query"]["pages"][0]["images"][0]["title"]
    # print(filename)
    image_page_url = "https://en.wikipedia.org/wiki/" + title
    image_data = {
        "filename": filename,
        "image_page_url": image_page_url,
        "image_src": fetch_image_src(filename),
        "image_date": fetch_image_upload_date(filename),
        "blurb": fetch_potd_blurb(filename)
    }

    return image_data


# Returns the direct url of an image file on Wikipedia that is set to a resolution of 1920-x pixels
def fetch_image_src(filename):
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": filename
    }

    response = SESSION.get(url=ENDPOINT, params=params)
    data = response.json()
    # print(data)
    page = next(iter(data["query"]["pages"].values()))
    # print(page)
    image_info = page["imageinfo"][0]
    # print(image_info)
    image_url = image_info["url"]
    make_picture_resolution_1920(image_url)
    return image_url


# Returns the blurb (or description) of an image on Wikipedia
def fetch_potd_blurb(filename):
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "imageinfo",
        "iiprop": "extmetadata",
        "titles": filename
    }

    response = SESSION.get(url=ENDPOINT2, params=params)
    data = response.json()
    description_raw = data["query"]["pages"][0]["imageinfo"][0]["extmetadata"]["ImageDescription"]["value"]
    print(data)
    description = htmlparser.strip_tags(description_raw)
    return description


def fetch_image_upload_date(filename):
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "imageinfo",
        "iiprop": "extmetadata",
        "titles": filename
    }

    response = SESSION.get(url=ENDPOINT, params=params)
    data = response.json()
    # print(data)
    date_raw = data["query"]["pages"][0]["imageinfo"][0]["extmetadata"]["DateTimeOriginal"]["value"]
    # print(date_raw)
    return date_raw


# Transforms an image url on Wikipedia to the same one, but with some stuff added to have
# the picture be 1920-x pixels (this is so that Discord will embed it instantly (hopefully))
def make_picture_resolution_1920(url):
    # print(url + '\n')
    after_commons_index = url.find('commons') + 8
    up_to_commons_sub = url[0:after_commons_index]
    after_commons_sub = url[after_commons_index:]
    thumb = "thumb/"
    # print(up_to_commons_sub + '\n')
    # print(after_commons_sub + '\n')

    second_slash_index = after_commons_sub.find("/", after_commons_sub.find("/") + 1) + 1
    between_thumb_and_image = after_commons_sub[:second_slash_index]
    only_image = after_commons_sub[second_slash_index:]

    # print(between_thumb_and_image)
    # print(only_image)

    final_url = up_to_commons_sub + thumb + between_thumb_and_image + only_image + "/1920px-" + only_image
    # print(final_url)
    return final_url
