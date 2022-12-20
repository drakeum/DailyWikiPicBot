from datetime import date, datetime
import currentimagedata as cid
import potdfunctions as pf


# Fetches the POTD from Wikipedia and stores it in variables
def store_new_potd():
    current_date = date.today()
    data = pf.fetch_potd(current_date)
    cid.image_url = data['image_src']
    cid.page_url = data["image_page_url"]
    cid.image_url_comp = data['image_src']
    cid.blurb = data['blurb']
    cid.image_date = data['image_date']
    print(
        "A new daily image has been fetched and stored! Current time: " + current_date.isoformat() + " " + datetime.now().strftime(
            "%H:%M:%S"))
