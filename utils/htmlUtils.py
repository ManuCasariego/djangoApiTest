from urllib.error import HTTPError
from urllib.request import urlopen


def getHTMLCode(link, offlineFile='', usingMock=False):
    if usingMock:
        file = open('/home/manu/PycharmProjects/scrappingAccommodations/data/' + offlineFile, 'r')
        html = file.read()
        file.close()
        return html

    # Optional: Check url well formed
    try:

        fp = urlopen(link)
    except HTTPError as e:
        print(e)
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


