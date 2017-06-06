
'''

    if checkin != '' or checkout != '' or minPrice != '' or maxPrice != '':
        link += '?'

    if city != '':
        link = link.replace('madrid', city)

    if checkin != '':
        if link[-1] != '?':
            link += '&'
        # Convert date format
        checkin = datetime.datetime.strptime(checkin, '%d-%m-%Y').strftime('%Y-%m-%d')
        link += 'move-in=' + checkin

    if checkout != '':
        if link[-1] != '?':
            link += '&'
        # Convert date format
        checkout = datetime.datetime.strptime(checkout, '%d-%m-%Y').strftime('%Y-%m-%d')
        link += 'move-out=' + checkout

    if minPrice != '' or maxPrice != '':
        if link[-1] != '?':
            link += '&'
        if minPrice == '':
            minPrice = '100'
        if maxPrice == '':
            maxPrice = '1500'
        link += 'budget=' + minPrice + '-' + maxPrice

    return link
'''



'''
        ###############################################################
        # TODO: Implement date on the link pre track
        checkin = filters.get('checkin', '')
        checkout = filters.get('checkout', '')
        if checkin != '' or checkout != '':
            links_string[i] += '?'
            if links_string[i][-1] != '?':
                links_string[i] += '&'
            if checkin != '':
                # Convert date format
                checkin = datetime.datetime.strptime(checkin, '%d-%m-%Y').strftime('%Y-%m-%d')
                links_string[i] += 'move-in=' + checkin
            if links_string[i][-1] != '?':
                links_string[i] += '&'
            if checkout != '':
                # Convert date format
                checkout = datetime.datetime.strptime(checkout, '%d-%m-%Y').strftime('%Y-%m-%d')
                links_string[i] += 'move-out=' + checkout

        #######################################################
        '''