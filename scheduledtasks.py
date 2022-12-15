from datetime import date, datetime
import currentimagedata as cid
import potdfunctions as pf

CURRENT_DATE = date.today()


def store_new_potd():
    data = pf.fetch_potd(CURRENT_DATE)
    image_url = data['image_src']
    cid.image_url = data['image_src']
    cid.page_url = data["image_page_url"]
    cid.image_url_comp = pf.make_picture_resolution_1920(image_url)
    cid.blurb = data['blurb']
    print(
        "A new daily image has been fetched and stored! Current time: " + CURRENT_DATE.isoformat() + " " + datetime.now().strftime(
            "%H:%M:%S"))
