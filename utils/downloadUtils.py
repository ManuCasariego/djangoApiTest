import json
import os


def save_to_file(dir_obj, accommodations_array, accommodations_name):
    print('se va a guardar el fichero ', accommodations_name)
    filename = os.path.join(dir_obj, '../data/' + accommodations_name + '.json')

    file = open(filename, 'w+')
    json.dump(accommodations_array, file)
    file.close()
