def add_paramaters_to_link(link, parameters):
    if len(parameters) > 0:
        if '?' not in link:
            link += '?'
        for key, value in parameters.items():
            if link[-1] != '?':
                link += '&'
            if type(value) is str:
                link += key + '=' + value
            elif type(value) is list:
                first_item_passed = False
                for value_aux in value:
                    if first_item_passed:
                        link += '&'
                    else:
                        first_item_passed = True
                    link += key + '=' + value_aux
    return link


def get_types_array(types):
    if types == '':
        return []
    else:
        return types.split(',')


def adaptCities(filters):
    cities = []
    # Setafoot, uniplaces, beroomers, studyAbroadApartments, erasmusinn ...

    # USA
    cities.append(['new-york', '', 'new-york-united-states', 'new-york', '', 'new-york'])
    cities.append(['boston', '', 'boston-ma-united-states', '', '', 'boston'])

    # Italy
    cities.append(['rome', 'rome', 'rome-italy', 'rome', 'rome', 'rome'])
    cities.append(['florence', 'florence', 'florence-italy', 'florence', 'florence', 'florence'])
    cities.append(['bologna', 'bologna', 'bologna-italy', '', '', 'bologna'])
    cities.append(['milan', 'milan', 'milan-italy', 'milan', 'milan', 'milan'])
    cities.append(['padua', 'padua', 'padova-italy', '', '', 'padua'])
    cities.append(['turin', 'turin', 'turin-italy', '', '', 'turin'])

    # United Kindgom
    cities.append(['london', 'london', 'london-united-kingdom', 'london', 'london', 'london'])
    cities.append(['manchester', 'manchester', '', '', '', ''])
    cities.append(['leeds', 'leeds', 'leeds-united-kingdom', '', '', 'leeds'])
    cities.append(['cardiff', 'cardiff', 'cardiff-united-kingdom', '', '', 'cardiff'])

    # Portugal
    cities.append(['porto', 'porto', 'porto-portugal', '', '', 'porto'])
    cities.append(['lisbon', 'lisbon', 'lisboa-portugal', '', '', 'lisbon'])
    cities.append(['coimbra', 'coimbra', '', '', '', ''])

    # Spain
    cities.append(['madrid', 'madrid', 'madrid-spain', 'madrid', 'madrid', 'madrid'])
    cities.append(['barcelona', 'barcelona', 'barcelona-spain', 'barcelona', 'barcelona', 'barcelona'])
    cities.append(['valencia', 'valencia', 'valencia-spain', 'valencia', '', 'valencia'])
    cities.append(['granada', 'granada', 'granada-spain', 'granada', 'granada', 'granada'])
    cities.append(['seville', 'seville', 'seville-spain', '', '', 'seville'])
    cities.append(['salamanca', 'salamanca', 'salamanca-spain', '', '', 'salamanca'])
    cities.append(['palma-de-mallorca', 'palma-de-mallorca', '', '', '', ''])
    cities.append(['alicante', 'alicante', 'alicante-spain', '', '', 'alicante'])
    cities.append(['malaga', 'malaga', 'malaga-spain', '', '', 'malaga'])
    cities.append(['zaragoza', 'zaragoza', 'zaragoza-spain', '', 'zaragoza', 'zaragoza'])
    cities.append(['cordova', 'cordova', 'cordoba-spain', '', '', 'cordova'])
    cities.append(['murcia', 'murcia', 'murcia-spain', '', '', 'murcia'])
    cities.append(['cadiz', 'cadiz', 'cadiz-spain', '', '', 'cadiz'])
    cities.append(['san-sebastian', '', '', 'san-sebastian', '', ''])

    # France
    cities.append(['paris', 'paris', 'paris-france', 'paris', '', 'paris'])

    # Germany
    cities.append(['berlin', 'berlin', 'berlin-germany', '', 'berlin', 'berlin'])
    cities.append(['munich', 'munich', '', '', '', ''])

    # Poland
    cities.append(['warsaw', '', '', '', 'warsaw', ''])
    cities.append(['poznan', '', '', '', 'poznan', ''])
    cities.append(['lodz', '', '', '', 'lodz', ''])

    # Turkey
    cities.append(['istanbul', '', '', '', 'istanbul', ''])

    # Check Republic
    cities.append(['prague', '', '', 'prague', '', ''])

    city_string = filters.get('city', '')

    if city_string != '':
        for city in cities:
            if city[0] == city_string:
                return city

    return ['madrid', 'madrid', 'madrid-spain', 'madrid', 'madrid', 'madrid']
