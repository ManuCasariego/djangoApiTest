import re

from bs4 import BeautifulSoup

from utils.parametersUtils import add_paramaters_to_link
from utils.htmlUtils import get_html_code


def apply_filters_be_roomers(link, filters):
    parameters = {}

    city = filters.get('city', '')
    checkin = filters.get('checkin', '')
    checkout = filters.get('checkout', '')
    minPrice = filters.get('minPrice', '')
    maxPrice = filters.get('maxPrice', '')
    type_aux = filters.get('type', [])
    type = list(type_aux)

    # Change the city
    link = link.replace('madrid-spain', city)

    if checkin != '':
        parameters['checkin'] = checkin

    if checkout != '':
        parameters['checkout'] = checkout

    if minPrice != '':
        parameters['minPrice'] = minPrice

    if maxPrice != '':
        parameters['maxPrice'] = maxPrice

    if 'shared-room' in type:
        type.remove('shared-room')

    added_the_type_flag = False
    if type:
        types = ''
        for t in type:
            if types != '':
                types += '%2C'
            if t == 'full-apartment':
                types += 'complete-apartment'
                if not added_the_type_flag:
                    link += '/apartments-for-rent'
                    added_the_type_flag = True
            elif t == 'room':
                types += 'shared-flat'
                if not added_the_type_flag:
                    link += '/rooms-for-rent'
                    added_the_type_flag = True
            elif t == 'host-family':
                types += 'host-family'
                if not added_the_type_flag:
                    link += '/homestay'
                    added_the_type_flag = True
            elif t == 'residence':
                types += 'student-hall'
                if not added_the_type_flag:
                    link += '/student-halls'
                    added_the_type_flag = True
        parameters['type'] = types

    return add_paramaters_to_link(link, parameters)


def beRoomersAccommodations(filters={}):
    accommodations = []
    link = 'https://www.beroomers.com/s/madrid-spain'
    link = apply_filters_be_roomers(link, filters)
    print(link)
    HTMLCode = get_html_code(link, offline_file='pruebacodeberoomers.html', using_mock=False)
    if HTMLCode is not None:
        bsObj = BeautifulSoup(HTMLCode, 'html.parser')

        links = bsObj.findAll('section', {'class': 'image-gallery'})
        links_string = []
        pictures_string = []
        typologies_string = []
        titles_string = []
        prices_string = []
        latitudes_string = []
        longitudes_string = []
        bills_string = []

        for link in links:
            links_string.append(link.findAll('a')[0]['href'])
            pictures_string.append(link.findAll('div', {'class': 'image-gallery-slide'})[0].img['src'])
            tipology = link.findAll('div', {'class': 'ProductCardMainProperties-type'})[0].span.get_text()
            if tipology == 'Shared Flat' or tipology == 'Piso Compartido':
                tipology = 'Bedroom'
            elif tipology == 'Complete Apartment' or tipology == 'Apartamento Completo':
                tipology = 'Full Apartment'
            elif tipology == 'Student Hall' or tipology == 'Residencia':
                tipology = 'Residence'

            typologies_string.append(tipology)
            titles_string.append(link.findAll('span', {'class': 'ProductCardMainProperties-info-title'})[0].get_text())

        prices = bsObj.findAll('span', {'class': 'BoxPrice-price'})

        for price in prices:
            prices_string.append(price.get_text())

        results = re.findall(pattern=r'coordinates":{"lat":.*?,.*?,', string=HTMLCode)

        bills = bsObj.findAll('span', {'class': 'BoxPrice-billsIncluded-label'})

        for bill in bills:
            bill_aux = bill.get_text()
            if bill_aux == 'Bills Included':
                bills_string.append('all bills included')
            else:
                bills_string.append('some bills included')

        for result in results:
            latitudes_string.append(result.split('"lat":')[1].split(',')[0])
            longitudes_string.append(result.split('"lon":')[1].split('}')[0])

        # Reformat links (and add tracker) and pictures

        for i in range(len(pictures_string)):
            pictures_string[i] = 'http://www.beroomers.com' + pictures_string[i]

        for i in range(len(links_string)):
            links_string[i] = 'https://www.beroomers.com' + links_string[i]
            # Tracker beRoomers
            links_string[i] = add_paramaters_to_link(links_string[i], {
                'affiliate': 'setafoot',
                'utm_source': 'setafoot',
                'utm_medium': 'afiliacion',
                'utm_campaign': 'aff_setafoot'
            })

        for i in range(len(links_string)):
            accommodation = {
                'title': titles_string[i],
                'link': links_string[i],
                'typology': typologies_string[i],
                'price': prices_string[i],
                'picture': pictures_string[i],
                'latitude': latitudes_string[i],
                'longitude': longitudes_string[i],
                'bills': bills_string[i],
                'provider': 'BeRoomers'
            }
            accommodations.append(accommodation)

    return accommodations
