import datetime

from bs4 import BeautifulSoup

from utils.parametersUtils import add_paramaters_to_link
from utils.htmlUtils import get_html_code


def apply_filters_uniplaces(link, filters):
    # Get the filters
    city = filters.get('city', '')
    checkin = filters.get('checkin', '')
    checkout = filters.get('checkout', '')
    minPrice = filters.get('minPrice', '')
    maxPrice = filters.get('maxPrice', '')
    type_copy = filters.get('type', [])

    type = list(type_copy)

    topRightLat = filters.get('topRightLat', '')
    topRightLng = filters.get('topRightLng', '')
    bottomLeftLat = filters.get('bottomLeftLat', '')
    bottomLeftLng = filters.get('bottomLeftLng', '')

    # Change the city
    link = link.replace('madrid', city)

    # Set the parameters
    parameters = {}

    if checkin != '':
        checkin = datetime.datetime.strptime(checkin, '%d-%m-%Y').strftime('%Y-%m-%d')
        parameters['move-in'] = checkin

    if checkout != '':
        checkout = datetime.datetime.strptime(checkout, '%d-%m-%Y').strftime('%Y-%m-%d')
        parameters['move-out'] = checkout

    if minPrice != '' or maxPrice != '':
        if minPrice == '':
            minPrice = '100'
        if maxPrice == '':
            maxPrice = '1500'
        parameters['budget'] = minPrice + '-' + maxPrice

    # type
    if 'host-family' in type:
        type.remove('host-family')

    if type:
        parameters['rent-types[]'] = []
        print(len(type))
        for t in type:
            if t == 'full-apartment':
                parameters['rent-types[]'].append('entire-property')
            elif t == 'room':
                parameters['rent-types[]'].append('bedroom')
            elif t == 'shared-room':
                parameters['rent-types[]'].append('bed')
            elif t == 'residence':
                parameters['accommodation-types[]'] = 'residence'

    if topRightLat != '':
        parameters['north'] = topRightLat
        parameters['east'] = topRightLng
        parameters['south'] = bottomLeftLat
        parameters['west'] = bottomLeftLng

    return add_paramaters_to_link(link, parameters)


def uniplacesAccommodations(filters={}):
    link = 'http://www.uniplaces.com/accommodation/madrid'
    link = apply_filters_uniplaces(link, filters)
    print(link)

    HTMLCode = get_html_code(link, offline_file='pruebacodigouniplaces.html', using_mock=False)
    bsObj = BeautifulSoup(HTMLCode, 'html.parser')

    titles = bsObj.findAll('a', {'class': 'offer-summary__main-link'})
    titles_string = []
    links_string = []
    for title in titles:
        titles_string.append(title.get_text().strip())

    links = bsObj.findAll('div', {'class': 'offer-summary__description'})
    for link in links:
        links_string.append(link.find_all('span')[0].get('content'))

    typologies = bsObj.findAll('div', {'class': 'offer-summary__tipology'})
    typologies_string = []
    for typology in typologies:
        tipology_aux = typology.get_text().strip()
        if tipology_aux == 'Entire property':
            tipology_aux = 'Full Apartment'
        if tipology_aux == 'Bed':
            tipology_aux = 'Shared Room'
        typologies_string.append(tipology_aux)

    # No todos los pisos tienen barrio, en las otras paginas web no aparece tampoco
    neighbourhoods = bsObj.findAll('div', {'class': 'offer-summary__neighbourhood'})
    neighbourhoods_string = []
    for neighbourhood in neighbourhoods:
        neighbourhoods_string.append(neighbourhood.get_text().strip())

    prices = bsObj.findAll('div', {'class': 'price'})
    prices_string = []

    for price in prices:
        prices_string.append(price.get_text().strip()
                             .replace(' ', ''))

    bills_string = []
    bills = bsObj.findAll('div', {'class': 'offer-summary__price'})

    for bill in bills:
        hasAllBills = False
        for child in bill.findChildren():
            if child.has_attr('class'):
                if child['class'][0] == 'offer-summary__bills':
                    hasAllBills = True
        if hasAllBills:
            bills_string.append('all bills included')
        else:
            bills_string.append('some bills included')

    pictures = bsObj.findAll('div', {'class': 'owl-carousel'})
    pictures_string = []
    for picture in pictures:
        pictures_string.append(picture.findAll('div')[0].get('data-src'))

    geoposs = bsObj.findAll('div', {'class': 'offer-geo'})
    latitudes_string = []
    longitudes_string = []
    for geopos in geoposs:
        latitudes_string.append(geopos['data-lat'])
        longitudes_string.append(geopos['data-long'])

    # Reformat links (and add tracker)

    for i in range(len(links_string)):
        # links_string[i] = 'https://www.uniplaces.com' + links_string[i]

        checkin = filters.get('checkin', '')
        checkout = filters.get('checkout', '')

        parameters = {}

        if checkin != '':
            checkin = datetime.datetime.strptime(checkin, '%d-%m-%Y').strftime('%Y-%m-%d')
            parameters['move-in'] = checkin

        if checkout != '':
            checkout = datetime.datetime.strptime(checkout, '%d-%m-%Y').strftime('%Y-%m-%d')
            parameters['move-out'] = checkout

        links_string[i] = add_paramaters_to_link(links_string[i], parameters)

        links_string[i] = links_string[i].replace('/en', '')

        links_string[i] = links_string[i].replace(':', '%3A') \
            .replace('/', '%2F') \
            .replace('?', '%3F') \
            .replace('&', '%26') \
            .replace('=', '%3D')

        links_string[i] = 'http://uniplaces.7eer.net/c/352294/206497/3534?u=' + links_string[i]

    # Here is where the magic comes true

    titles_string_aux = []
    links_string_aux = []
    tipologies_string_aux = []
    prices_string_aux = []
    bills_string_aux = []

    for i in range(len(titles_string)):
        if '-' not in prices_string[i] and 'All' not in prices_string[i]:
            titles_string_aux.append(titles_string[i])
            links_string_aux.append(links_string[i])
            tipologies_string_aux.append(typologies_string[i])
            prices_string_aux.append(prices_string[i])
            bills_string_aux.append(bills_string[i])

    titles_string = titles_string_aux
    links_string = links_string_aux
    typologies_string = tipologies_string_aux
    prices_string = prices_string_aux
    bills_string = bills_string_aux

    accommodations = []
    if len(titles_string) == len(links_string) == len(typologies_string) == len(prices_string) == len(pictures_string) == len(latitudes_string) == len(longitudes_string) == len(bills_string):
        for i in range(len(titles_string)):
            accommodation = {
                'title': titles_string[i],
                'link': links_string[i],
                'typology': typologies_string[i],
                # 'neighbourhood': neighbourhoods_string[i],
                'price': prices_string[i],
                'picture': pictures_string[i],
                'latitude': latitudes_string[i],
                'longitude': longitudes_string[i],
                'bills': bills_string[i],
                'provider': 'Uniplaces'}

            accommodations.append(accommodation)

    return accommodations
