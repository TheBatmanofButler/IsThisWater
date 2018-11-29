from flask import Flask, render_template, request, url_for, redirect, jsonify

import os
import json

app = Flask(__name__)

MAPBOX_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
STANDARD_ZOOM = 15
filepath = 'sites.json'

with open(filepath) as fp:
    sites_dict = json.load(fp)


@app.route('/', methods=['GET'])
def index():
    site = sites_dict['unchecked'][0]
    lat = site.get('lat')
    lon = site.get('lon')
    num_images_labeled = len(sites_dict['water_found']) + len(sites_dict['water_not_found'])

    print_image_log(site)

    return render_template('index.html',
                            num_images_labeled=num_images_labeled,
                            lat=lat,
                            lon=lon,
                            zoom=STANDARD_ZOOM,
                            MAPBOX_ACCESS_TOKEN=MAPBOX_ACCESS_TOKEN)


@app.route('/load_next_image', methods=['POST'])
def load_next_image():
    water_found, zoom = request.json

    site = sites_dict['unchecked'].pop(0)
    site['zoom'] = zoom
    
    if water_found:
        sites_dict['water_found'].append(site)
    else:
        sites_dict['water_not_found'].append(site)
    
    with open(filepath, 'w+') as fp:
        json.dump(sites_dict, fp)

    if not len(sites_dict['unchecked']):
        return jsonify(None)

    site = sites_dict['unchecked'][0]
    lat = site['lat']
    lon = site['lon']
    zoom = STANDARD_ZOOM
    num_images_labeled = len(sites_dict['water_found']) + len(sites_dict['water_not_found'])
    print_image_log(site)

    return jsonify([lat, lon, zoom, num_images_labeled])


def print_image_log(site):
    print(site.get('name'), site.get('site_code'))


if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)