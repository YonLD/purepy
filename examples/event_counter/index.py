from pure.html import html, head, body, meta, title, link, script
from .App import App

def EventCounter():
    return (
        html(
            head(
                meta().charset('UTF-8'),
                meta().http_equiv('X-UA-Compatible').content('IE=edge'),
                meta().name('viewport').content('width=device-width, initial-scale=1.0'),
                title('Event example'),
                link().rel('stylesheet').href('./event_counter/style.css'),
            ),
            body(
                App(),
                script().src('./event_counter/script.js'),
            )
        ).lang('en')
    )
