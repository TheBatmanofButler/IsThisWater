import os
import json
import urllib
import time
import shutil

from mapbox import Static


MAPBOX_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
service = Static(access_token=MAPBOX_ACCESS_TOKEN)


class ImagesManager:

    def __init__(self, sites_data_filepath='json/sites_from_cities_0.json'):
        self._STANDARD_ZOOM = 15
        self._STATIC_DIRECTORY = 'static/'
        self._BASE_IMAGES_DIRECTORY = 'base_images/'
        self._CURRENT_IMAGE_DIRECTORY = 'current_image/'
        self._LABELED_IMAGES_DIRECTORY = 'labeled_images/'
        self._SITES_DATA_FILEPATH = sites_data_filepath
        self._IMAGE_WIDTH = 1000
        self._IMAGE_HEIGHT = 1000

        self._sites_dict = self.get_sites_dict()
        self._unchecked_sites = self._sites_dict['unchecked']
        self._water_sites = self._sites_dict['water']
        self._no_water_sites = self._sites_dict['no_water']

        self._current_site = None
        next_image_is_ready = self.initialize_next_image()

        if not next_image_is_ready:
            raise Exception('No sites left.')

    def save_sites_dict(self):
        self._sites_dict = {
            'unchecked': self._unchecked_sites,
            'water': self._water_sites,
            'no_water': self._no_water_sites
        }

        with open(self._SITES_DATA_FILEPATH, 'w+') as fp:
            json.dump(self._sites_dict, fp)

    def get_current_zoom(self):
        return self._current_site.get('zoom')

    def get_num_images_left(self):
        num_images_left = len(self._unchecked_sites)
        return num_images_left

    def classify_site(self, image_label):
        if image_label < 2:
            if image_label == 0:
                self._no_water_sites.append(self._current_site)
                label = 'no_water'
            elif image_label == 1:
                self._water_sites.append(self._current_site)
                label = 'water'

            current_image_filepath = self.get_current_image_filepath()
            labeled_image_filepath = self.get_labeled_image_filepath(label)
            shutil.copyfile(current_image_filepath, labeled_image_filepath)

        self._unchecked_sites.pop(0)
        self.delete_current_image()
        self.save_sites_dict()

    def initialize_next_image(self):
        if self._unchecked_sites:
            self._current_site = self._unchecked_sites[0]
            self._current_site['zoom'] = self._STANDARD_ZOOM
            self.load_image_from_base_dir()

            return True

        return False

    def next_image(self, image_label):
        self.classify_site(image_label)
        next_image_is_ready = self.initialize_next_image()

        return next_image_is_ready

    def update_image(self, zoom):
        download_status_code = self.download_image(zoom)

        if download_status_code == 200:
            self._current_site['zoom'] = zoom
        
        return download_status_code

    def get_sites_dict(self):
        with open(self._SITES_DATA_FILEPATH) as fp:
            sites_dict = json.load(fp)

        return sites_dict

    def print_image_log(self):
        print('Downloaded {}'.format(self._current_site.get('name')))
        print('Zoom: {}'.format(self._current_site.get('zoom')))
        print('{}.png'.format(self._current_site.get('site_code')))

    def delete_current_image(self):
        image_filepath = self.get_current_image_filepath()
        os.remove(image_filepath)

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

        response = service.image('mapbox.satellite',
                                 lon=lon,
                                 lat=lat,
                                 z=zoom,
                                 width=self._IMAGE_WIDTH,
                                 height=self._IMAGE_HEIGHT)

        return response
