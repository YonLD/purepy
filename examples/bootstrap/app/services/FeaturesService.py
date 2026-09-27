from ..dao.FeaturesDao import content as dao_content

TITLES = {
    'columns': 'Columns with icons',
    'hanging': 'Hanging icons',
    'cards': 'Custom cards',
    'grid': 'Icon grid',
}


def page_title():
    return 'Features · Bootstrap v5.2'


def section(key):
    if key not in TITLES:
        raise RuntimeError(
            "unknown features section '{}'; known sections: {}.".format(key, ', '.join(TITLES.keys()))
        )

    items = dao_content()[key]

    return {'title': TITLES[key], 'items': items}


def feature_section():
    features = dao_content()['features']

    return {
        'title': 'Features with title',
        'main': {
            'title': 'Left-aligned title explaining these awesome features',
            'content': "Paragraph of text beneath the heading to explain the heading. We'll add onto it with another sentence and probably just keep going until we run out of words.",
            'link': '#',
            'linkText': 'Primary button',
        },
        'features': features,
    }
