import json
import os
from urllib.error import HTTPError
from urllib.request import urlopen
from downloadUtils import save_to_file

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


def studyAbroadAccommodations():
    firstLink = 'https://www.studyabroadapartments.com/api/apartments.json'
    apartment_count_html_code = get_html_code(firstLink)

    apartment_count_json_data = json.loads(apartment_count_html_code)
    apartment_count = apartment_count_json_data['apartment_count']

    number_of_pages = int((apartment_count - 1) / 48)
    print('There are %d pages.' % (number_of_pages))

    accommodations = []

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

    for i in range(number_of_pages + 1):
        paging_link = 'https://www.studyabroadapartments.com/api/apartments.json?q=%7B%22page%22:' + str(i) + '%7D'

        paging_html_code = get_html_code(paging_link)

        if paging_html_code == None:
            paging_html_code = '{"apartments":[]}'

        paging_json_data = json.loads(paging_html_code)

        # print(len(paging_json_data['apartments']))
        for accommodation in paging_json_data.get('apartments'):
            # city
            city = accommodation.get(city_string, 'noCity')

            # id
            id = accommodation.get(id_string, 0)
            id = 'SAA-' + str(id)

            # title
            title = accommodation.get('name', 'Accommodation')

            # price
            currency = accommodation.get('currency', 'EUR')
            price = accommodation.get('display_price', 500)
            price = str(price)
            if currency == 'EUR':
                price = price + '€'
            elif currency == 'GBP':
                price = price + '£'
            elif currency == 'USD':
                price = price + '$'

            # link
            link = accommodation.get('link_path', '/madrid/rooms/velazquez-7a-room-8')
            link = 'https://www.studyabroadapartments.com' + link
            link = link + '?referral=SetAFoot'

            # latitude and longitude
            latitude = accommodation.get(latitude_string, 40.40)
            longitude = accommodation.get(longitude_string, -3.68)

            latitude = str(latitude)
            longitude = str(longitude)

            if latitude == 'None':
                latitude = str(40.40)
            if longitude == 'None':
                longitude = str(-3.68)

            # typology
            typology = accommodation.get('apart_type', 'room')

            if typology == 'room':
                typology = 'Bedroom'
            elif typology == 'apartment':
                typology = 'Full Apartment'
            elif typology == 'student_hall':
                typology = 'Residence'
            elif typology == 'bed':
                typology = 'Shared Room'

            # picture
            picture = accommodation.get('image_public_ids')[0].get('secure_url',
                                                                   'https://res.cloudinary.com/saacloud/image/upload/v1489435941/Madrid/saa_provider_1106/Preciados_2D_Room_11/yqajde7ruqxdxavdwu19.jpg')

            # occupancies
            occupancies = accommodation.get(occupancies_string)
            new_occupancies = []
            for occupancy in occupancies:
                first_date = occupancy.get('to')
                second_date = occupancy.get('from')

                first_date_array = first_date.split('-')
                first_date = first_date_array[2] + '-' + first_date_array[1] + '-' + first_date_array[0]

                second_date_array = second_date.split('-')
                second_date = second_date_array[2] + '-' + second_date_array[1] + '-' + second_date_array[0]

                new_occupancy = {
                    'to': first_date,
                    'from': second_date
                }
                new_occupancies.append(new_occupancy)

            accommodations.append({
                city_string: city,
                id_string: id,
                title_string: title,
                price_string: price,
                link_string: link,
                latitude_string: latitude,
                longitude_string: longitude,
                provider_string: 'StudyAbroadAp',
                typology_string: typology,
                picture_string: picture,
                bills_string: 'all bills included',
                occupancies_string: new_occupancies
            })

        for accommodation in accommodations:
            city = accommodation.get('city')
            if city == 'madrid':
                accommodations_madrid.append(accommodation)
            elif city == 'new-york':
                accommodations_new_york.append(accommodation)
            elif city == 'barcelona':
                accommodations_barcelona.append(accommodation)
            elif city == 'florence':
                accommodations_florence.append(accommodation)
            elif city == 'granada':
                accommodations_granada.append(accommodation)
            elif city == 'london':
                accommodations_london.append(accommodation)
            elif city == 'milan':
                accommodations_milan.append(accommodation)
            elif city == 'prague':
                accommodations_prague.append(accommodation)
            elif city == 'paris':
                accommodations_paris.append(accommodation)
            elif city == 'rome':
                accommodations_rome.append(accommodation)
            elif city == 'san-sebastian':
                accommodations_san_sebastian.append(accommodation)
            elif city == 'valencia':
                accommodations_valencia.append(accommodation)

    dir = os.path.dirname(__file__)

    save_to_file(dir, accommodations, 'data_studyabroadapartments')
    save_to_file(dir, accommodations, 'accommodations_saa_madrid')
    save_to_file(dir, accommodations, 'accommodations_saa_new_york')
    save_to_file(dir, accommodations, 'accommodations_saa_barcelona')
    save_to_file(dir, accommodations, 'accommodations_saa_florence')
    save_to_file(dir, accommodations, 'accommodations_saa_granada')
    save_to_file(dir, accommodations, 'accommodations_saa_london')
    save_to_file(dir, accommodations, 'accommodations_saa_milan')
    save_to_file(dir, accommodations, 'accommodations_saa_prague')
    save_to_file(dir, accommodations, 'accommodations_saa_paris')
    save_to_file(dir, accommodations, 'accommodations_saa_rome')
    save_to_file(dir, accommodations, 'accommodations_saa_san_sebastian')
    save_to_file(dir, accommodations, 'accommodations_saa_valencia')


studyAbroadAccommodations()
