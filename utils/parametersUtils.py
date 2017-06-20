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
        return types.split('%2C')


def adaptCities(filters):
    cities = []
    # Setafoot, uniplaces, beroomers, ...

    # USA
    cities.append(['new-york', '', 'new-york-united-states'])
    cities.append(['boston', '', 'boston-ma-united-states'])

    # Italy
    cities.append(['rome', 'rome', 'rome-italy'])
    cities.append(['florence', 'florence', 'florence-italy'])
    cities.append(['bologna', 'bologna', 'bologna-italy'])
    cities.append(['milan', 'milan', 'milan-italy'])
    cities.append(['padua', 'padua', 'padova-italy'])
    cities.append(['turin', 'turin', 'turin-italy'])

    # United Kindgom
    cities.append(['london', 'london', 'london-united-kingdom'])
    cities.append(['manchester', 'manchester', ''])
    cities.append(['leeds', 'leeds', 'leeds-united-kingdom'])
    cities.append(['cardiff', 'cardiff', 'cardiff-united-kingdom'])

    # Portugal
    cities.append(['porto', 'porto', 'porto-portugal'])
    cities.append(['lisbon', 'lisbon', 'lisboa-portugal'])
    cities.append(['coimbra', 'coimbra', ''])

    # Spain
    cities.append(['madrid', 'madrid', 'madrid-spain'])
    cities.append(['barcelona', 'barcelona', 'barcelona-spain'])
    cities.append(['valencia', 'valencia', 'valencia-spain'])
    cities.append(['granada', 'granada', 'granada-spain'])
    cities.append(['seville', 'seville', 'seville-spain'])
    cities.append(['salamanca', 'salamanca', 'salamanca-spain'])
    cities.append(['palma-de-mallorca', 'palma-de-mallorca', ''])
    cities.append(['alicante', 'alicante', 'alicante-spain'])
    cities.append(['malaga', 'malaga', 'malaga-spain'])
    cities.append(['zaragoza', 'zaragoza', 'zaragoza-spain'])
    cities.append(['cordova', 'cordova', 'cordoba-spain'])
    cities.append(['murcia', 'murcia', 'murcia-spain'])
    cities.append(['cadiz', 'cadiz', 'cadiz-spain'])

    # France
    cities.append(['paris', 'paris', 'paris-france'])

    # Germany
    cities.append(['berlin', 'berlin', 'berlin-germany'])
    cities.append(['munich', 'munich', ''])

    cityString = filters.get('city', '')

    if cityString != '':
        for city in cities:
            if city[0] == cityString:
                return city

    return ['madrid', 'madrid', 'madrid-spain']
