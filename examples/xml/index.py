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
    return XML('address', args)

def street(*args):
    return XML('street', args)

def city(*args):
    return XML('city', args)

def state(*args):
    return XML('state', args)

def zip(*args):
    return XML('zip', args)

def customers(*args):
    return XML('customers', args)

def customer(*args):
    return XML('customer', args)

def name(*args):
    return XML('name', args)

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
