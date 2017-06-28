import json
import random

from utils import scrapUniplaces, scrapBeRoomers
from utils.parametersUtils import adaptCities, get_types_array


def saveToFile(data, fileName):
    file = open(fileName + '.json', 'w+')
    json.dump(data, file)
    file.close()


def join_two_lists(list1, list2):
    num = min(len(list1), len(list2))
    result = [None] * (num * 2)
    result[::2] = list1[:num]
    result[1::2] = list2[:num]
    result.extend(list1[num:])
    result.extend(list2[num:])
    return result


def getJsonAccommodations(filters={}):
    accommodations = []

    # Adapt cities
    city = adaptCities(filters)
    type = get_types_array(filters.get('type', ''))
    filters['type'] = type

    # Requiring Uniplaces accommodations
    filters['city'] = city[1]
    uniplaces = scrapUniplaces.uniplacesAccommodations(filters)
    # saveToFile(uniplaces, '../data/salidaUniplaces')
    accommodations = accommodations + uniplaces

    # Requiring beRoomers accommodations
    filters['city'] = city[2]

    beRoomers = scrapBeRoomers.beRoomersAccommodations(filters)
    # saveToFile(beRoomers, '../data/salidaBeRoomers')
    accommodations = accommodations + beRoomers

    # random.shuffle(accommodations)
    accommodations = join_two_lists(uniplaces, beRoomers)

    return accommodations

# # TODO: meter filtros de prueba aqui
# # TODO: faltan la busqueda de barrios/universidades
# filters = dict()
# filters['city'] = 'madrid'
# filters['checkin'] = '02-01-2018'
# filters['checkout'] = '03-08-2018'
# filters['minPrice'] = '200'
# filters['maxPrice'] = '1000'
# filters['type'] = ['shared-room', 'room']
# getJsonAccommodations(filters=filters)
