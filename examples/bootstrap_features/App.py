from pure.html import main, h1, div
from .components.Section import Section
from .components.Divider import Divider
from .components.IconColumn import IconColumn
from .components.HangingIcon import HangingIcon
from .components.CustomCard import CustomCard
from .components.MainFeature import MainFeature
from .components.CellIcon import CellIcon
from .components.FeatureTitle import FeatureTitle
from .data import columnsData, hangingData, cardsData, gridData, featuresData

def App():
    return (
        main(
            h1('Features examples').class_name('visually-hidden'),
            Section(
                title = 'Columns with icons',
                contents = list(map(IconColumn, columnsData)),
                classList = 'row g-4 py-5 row-cols-1 row-cols-lg-3'
            ),
            Divider(),
            Section(
                title = 'Hanging icons',
                contents = list(map(HangingIcon, hangingData)),
                classList = 'row g-4 py-5 row-cols-1 row-cols-lg-3'
            ),
            Divider(),
            Section(
                title = 'Custom cards',
                contents = list(map(CustomCard, cardsData)),
                classList = 'row row-cols-1 row-cols-lg-3 align-items-stretch g-4 py-5'
            ),
            Divider(),
            Section(
                title = 'Icon grid',
                contents = list(map(CellIcon, gridData)),
                classList = 'row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5'
            ),
            Divider(),
            Section(
                title = 'Features with title',
                contents = [
                    MainFeature(
                        title = 'Left-aligned title explaining these awesome features',
                        content = "Paragraph of text beneath the heading to explain the heading. We'll add onto it with another sentence and probably just keep going until we run out of words.",
                        link = '#',
                        linkText = 'Primary button'
                    ),
                    div(
                        div(
                            list(map(FeatureTitle, featuresData))
                        ).class_name('row row-cols-1 row-cols-sm-2 g-4')
                    ).class_name('col')
                ],
                classList = 'row row-cols-1 row-cols-md-2 align-items-md-center g-5 py-5'
            ),
        )
    )
