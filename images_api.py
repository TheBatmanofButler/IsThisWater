import os
import json
import urllib
import time


class ImagesManager:

    def __init__(self):
        self._MAPBOX_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
        self._STANDARD_ZOOM = 15
        self._STATIC_DIRECTORY = 'static/'
        self._IMAGES_DIRECTORY = 'images/'
        self._DATA_FILEPATH = 'sites.json'

        self._sites_dict = self.get_sites_dict()
        self._unchecked_sites = self._sites_dict['unchecked']
        self._water_sites = self._sites_dict['water']
        self._no_water_sites = self._sites_dict['no_water']

        self._current_site = None
        self.initialize_next_image()

    def save_sites_dict(self):
        self._sites_dict = {
            'unchecked': self._unchecked_sites,
            'water_found': self._water_sites,
            'water_not_found': self._no_water_sites
        }

        with open(self._DATA_FILEPATH, 'w+') as fp:
            json.dump(self._sites_dict, fp)

    def get_current_zoom(self):
        return self._current_site.get('zoom')

    def get_num_images_labeled(self):
        num_images_labeled = len(self._water_sites) + len(self._no_water_sites)

        return num_images_labeled

    def classify_site(self, water_found):
        if water_found:
            self._water_sites.append(self._current_site)
        else:
            self._no_water_sites.append(self._current_site)

        self._unchecked_sites.pop(0)

    def initialize_next_image(self):
        try:
            self._current_site = self._unchecked_sites[0]
        except IndexError:
            raise Exception('out of sites')

        self._current_site['zoom'] = self._STANDARD_ZOOM

        self.download_image()

    def next_image(self, water_found):
        self.classify_site(water_found)
        self.initialize_next_image()

    def update_image(self, zoom):
        self.delete_image()
        self._current_site['zoom'] = zoom
        self.download_image()

    def get_sites_dict(self):
        with open(self._DATA_FILEPATH) as fp:
            sites_dict = json.load(fp)

        return sites_dict

    def print_image_log(self):
        print('Downloaded {} ({}.png)'.format(
              self._current_site.get('name'),
              self._current_site.get('site_code')))

    def get_current_image_filepath(self):
        site_code = self._current_site.get('site_code')
        image_filename = '{}.png'.format(site_code)
        image_filepath = os.path.join(self._STATIC_DIRECTORY,
                                      self._IMAGES_DIRECTORY,
                                      image_filename)

        return image_filepath

    def delete_image(self):
        t0 = time.time()
        image_filepath = self.get_current_image_filepath()
        os.remove(image_filepath)
        print(time.time() - t0, 'delete')

    def download_image(self):
        t0 = time.time()
        image_url = self.get_image_url()
        image_filepath = self.get_current_image_filepath()
        urllib.request.urlretrieve(image_url, image_filepath)

        self.print_image_log()
        print(time.time() - t0, 'download')

    def get_image_url(self):
        lat = self._current_site.get('lat')
        lon = self._current_site.get('lon')
        zoom = self._current_site.get('zoom')

        return 'https://api.mapbox.com/v4/mapbox.satellite/{},{},{}/1000x1000.png32?access_token={}'.format(lon, lat, zoom, self._MAPBOX_ACCESS_TOKEN)
