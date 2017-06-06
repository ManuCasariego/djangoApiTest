def addParamatersToLink(link, parameters):
    if len(parameters) > 0:
        if '?' not in link:
            link += '?'
        for key, value in parameters.items():
            if link[-1] != '?':
                link += '&'
            if type(value) is str:
                link += key + '=' + value
            elif type(value) is list:
                firstItemPassed = False
                for value_aux in value:
                    if firstItemPassed:
                        link += '&'
                    else:
                        firstItemPassed = True
                    link += key + '=' + value_aux
    return link
