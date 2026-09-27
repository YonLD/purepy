from pure.compile.Compile import Compile
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.core.XML import XML
from pure.utils import renderXML


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


def AddressShape():
    return Compile.shape(
        address(
            street(Slot.value('street')),
            Slot.if_('city', city(Slot.value('city'))),
            state(Slot.value('state')),
            zip(Slot.value('zip'))
        )
    )


def XmlPageShape():
    return Compile.shape(
        customers(
            customer(
                name('Charter Group'),
                Slot.each('addresses', AddressShape())
            ).id('55000')
        )
    )


def Xml(*children):
    return component('Xml', *children)


register(Xml, lambda: XmlPageShape())


def xml_page(data):
    return renderXML(component('Xml').addresses(data['addresses']))
