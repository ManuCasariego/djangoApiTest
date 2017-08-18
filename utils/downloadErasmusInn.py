import json
import os
from urllib.error import HTTPError
from urllib.request import urlopen

# https://www.studyabroadapartments.com/api/apartments.json?q=%7B%22page%22:1%7D
# https://www.studyabroadapartments.com/api/apartments.json?q=%7B"page":1%7D
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


def erasmusInnAccommodations():
    firstLink = 'https://www.erasmusinn.com/partner/nestpickfeed'
    apartment_count_html_code = get_html_code(firstLink)

    apartment_count_json_data = json.loads(apartment_count_html_code)

    number_of_pages = apartment_count_json_data['total_page']
    print('There are %d pages.' % (number_of_pages))

    accommodations = []

    cities = {}

    for i in range(number_of_pages):
        paging_link = 'https://www.erasmusinn.com/partner/nestpickfeed?page=' + str(i + 1)

        paging_html_code = get_html_code(paging_link)

        if paging_html_code == None:
            paging_html_code = '{"properties":[]}'

        paging_json_data = json.loads(paging_html_code)

        # print(len(paging_json_data['apartments']))
        for accommodation in paging_json_data.get('properties'):
            # city
            city = accommodation.get('location').get('city')

            if cities.get(city):
                cities[city] += 1
            else:
                cities[city] = 1
            # id
            id = accommodation.get('property code', 0)
            id = 'ERI-' + str(id)

            # title
            title = accommodation.get('name', 'Accommodation')

            # price
            currency = accommodation.get('price').get('currency')
            price = accommodation.get('price').get('value')

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
            link = accommodation.get('property URL')

            # latitude and longitude
            location = accommodation.get('location').get('geocoordinates')

            location_array = location.split(',')

            latitude = float(location_array[0].replace(' ', ''))
            longitude = float(location_array[1].replace(' ', ''))

            latitude = str(latitude)
            longitude = str(longitude)

            # typology
            typology = accommodation.get('type')

            if typology == 'Room':
                typology = 'Bedroom'
            elif typology == 'Apartment':
                typology = 'Full Apartment'
            elif typology == 'Student Residence':
                typology = 'Residence'

            # picture
            picture = accommodation.get('photos')[0]
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

            occupancies = accommodation.get('availability')

            accommodations.append({
                city_string: city,
                id_string: id,
                title_string: title,
                price_string: price,
                link_string: link,
                latitude_string: latitude,
                longitude_string: longitude,
                provider_string: 'ErasmusInn',
                typology_string: typology,
                picture_string: picture,
                bills_string: 'all bills included',
                occupancies_string: occupancies
            })

        # Order the different accommodation in each city

        accommodations_new_york = []
        accommodations_barcelona = []
        accommodations_madrid = []
        accommodations_florence = []
        accommodations_granada = []
        accommodations_london = []
        accommodations_milan = []
        accommodations_prague = []
        accommodations_paris = []
        accommodations_rome = []
        accommodations_san_sebastian = []
        accommodations_valencia = []
        #
        # for accommodation in accommodations:
        #     city = accommodation.get('city')
        #     if city == 'madrid':
        #         accommodations_madrid.append(accommodation)
        #     elif city == 'new-york':
        #         accommodations_new_york.append(accommodation)
        #     elif city == 'barcelona':
        #         accommodations_barcelona.append(accommodation)
        #     elif city == 'florence':
        #         accommodations_florence.append(accommodation)
        #     elif city == 'granada':
        #         accommodations_granada.append(accommodation)
        #     elif city == 'london':
        #         accommodations_london.append(accommodation)
        #     elif city == 'milan':
        #         accommodations_milan.append(accommodation)
        #     elif city == 'prague':
        #         accommodations_prague.append(accommodation)
        #     elif city == 'paris':
        #         accommodations_paris.append(accommodation)
        #     elif city == 'rome':
        #         accommodations_rome.append(accommodation)
        #     elif city == 'san-sebastian':
        #         accommodations_san_sebastian.append(accommodation)
        #     elif city == 'valencia':
        #         accommodations_valencia.append(accommodation)

        dir = os.path.dirname(__file__)
        save_to_file(dir, accommodations, 'data_erasmusInn')


erasmusInnAccommodations()
