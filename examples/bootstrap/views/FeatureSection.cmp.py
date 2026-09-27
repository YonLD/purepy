import os
from pure.component.Call import Call
from pure.component.functions import component, register
from pure.core.Slot import Slot
from pure.html import div, h2

from pure.loader import load_module
MainFeature = load_module(os.path.join(os.path.dirname(__file__), '../components/MainFeature.cmp.py'), 'MainFeature').MainFeature
from pure.loader import load_module
FeatureTitle = load_module(os.path.join(os.path.dirname(__file__), '../components/FeatureTitle.cmp.py'), 'FeatureTitle').FeatureTitle
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..')))
from app.services import FeaturesService


def FeatureSection(*children):
    return component('FeatureSection', *children)


register(FeatureSection,
    factory=lambda: (
        div(
            h2(Slot.value('title')).class_name('pb-2 border-bottom'),
            div(
                Slot.raw('main'),
                div(
                    div(Slot.raw('features')).class_name('row row-cols-1 row-cols-sm-2 g-4')
                ).class_name('col')
            ).class_name('row row-cols-1 row-cols-md-2 align-items-md-center g-5 py-5')
        ).class_name('container px-4 py-5')
    ),
    prepare=lambda: {
        'title': FeaturesService.feature_section()['title'],
        'main': MainFeature().props(FeaturesService.feature_section()['main']),
        'features': [FeatureTitle().props(feature) for feature in FeaturesService.feature_section()['features']],
    }
)
