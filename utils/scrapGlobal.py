import json
import random

from utils import scrapUniplaces, scrapBeRoomers


def saveToFile(data, fileName):
    file = open(fileName + '.json', 'w+')
    json.dump(data, file)
    file.close()


def adaptCities(filters):
    cities = []
    # Setafoot, uniplaces, beroomers, ...

    # USA
    cities.append(['new-york', '', 'new-york-united-states'])
    cities.append(['boston', '', 'boston-ma-united-states'])

    # Italy
    cities.append(['rome', 'rome', 'rome-italy'])
    cities.append(['florence', 'florence', 'florence-italy'])
    cities.append(['bologna', 'bologna', 'bologna-italy'])
    cities.append(['milan', 'milan', 'milan-italy'])
    cities.append(['padua', 'padua', 'padova-italy'])
    cities.append(['turin', 'turin', 'turin-italy'])

    # United Kindgom
    cities.append(['london', 'london', 'london-united-kingdom'])
    cities.append(['manchester', 'manchester', ''])
    cities.append(['leeds', 'leeds', 'leeds-united-kingdom'])
    cities.append(['cardiff', 'cardiff', 'cardiff-united-kingdom'])

    # Portugal
    cities.append(['porto', 'porto', 'porto-portugal'])
    cities.append(['lisbon', 'lisbon', 'lisboa-portugal'])
    cities.append(['coimbra', 'coimbra', ''])

    # Spain
    cities.append(['madrid', 'madrid', 'madrid-spain'])
    cities.append(['barcelona', 'barcelona', 'barcelona-spain'])
    cities.append(['valencia', 'valencia', 'valencia-spain'])
    cities.append(['granada', 'granada', 'granada-spain'])
    cities.append(['seville', 'seville', 'seville-spain'])
    cities.append(['salamanca', 'salamanca', 'salamanca-spain'])
    cities.append(['palma-de-mallorca', 'palma-de-mallorca', ''])
    cities.append(['alicante', 'alicante', 'alicante-spain'])
    cities.append(['malaga', 'malaga', 'malaga-spain'])
    cities.append(['zaragoza', 'zaragoza', 'zaragoza-spain'])
    cities.append(['cordova', 'cordova', 'cordoba-spain'])
    cities.append(['murcia', 'murcia', 'murcia-spain'])
    cities.append(['cadiz', 'cadiz', 'cadiz-spain'])

    # France
    cities.append(['paris', 'paris', 'paris-france'])

    # Germany
    cities.append(['berlin', 'berlin', 'berlin-germany'])
    cities.append(['munich', 'munich', ''])

    cityString = filters.get('city', '')

    if cityString != '':
        for city in cities:
            if city[0] == cityString:
                return city

    return ['madrid', 'madrid', 'madrid-spain']


def getJsonAccommodations(filters={}):
    accommodations = []

    # Adapt cities
    city = adaptCities(filters)

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

    random.shuffle(accommodations)

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
