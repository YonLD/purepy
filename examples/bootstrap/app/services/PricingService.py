from ..dao.PricingDao import content as dao_content

COMPANY = 'Company name'


def header():
    header = dao_content()['header']

    return {
        'company': COMPANY,
        'navs': header['navs'],
        'signUp': header['signUp'],
    }


def pricing():
    return dao_content()['pricing']


def deck():
    return dao_content()['deck']['cards']


def footer():
    footer = dao_content()['footer']

    return {
        'logo': footer['logo'],
        'columns': footer['links'],
    }
