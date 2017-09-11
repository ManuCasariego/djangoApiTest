import json
import os
from urllib.error import HTTPError
from urllib.request import urlopen
from downloadUtils import save_to_file

# https://www.beroomers.com/load-more?page=2
# https://www.beroomers.com/load-more?page=1

occupancies_string = 'occupancies'
bills_string = 'bills'
picture_string = 'picture'
typology_string = 'typology'
provider_string = 'provider'
city_string = 'city'
id_string = 'id'
title_string = 'title'
price_string = 'price'
longitude_string = 'longitude'
link_string = 'link'
latitude_string = 'latitude'


def get_html_code(link):
    print('This link is going to be scraped: ' + link)

    # Optional: Check url well formed
    try:
        fp = urlopen(link)
    except HTTPError as e:
        print(e)
        print('--------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------')
        print('esta pagina esta perdida: ' + link)
        print('--------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------')
        # return null, break, or do some other "Plan b"
        return None
    if fp is None:
        print('URL not found')
    else:
        # program continues
        print('Program continues')
    code = fp.read().decode('utf8')
    fp.close()
    return code


def beRoomersAccommodations():
    firstLink = 'https://www.beroomers.com/load-more?page=1'
    apartment_count_html_code = get_html_code(firstLink)

    apartment_count_json_data = json.loads(apartment_count_html_code)

    number_of_pages = (apartment_count_json_data.get('pagination').get(
        'totalResults') - 1) / apartment_count_json_data.get('pagination').get('pageSize')
    print('There are %d pages.' % (number_of_pages))

    number_of_pages = int(number_of_pages)

    accommodations = []

    accommodations_new_york = []
    accommodations_boston = []
    accommodations_rome = []
    accommodations_florence = []
    accommodations_bologna = []
    accommodations_milan = []
    accommodations_padua = []
    accommodations_turin = []
    accommodations_london = []
    accommodations_leeds = []
    accommodations_cardiff = []
    accommodations_porto = []
    accommodations_lisbon = []
    accommodations_paris = []
    accommodations_berlin = []
    accommodations_madrid = []
    accommodations_barcelona = []
    accommodations_valencia = []
    accommodations_granada = []
    accommodations_seville = []
    accommodations_salamanca = []
    accommodations_alicante = []
    accommodations_malaga = []
    accommodations_zaragoza = []
    accommodations_cordova = []
    accommodations_murcia = []
    accommodations_cadiz = []

    cities = {}
    propertiesTypes = {}

    for i in range(number_of_pages + 1):
        paging_link = 'https://www.beroomers.com/load-more?page=' + str(i + 1)

        paging_html_code = get_html_code(paging_link)

        if paging_html_code == None:
            paging_html_code = '{"results":[]}'

        paging_json_data = json.loads(paging_html_code)

        # print(len(paging_json_data['apartments']))
        for accommodation in paging_json_data.get('results'):
            # city
            city = accommodation.get('city')

            if cities.get(city):
                cities[city] += 1
            else:
                cities[city] = 1

            if city == 'New York':
                city = 'new-york'
            elif city == 'Boston (MA)':
                city = 'boston'
            elif city == 'Rome':
                city = 'rome'
            elif city == 'Florence':
                city = 'florence'
            elif city == 'Bologna':
                city = 'bologna'
            elif city == 'Milan':
                city = 'milan'
            elif city == 'Padua' or city == 'Padova':
                city = 'padua'
            elif city == 'Turin':
                city = 'turin'
            elif city == 'London':
                city = 'london'
            elif city == 'Leeds, United Kingdom':
                city = 'leeds'
            elif city == 'Cardiff':
                city = 'cardiff'
            elif city == 'Porto':
                city = 'porto'
            elif city == 'Paris':
                city = 'paris'
            elif city == 'Berlin':
                city = 'berlin'
            elif city == 'Madrid':
                city = 'madrid'
            elif city == 'Barcelona':
                city = 'barcelona'
            elif city == 'Valencia':
                city = 'valencia'
            elif city == 'Granada':
                city = 'granada'
            elif city == 'Seville':
                city = 'seville'
            elif city == 'Salamanca':
                city = 'salamanca'
            elif city == 'Alicante':
                city = 'alicante'
            elif city == 'Malaga':
                city = 'malaga'
            elif city == 'Zaragoza':
                city = 'zaragoza'
            elif city == 'Córdoba':
                city = 'cordova'
            elif city == 'Murcia':
                city = 'murcia'
            elif city == 'Cadiz':
                city = 'cadiz'

            # id
            id = accommodation.get('id', 0)
            id = 'BER-' + str(id)

            # title
            title = accommodation.get('title', 'Accommodation')

            # price
            currency = accommodation.get('currency').get('isoCode')
            price = accommodation.get('price')
            price = str(price)

            if currency == 'EUR':
                price = price + '€'
            elif currency == 'GBP':
                price = price + '£'
            elif currency == 'USD':
                price = price + '$'
            elif currency == 'PLN':
                price = price + 'zł'
            elif currency == 'TRY':
                price = price + 'TRY'

            # link
            link = accommodation.get('url').get('en')
            link = 'https://beroomers.com' + link
            link = link + '?affiliate=setafoot&utm_source=setafoot&utm_medium=afiliacion&utm_campaign=aff_setafoot'

            # latitude and longitude
            location = accommodation.get('coordinates')

            longitude = location.get('lon')
            longitude = str(longitude)

            latitude = location.get('lat')
            latitude = str(latitude)

            # typology
            typology = accommodation.get('propertyType')

            if propertiesTypes.get(typology):
                propertiesTypes[typology] += 1
            else:
                propertiesTypes[typology] = 1

            if typology == 'shared-flat':
                typology = 'Bedroom'
            elif typology == 'complete-apartment':
                typology = 'Full Apartment'
            elif typology == 'student-hall':
                typology = 'Residence'
            elif typology == 'host-family':
                continue

            # picture
            picture = accommodation.get('defaultPhoto')
            picture = 'https://www.beroomers.com' + picture

            # occupancies
            occupancies = accommodation.get('occupancies')
            new_occupancies = []
            for occupancy in occupancies:
                first_date = occupancy.get('dateTo')
                second_date = occupancy.get('dateFrom')

                first_date_array = first_date.split('-')
                first_date = first_date_array[2] + '-' + first_date_array[1] + '-' + first_date_array[0]

                second_date_array = second_date.split('-')
                second_date = second_date_array[2] + '-' + second_date_array[1] + '-' + second_date_array[0]

                new_occupancy = {
                    'to': first_date,
                    'from': second_date
                }
                new_occupancies.append(new_occupancy)

            bills = accommodation.get('billsIncluded')
            bills = bills.lower()
            if bills == 'bills included':
                bills = 'all bills included'

            accommodations.append({
                city_string: city,
                id_string: id,
                title_string: title,
                price_string: price,
                link_string: link,
                latitude_string: latitude,
                longitude_string: longitude,
                provider_string: 'BeRoomers',
                typology_string: typology,
                picture_string: picture,
                bills_string: bills,
                occupancies_string: new_occupancies,
            })

    for accommodation in accommodations:
        city = accommodation.get('city')
        if city == 'new-york':
            accommodations_new_york.append(accommodation)
        elif city == 'boston':
            accommodations_boston.append(accommodation)
        elif city == 'rome':
            accommodations_rome.append(accommodation)
        elif city == 'florence':
            accommodations_florence.append(accommodation)
        elif city == 'bologna':
            accommodations_bologna.append(accommodation)
        elif city == 'milan':
            accommodations_milan.append(accommodation)
        elif city == 'padua':
            accommodations_padua.append(accommodation)
        elif city == 'turin':
            accommodations_turin.append(accommodation)
        elif city == 'london':
            accommodations_london.append(accommodation)
        elif city == 'leeds':
            accommodations_leeds.append(accommodation)
        elif city == 'cardiff':
            accommodations_cardiff.append(accommodation)
        elif city == 'porto':
            accommodations_porto.append(accommodation)
        elif city == 'lisbon':
            accommodations_lisbon.append(accommodation)
        elif city == 'paris':
            accommodations_paris.append(accommodation)
        elif city == 'berlin':
            accommodations_berlin.append(accommodation)
        elif city == 'madrid':
            accommodations_madrid.append(accommodation)
        elif city == 'barcelona':
            accommodations_barcelona.append(accommodation)
        elif city == 'valencia':
            accommodations_valencia.append(accommodation)
        elif city == 'granada':
            accommodations_granada.append(accommodation)
        elif city == 'seville':
            accommodations_seville.append(accommodation)
        elif city == 'salamanca':
            accommodations_salamanca.append(accommodation)
        elif city == 'alicante':
            accommodations_alicante.append(accommodation)
        elif city == 'malaga':
            accommodations_malaga.append(accommodation)
        elif city == 'zaragoza':
            accommodations_zaragoza.append(accommodation)
        elif city == 'cordova':
            accommodations_cordova.append(accommodation)
        elif city == 'murcia':
            accommodations_murcia.append(accommodation)
        elif city == 'cadiz':
            accommodations_cadiz.append(accommodation)

    dir = os.path.dirname(__file__)
    save_to_file(dir, accommodations, 'data_beRoomers')
    save_to_file(dir, accommodations_new_york, 'accommodations_ber_new_york')
    save_to_file(dir, accommodations_boston, 'accommodations_ber_boston')
    save_to_file(dir, accommodations_rome, 'accommodations_ber_rome')
    save_to_file(dir, accommodations_florence, 'accommodations_ber_florence')
    save_to_file(dir, accommodations_bologna, 'accommodations_ber_bologna')
    save_to_file(dir, accommodations_milan, 'accommodations_ber_milan')
    save_to_file(dir, accommodations_padua, 'accommodations_ber_padua')
    save_to_file(dir, accommodations_turin, 'accommodations_ber_turin')
    save_to_file(dir, accommodations_london, 'accommodations_ber_london')
    save_to_file(dir, accommodations_leeds, 'accommodations_ber_leeds')
    save_to_file(dir, accommodations_cardiff, 'accommodations_ber_cardiff')
    save_to_file(dir, accommodations_porto, 'accommodations_ber_porto')
    save_to_file(dir, accommodations_lisbon, 'accommodations_ber_lisbon')
    save_to_file(dir, accommodations_paris, 'accommodations_ber_paris')
    save_to_file(dir, accommodations_berlin, 'accommodations_ber_berlin')
    save_to_file(dir, accommodations_madrid, 'accommodations_ber_madrid')
    save_to_file(dir, accommodations_barcelona, 'accommodations_ber_barcelona')
    save_to_file(dir, accommodations_valencia, 'accommodations_ber_valencia')
    save_to_file(dir, accommodations_granada, 'accommodations_ber_granada')
    save_to_file(dir, accommodations_seville, 'accommodations_ber_seville')
    save_to_file(dir, accommodations_salamanca, 'accommodations_ber_salamanca')
    save_to_file(dir, accommodations_alicante, 'accommodations_ber_alicante')
    save_to_file(dir, accommodations_malaga, 'accommodations_ber_malaga')
    save_to_file(dir, accommodations_zaragoza, 'accommodations_ber_zaragoza')
    save_to_file(dir, accommodations_cordova, 'accommodations_ber_cordova')
    save_to_file(dir, accommodations_murcia, 'accommodations_ber_murcia')
    save_to_file(dir, accommodations_cadiz, 'accommodations_ber_cadiz')
    # print(cities)
    # print(propertiesTypes)


beRoomersAccommodations()
