import string
import random
import os
import shutil
import validators
import urllib.request
from redfin import Redfin

class RedFinImages():

    def __init__(self):
        self.client = Redfin()

    def validate_url(self, raw):
        if validators.url(raw):
            api_url = raw.replace('https://www.redfin.com','')
            initial_info = self.client.initial_info(api_url)
            if initial_info['payload']['responseCode'] != 200:
                return "Bad URL"
        else:
            res = self.client.search(raw)
            if res['errorMessage'] == 'Success':
                api_url = res['payload']['sections'][0]['rows'][0]['url']
                initial_info = self.client.initial_info(api_url)
            else:
                return "Can not find address"
        return initial_info

    def get_random_string(self, length=32):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def download_images(self, url):
        stat = self.validate_url(url)
        if stat == False:
            return False
        property_id = stat['payload']['propertyId']
        listing_id = stat['payload']['listingId']
        mls_data = self.client.avm_details(property_id, listing_id)

        image_url  = stat['payload']['preloadImageUrls'][0]

        i = image_url.split('_')
        dir = self.get_random_string()
        os.mkdir('images')
        os.mkdir('images/{dir}'.format(dir=dir))
        for x in range(1,11):
            i_url = i[0] + '_' + str(x) + '_' + i[1]

            try:
                urllib.request.urlretrieve(i_url, "images/"+dir+"/img_"+str(x)+".jpg")
            except:
                continue
        shutil.make_archive('images/{dir}'.format(dir=dir), 'zip', 'images/{dir}'.format(dir=dir))
        return dir
