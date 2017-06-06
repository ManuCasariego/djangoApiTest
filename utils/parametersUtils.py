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
