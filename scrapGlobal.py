import json

import scrapBeRoomers
import scrapUniplaces


def saveToFile(data, fileName):
    file = open(fileName + '.json', 'w')
    json.dump(data, file)
    file.close()


def getJsonAccommodations(filters={}):
    accommodations = []

    # Requiring beRoomers accommodations
    beRoomers = scrapBeRoomers.beRoomersAccommodations(filters)
    saveToFile(beRoomers, 'data/salidaBeRoomers')
    accommodations = accommodations + beRoomers

    # Requiring Uniplaces accommodations
    uniplaces = scrapUniplaces.uniplacesAccommodations(filters)
    saveToFile(uniplaces, 'data/salidaUniplaces')
    accommodations = accommodations + uniplaces

    return accommodations


# TODO: meter filtros de prueba aqui
# TODO: faltan la busqueda de barrios/universidades
filters = dict()
filters['city'] = 'madrid'
filters['checkin'] = '02-01-2018'
filters['checkout'] = '03-08-2018'
filters['minPrice'] = '200'
filters['maxPrice'] = '1000'
filters['type'] = ['shared-room', 'room']
getJsonAccommodations(filters=filters)
