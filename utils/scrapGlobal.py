import json

from utils import scrapUniplaces, scrapBeRoomers, scrapStudyAbroadApartments
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


def join_three_lists(list1, list2, list3):
    num = min(len(list1), len(list2), len(list3))
    result = [None] * (num * 3)
    result[::3] = list1[:num]
    result[1::3] = list2[:num]
    result[2::3] = list3[:num]
    result.extend(list1[num:])
    result.extend(list2[num:])
    result.extend(list3[num:])
    return result


def getJsonAccommodations(filters={}):

    # Adapt cities
    city = adaptCities(filters)
    type = get_types_array(filters.get('type', ''))
    filters['type'] = type

    # Requiring Uniplaces accommodations
    filters['city'] = city[1]
    if city[1] != '':
        uniplaces = scrapUniplaces.uniplacesAccommodations(filters)
        # saveToFile(uniplaces, '../data/salidaUniplaces')
    else:
        uniplaces = []

    # Requiring beRoomers accommodations
    filters['city'] = city[2]
    if city[2] != '':
        beRoomers = scrapBeRoomers.beRoomersAccommodations(filters)
        # saveToFile(beRoomers, '../data/salidaBeRoomers')
    else:
        beRoomers = []

    # Requiring studyAbroadApartments accommodations
    filters['city'] = city[3]
    if city[3] != '':
        studyAbroadApartments = []
        pass
        # TODO: studyAbroad needs time
        # studyAbroadApartments = scrapStudyAbroadApartments.studyAbroadApartmentsAccommodations(filters)
    else:
        studyAbroadApartments = []

    # random.shuffle(accommodations)
    accommodations = join_three_lists(uniplaces, beRoomers, studyAbroadApartments)

    return accommodations
