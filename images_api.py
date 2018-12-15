import os
import json
import urllib
import time
import shutil

from mapbox import Static

MAPBOX_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
service = Static(access_token=MAPBOX_ACCESS_TOKEN)


class ImagesManager:

    def __init__(self):
        self._STANDARD_ZOOM = 15
        self._STATIC_DIRECTORY = 'static/'
        self._BASE_IMAGES_DIRECTORY = 'base_images/'
        self._CURRENT_IMAGE_DIRECTORY = 'current_image/'
        self._LABELED_IMAGES_DIRECTORY = 'labeled_images/'
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
            label = 'water'
        else:
            self._no_water_sites.append(self._current_site)
            label = 'no_water'

        current_image_filepath = self.get_current_image_filepath()
        labeled_image_filepath = self.get_labeled_image_filepath(label)
        shutil.copyfile(current_image_filepath, labeled_image_filepath)

        self._unchecked_sites.pop(0)

    def initialize_next_image(self):
        try:
            self._current_site = self._unchecked_sites[0]
        except IndexError:
            raise Exception('out of sites')

        self._current_site['zoom'] = self._STANDARD_ZOOM

        self.load_image_from_base_dir()

    def next_image(self, water_found):
        self.classify_site(water_found)
        self.initialize_next_image()

    def update_image(self, zoom):
        download_status_code = self.download_image(zoom)

        if download_status_code == 200:
            self._current_site['zoom'] = zoom

        return download_status_code

    def get_sites_dict(self):
        with open(self._DATA_FILEPATH) as fp:
            sites_dict = json.load(fp)

        return sites_dict

    def print_image_log(self):
        print('Downloaded {}'.format(self._current_site.get('name')))
        print('Zoom: {}'.format(self._current_site.get('zoom')))
        print('{}.png'.format(self._current_site.get('site_code')))

    def delete_image(self):
        t0 = time.time()
        image_filepath = self.get_current_image_filepath()
        os.remove(image_filepath)
        print(time.time() - t0, 'delete')

    def load_image_from_base_dir(self):
        base_image_filepath = self.get_base_image_filepath()
        current_image_filepath = self.get_current_image_filepath()
        shutil.copyfile(base_image_filepath, current_image_filepath)

    def get_base_image_filepath(self):
        return self.get_image_filepath(self._BASE_IMAGES_DIRECTORY)

    def get_current_image_filepath(self):
        return self.get_image_filepath(self._CURRENT_IMAGE_DIRECTORY)

    def get_labeled_image_filepath(self, label):
        subdirectory = os.path.join(self._LABELED_IMAGES_DIRECTORY, label)
        return self.get_image_filepath(subdirectory)

    def get_image_filepath(self, subdirectory):
        site_code = self._current_site.get('site_code')
        image_filename = '{}.png'.format(site_code)
        image_filepath = os.path.join(self._STATIC_DIRECTORY,
                                      subdirectory,
                                      image_filename)

        return image_filepath

    def download_image(self, zoom):
        response = self.get_mapbox_api_response(zoom)

        if response.status_code == 200:
            image_filepath = self.get_current_image_filepath()

            with open(image_filepath, 'wb') as output:
                output.write(response.content)

            self.print_image_log()

        return response.status_code

    def get_mapbox_api_response(self, zoom):
        lat = self._current_site.get('lat')
        lon = self._current_site.get('lon')

        response = service.image('mapbox.satellite', lon=lon, lat=lat, z=zoom)

        return response
