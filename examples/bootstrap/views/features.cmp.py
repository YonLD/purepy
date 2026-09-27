import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Raw import Raw
from pure.core.Slot import Slot
from pure.html import body, h1, head, html, link, main, meta, title
from pure.utils import renderHTML

from pure.loader import load_module
IconSheet = load_module(os.path.join(os.path.dirname(__file__), '../components/IconSheet.cmp.py'), 'IconSheet').IconSheet
from pure.loader import load_module
IconColumn = load_module(os.path.join(os.path.dirname(__file__), '../components/IconColumn.cmp.py'), 'IconColumn').IconColumn
from pure.loader import load_module
HangingIcon = load_module(os.path.join(os.path.dirname(__file__), '../components/HangingIcon.cmp.py'), 'HangingIcon').HangingIcon
from pure.loader import load_module
CustomCard = load_module(os.path.join(os.path.dirname(__file__), '../components/CustomCard.cmp.py'), 'CustomCard').CustomCard
from pure.loader import load_module
CellIcon = load_module(os.path.join(os.path.dirname(__file__), '../components/CellIcon.cmp.py'), 'CellIcon').CellIcon
from pure.loader import load_module
MainFeature = load_module(os.path.join(os.path.dirname(__file__), '../components/MainFeature.cmp.py'), 'MainFeature').MainFeature
from pure.loader import load_module
FeatureTitle = load_module(os.path.join(os.path.dirname(__file__), '../components/FeatureTitle.cmp.py'), 'FeatureTitle').FeatureTitle
from pure.loader import load_module
Divider = load_module(os.path.join(os.path.dirname(__file__), '../components/Divider.cmp.py'), 'Divider').Divider
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import FeaturesService
from pure.loader import load_module
Section = load_module(os.path.join(os.path.dirname(__file__), 'Section.cmp.py'), 'Section').Section
from pure.loader import load_module
FeatureSection = load_module(os.path.join(os.path.dirname(__file__), 'FeatureSection.cmp.py'), 'FeatureSection').FeatureSection


def Features(*children):
    return component('Features', *children)


register(Features, factory=lambda: (
    html(
        head(
            meta().charset('utf-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1'),
            meta().name('description').content('pure demo'),
            meta().name('author').content('Mark Otto, Jacob Thornton, and Bootstrap contributors'),
            meta().name('generator').content('Hugo 0.104.2'),
            meta().name('theme-color').content('#712cf9'),
            title(Slot.value('title')),
            link().rel('canonical').href('https://getbootstrap.com/docs/5.2/examples/features/'),
            link().rel('stylesheet').crossorigin('anonymous').href('https://getbootstrap.com/docs/5.2/dist/css/bootstrap.min.css').integrity('sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65'),
            link().rel('apple-touch-icon').sizes('180x180').href('https://getbootstrap.com/docs/5.2/assets/img/favicons/apple-touch-icon.png'),
            link().rel('icon').type('image/png').sizes('32x32').href('https://getbootstrap.com/docs/5.2/assets/img/favicons/favicon-32x32.png'),
            link().rel('icon').type('image/png').sizes('16x16').href('https://getbootstrap.com/docs/5.2/assets/img/favicons/favicon-16x16.png'),
            link().rel('manifest').href('https://getbootstrap.com/docs/5.2/assets/img/favicons/manifest.json'),
            link().rel('mask-icon').color('#712cf9').href('https://getbootstrap.com/docs/5.2/assets/img/favicons/safari-pinned-tab.svg'),
            link().rel('icon').href('https://getbootstrap.com/docs/5.2/assets/img/favicons/favicon.ico'),
            link().rel('stylesheet').href('https://getbootstrap.com/docs/5.2/examples/features/features.css'),
            link().rel('stylesheet').href('./style.css')
        ),
        body(
            Raw.of(str(IconSheet())),
            main(
                h1('Features examples').class_name('visually-hidden'),
                Slot.raw('columns'),
                Raw.of(str(Divider())),
                Slot.raw('hanging'),
                Raw.of(str(Divider())),
                Slot.raw('cards'),
                Raw.of(str(Divider())),
                Slot.raw('grid'),
                Raw.of(str(Divider())),
                Slot.raw('features')
            )
        )
    )
), prepare=lambda: features_bindings())


def features_bindings():
    return {
        'title': FeaturesService.page_title(),
        'columns': Section()
            .section('columns')
            .class_name('row g-4 py-5 row-cols-1 row-cols-lg-3')
            .item(lambda record: IconColumn().props(record)),
        'hanging': Section()
            .section('hanging')
            .class_name('row g-4 py-5 row-cols-1 row-cols-lg-3')
            .item(lambda record: HangingIcon().props(record)),
        'cards': Section()
            .section('cards')
            .class_name('row row-cols-1 row-cols-lg-3 align-items-stretch g-4 py-5')
            .item(lambda record: CustomCard().props(record)),
        'grid': Section()
            .section('grid')
            .class_name('row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5')
            .item(lambda record: CellIcon().props(record)),
        'features': FeatureSection(),
    }


def features_page():
    return renderHTML(component('Features'))
