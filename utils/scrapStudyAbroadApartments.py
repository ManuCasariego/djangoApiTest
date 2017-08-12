import json
import os


def is_date1_bigger_or_equal_than_date2(day1, month1, year1, day2, month2, year2):
    return year1 > year2 or year1 == year2 and month1 > month2 or year1 == year2 and month1 == month2 and day1 >= day2


def studyAbroadApartmentsAccommodations(filters=None):
    if filters is None:
        filters = {}
    city = filters.get('city', 'madrid')
    checkin = filters.get('checkin', '')
    checkout = filters.get('checkout', '')
    minPrice = filters.get('minPrice', '')
    maxPrice = filters.get('maxPrice', '')
    type_aux = filters.get('type', [])

    type = list(type_aux)

    top_right_lat = filters.get('topRightLat', '')
    top_right_lng = filters.get('topRightLng', '')
    bottom_left_lat = filters.get('bottomLeftLat', '')
    bottom_left_lng = filters.get('bottomLeftLng', '')

    dir = os.path.dirname(__file__)
    route = '../data/accommodations_saa_' + city.replace('-', '_') + '.json'
    filename = os.path.join(dir, route)

    if not os.path.isfile(filename):
        print('File doesn\'t exist')
        return []

    file = open(filename, 'r')
    file_string = file.read()
    file.close()

    accommodations = json.loads(file_string)

    accommodations_to_return = []
    for accommodation in accommodations:

        id = accommodation.get('id')
        bills = accommodation.get('bills')
        longitude = accommodation.get('longitude')
        latitude = accommodation.get('latitude')
        picture = accommodation.get('picture')
        city = accommodation.get('city')
        link = accommodation.get('link')
        price = accommodation.get('price')
        title = accommodation.get('title')
        occupancies = accommodation.get('occupancies')
        provider = accommodation.get('provider')
        typology = accommodation.get('typology')

        every_filter_is_passed = True

        # Price

        price = int(price.replace('€', '').replace('$', '').replace('£', ''))

        if minPrice != '' and every_filter_is_passed:
            minPrice = int(minPrice)
            if minPrice <= price:
                pass
            else:
                every_filter_is_passed = False

        if maxPrice != '' and every_filter_is_passed:
            maxPrice = int(maxPrice)
            if price <= maxPrice:
                pass
            else:
                every_filter_is_passed = False

        # Geographic Coordinates
        latitude = float(latitude)
        longitude = float(longitude)

        if bottom_left_lat != '' and every_filter_is_passed:

            bottom_left_lat = float(bottom_left_lat)
            bottom_left_lng = float(bottom_left_lng)
            top_right_lat = float(top_right_lat)
            top_right_lng = float(top_right_lng)

            if bottom_left_lat < latitude < top_right_lat:
                if bottom_left_lng < longitude < top_right_lng:
                    pass
                else:
                    every_filter_is_passed = False
            else:
                every_filter_is_passed = False

        # Type

        if type and every_filter_is_passed:
            ha_pasado = False
            for t in type:
                if t == 'full-apartment' and typology == 'Full Apartment' \
                        or t == 'room' and typology == 'Bedroom' \
                        or t == 'residence' and typology == 'Residence' \
                        or t == 'shared-room' and typology == 'Shared Room':
                    ha_pasado = True
            if not ha_pasado:
                every_filter_is_passed = False

        # Dates

        if checkin != '':
            checkin_array = checkin.split('-')
            day_checkin = int(checkin_array[0])
            month_checkin = int(checkin_array[1])
            year_checkin = int(checkin_array[2])

        if checkout != '':
            checkout_array = checkout.split('-')
            day_checkout = int(checkout_array[0])
            month_checkout = int(checkout_array[1])
            year_checkout = int(checkout_array[2])

        if (checkin != '' or checkout != '') and every_filter_is_passed:

            for occupancy in occupancies:
                occupancy_from = occupancy.get('from')
                occupancy_from_array = occupancy_from.split('-')
                day_occupancy_from = int(occupancy_from_array[0])
                month_occupancy_from = int(occupancy_from_array[1])
                year_occupancy_from = int(occupancy_from_array[2])

                occupancy_to = occupancy.get('to')
                occupancy_to_array = occupancy_to.split('-')
                day_occupancy_to = int(occupancy_to_array[0])
                month_occupancy_to = int(occupancy_to_array[1])
                year_occupancy_to = int(occupancy_to_array[2])

                # comprobar que el checkindate > to o que el checkoutdate < from
                # entonces sigue

                if checkin != '' and every_filter_is_passed:
                    if not is_date1_bigger_or_equal_than_date2(
                            day_checkin, month_checkin, year_checkin,
                            day_occupancy_to, month_occupancy_to, year_occupancy_to):
                        every_filter_is_passed = False

                if checkout != '' and every_filter_is_passed:
                    if not is_date1_bigger_or_equal_than_date2(
                            day_occupancy_from, month_occupancy_from, year_occupancy_from,
                            day_checkout, month_checkout, year_checkout):
                        every_filter_is_passed = False
        # final resolution
        if every_filter_is_passed:
            accommodations_to_return.append(accommodation)

    accommodations_to_return = accommodations_to_return[0:201]
    return accommodations_to_return

#
# respuesta = read_accommodation_json_file({
#     "city": 'madrid',
#     'maxPrice': '2000',
#     'minPrice': '300',
#     'type': ['room', 'full-apartment'],
#     'checkin': '22-09-22982'
#
# })
# #
# # i = 1
# # for respuest in respuesta:
# #     print(str(i), respuest.get('typology'))
# #     i += 1
#
# print('hay ', len(respuesta), ' resultados')
