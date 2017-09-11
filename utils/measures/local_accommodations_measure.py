import json
import os


def getAccommodationsFromFile(path_route):
    dir = os.path.dirname(__file__)
    route = '../../data/' + path_route + '.json'
    filename = os.path.join(dir, route)

    file = open(filename, 'r')
    file_string = file.read()
    file.close()

    accommodations = json.loads(file_string)

    return accommodations


accommodations_beRoomers = getAccommodationsFromFile('data_beRoomers')
accommodations_erasmusInn = getAccommodationsFromFile('data_erasmusInn')
accommodations_studyAbroadApartments = getAccommodationsFromFile('data_studyabroadapartments')

print('On BeRoomers we have ' + str(len(accommodations_beRoomers)) + ' accommodations.')
print('On erasmusInn we have ' + str(len(accommodations_erasmusInn)) + ' accommodations.')
print('On studyAbroadApartments we have ' + str(len(accommodations_studyAbroadApartments)) + ' accommodations.')

print('In total we have ' + str(len(accommodations_beRoomers) + len(accommodations_erasmusInn) + len(accommodations_studyAbroadApartments)) + ' accommodations.')