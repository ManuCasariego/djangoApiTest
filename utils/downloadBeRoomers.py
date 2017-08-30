import json
import os
from urllib.error import HTTPError
from urllib.request import urlopen

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


def save_to_file(dir_obj, accommodations_array, accommodations_name):
    filename = os.path.join(dir_obj, '../data/' + accommodations_name + '.json')

    file = open(filename, 'w+')
    json.dump(accommodations_array, file)
    file.close()


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

            # if city == 'roma, italy':
            #     city = 'rome'
            # elif city == 'milano, italy':
            #     city = 'milan'
            # elif city == 'warsaw, poland':
            #     city = 'warsaw'
            # elif city == 'istanbul, t\u00fcrkiye':
            #     city = 'istanbul'
            # elif city == 'madrid, spain':
            #     city = 'madrid'
            # elif city == 'barcelona, spain':
            #     city = 'barcelona'
            # elif city == 'poznan, poland':
            #     city = 'poznan'
            # elif city == 'berlin, germany':
            #     city = 'berlin'
            # elif city == 'lodz, poland':
            #     city = 'lodz'
            # elif city == 'granada, spain':
            #     city = 'granada'
            # elif city == 'london, united kingdom':
            #     city = 'london'
            # elif city == 'florence, italy':
            #     city = 'florence'
            # elif city == 'zaragoza, spain':
            #     city = 'zaragoza'

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
            # TODO: Deal with the link, referral and link link

            # latitude and longitude
            location = accommodation.get('coordinates')

            longitude = location.get('lat')
            longitude = str(longitude)

            latitude = location.get('lon')
            latitude = str(latitude)

            # typology
            typology = accommodation.get('propertyType')

            if propertiesTypes.get(typology):
                propertiesTypes[typology] += 1
            else:
                propertiesTypes[typology] = 1

            # if typology == 'Room':
            #     typology = 'Bedroom'
            # elif typology == 'complete-apartment':
            #     typology = 'Full Apartment'
            # elif typology == 'Student Residence':
            #     typology = 'Residence'
            # elif typology == 'shared-flat':
            #     typology = 'shared-flat'

            # picture
            picture = accommodation.get('defaultPhoto')
            #
            # # occupancies
            # occupancies = accommodation.get(occupancies_string)
            # new_occupancies = []
            # for occupancy in occupancies:
            #     first_date = occupancy.get('to')
            #     second_date = occupancy.get('from')
            #
            #     first_date_array = first_date.split('-')
            #     first_date = first_date_array[2] + '-' + first_date_array[1] + '-' + first_date_array[0]
            #
            #     second_date_array = second_date.split('-')
            #     second_date = second_date_array[2] + '-' + second_date_array[1] + '-' + second_date_array[0]
            #
            #     new_occupancy = {
            #         'to': first_date,
            #         'from': second_date
            #     }
            #     new_occupancies.append(new_occupancy)

            # occupancies = accommodation.get('availability')

            bills = accommodation.get('billsIncluded')
            if bills == 'Some Bills Included':
                bills = 'some bills included'
            elif bills == 'Bills Included':
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
                # occupancies_string: occupancies,
                occupancies_string: [],
            })

        # Order the different accommodation in each city
        # accommodations_rome = []
        # accommodations_milan = []
        # accommodations_warsaw = []
        # accommodations_istanbul = []
        # accommodations_madrid = []
        # accommodations_barcelona = []
        # accommodations_poznan = []
        # accommodations_berlin = []
        # accommodations_lodz = []
        # accommodations_granada = []
        # accommodations_london = []
        # accommodations_florence = []
        # accommodations_zaragoza = []
        #
        # for accommodation in accommodations:
        #     city = accommodation.get('city')
        #
        #     if city == 'rome':
        #         accommodations_rome.append(accommodation)
        #     elif city == 'milan':
        #         accommodations_milan.append(accommodation)
        #     elif city == 'warsaw':
        #         accommodations_warsaw.append(accommodation)
        #     elif city == 'istanbul':
        #         accommodations_istanbul.append(accommodation)
        #     elif city == 'madrid':
        #         accommodations_madrid.append(accommodation)
        #     elif city == 'barcelona':
        #         accommodations_barcelona.append(accommodation)
        #     elif city == 'poznan':
        #         accommodations_poznan.append(accommodation)
        #     elif city == 'berlin':
        #         accommodations_berlin.append(accommodation)
        #     elif city == 'lodz':
        #         accommodations_lodz.append(accommodation)
        #     elif city == 'granada':
        #         accommodations_granada.append(accommodation)
        #     elif city == 'london':
        #         accommodations_london.append(accommodation)
        #     elif city == 'florence':
        #         accommodations_florence.append(accommodation)
        #     elif city == 'zaragoza':
        #         accommodations_zaragoza.append(accommodation)

        dir = os.path.dirname(__file__)
        # save_to_file(dir, accommodations, 'data_erasmusInn')
        # save_to_file(dir, accommodations_rome, 'accommodations_eri_rome')
        # save_to_file(dir, accommodations_milan, 'accommodations_eri_milan')
        # save_to_file(dir, accommodations_warsaw, 'accommodations_eri_warsaw')
        # save_to_file(dir, accommodations_istanbul, 'accommodations_eri_istanbul')
        # save_to_file(dir, accommodations_madrid, 'accommodations_eri_madrid')
        # save_to_file(dir, accommodations_barcelona, 'accommodations_eri_barcelona')
        # save_to_file(dir, accommodations_poznan, 'accommodations_eri_poznan')
        # save_to_file(dir, accommodations_berlin, 'accommodations_eri_berlin')
        # save_to_file(dir, accommodations_lodz, 'accommodations_eri_lodz')
        # save_to_file(dir, accommodations_granada, 'accommodations_eri_granada')
        # save_to_file(dir, accommodations_london, 'accommodations_eri_london')
        # save_to_file(dir, accommodations_florence, 'accommodations_eri_florence')
        # save_to_file(dir, accommodations_zaragoza, 'accommodations_eri_zaragoza')
    print(cities)
    print(propertiesTypes)


beRoomersAccommodations()
