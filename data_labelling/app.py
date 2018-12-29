from flask import Flask, render_template, request, url_for, redirect, jsonify
from images_api import ImagesManager

import os
import json
import random

app = Flask(__name__)

images_manager = ImagesManager()


@app.route('/', methods=['GET'])
def index():
    num_images_labeled = images_manager.get_num_images_labeled()
    image_filepath = images_manager.get_current_image_filepath()
    zoom = images_manager.get_current_zoom()

    return render_template('index.html',
                           image_filepath=image_filepath,
                           zoom=zoom,
                           num_images_labeled=num_images_labeled)


@app.route('/update_zoom', methods=['POST'])
def update_zoom():
    zoom = int(request.json)
    download_status_code = images_manager.update_image(zoom)

    if download_status_code == 200:

        image_filepath_og = images_manager.get_current_image_filepath()

        random_num = random.randint(1e6, 1e7 - 1)
        image_filepaths_rand = '{}?dummy={}'.format(image_filepath_og, 
                                                    random_num)

        response = jsonify([image_filepaths_rand, zoom])

    else:
        response = jsonify({
            'message': 'Download failed. Check logs for details.'
        })

    response.status_code = download_status_code

    return response


@app.route('/load_next_image', methods=['POST'])
def load_next_image():
    water_found = request.json

    images_manager.next_image(water_found)

    if not images_manager._unchecked_sites:
        return jsonify(None)

    image_filepath = images_manager.get_current_image_filepath()
    zoom = images_manager.get_current_zoom()
    num_images_labeled = images_manager.get_num_images_labeled()

    return jsonify([image_filepath, zoom, num_images_labeled])


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
