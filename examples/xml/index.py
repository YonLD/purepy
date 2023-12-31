from typing import Dict
from pure.core.XML import XML

data = [
    {
        'street': '100 Main',
        'city'  : 'Framingham',
        'state' : 'MA',
        'zip'   : '01701'
    },
    {
        'street': '720 Prospect',
        'city'  : 'Framingham',
        'state' : 'MA',
        'zip'   : '01701'
    },
    {
        'street': '120 Ridge',
        'state' : 'MA',
        'zip'   : '01760'
    }
]

def address(*args):
    tag = XML('address')
    return tag(*args)

def street(*args):
    tag = XML('street')
    return tag(*args)

def city(*args):
    tag = XML('city')
    return tag(*args)

def state(*args):
    tag = XML('state')
    return tag(*args)

def zip(*args):
    tag = XML('zip')
    return tag(*args)

def customers(*args):
    tag = XML('customers')
    return tag(*args)

def customer(*args):
    tag = XML('customer')
    return tag(*args)

def name(*args):
    tag = XML('name')
    return tag(*args)

def Address(props: Dict[str, str]):
    street_val = props.get('street')
    city_val = props.get('city')
    state_val = props.get('state')
    zip_code = props.get('zip')

    return address(
        street(street_val) if (street_val) else None,
        city(city_val) if (city_val) else None,
        state(state_val) if (state_val) else None,
        zip(zip_code) if (zip_code) else None
    )

def Xml():
    return (
        customers(
            customer(
                name('Charter Group'),
                list(map(Address, data))
            ).id('55000')
        )
    )

Xml().to_save('./output.xml')
