from utils.scrapGlobal import getJsonAccommodations


def get_accommodations(filters={}):
    # response_data = {}
    # response_data['title'] = 'Title 1'
    # response_data['price'] = '1234'
    # response_data['link'] = 'www.google.es'
    # response_data['type'] = ['bed', 'bed2']
    # response_data = merge_2_dictionaries(response_data, filters)
    # response_data['extra'] = filters.get('manu2', '')

    response_data = getJsonAccommodations(filters)
    return response_data


def merge_2_dictionaries(dictionary1, dictionary2):
    z = dictionary1.copy()
    z.update(dictionary2)
    return z
