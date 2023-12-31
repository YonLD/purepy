from pure.html import html, head, meta, link, title, body
from .App import App

# saved from url=(0051)https://getbootstrap.com/docs/4.0/examples/pricing/

def BootstrapPricing():
    return (
        html(
            head(
                meta().http_equiv('Content-Type').content('text/html; charset=UTF-8'),
                meta().name('viewport').content('width=device-width, initial-scale=1, shrink-to-fit=no'),
                meta().name('description').content(''),
                meta().name('author').content(''),
                link().rel('icon').href('https://getbootstrap.com/docs/4.0/assets/img/favicons/favicon.ico'),
                title('Pricing example for Bootstrap'),
                link().rel('canonical').href('https://getbootstrap.com/docs/4.0/examples/pricing/'),
                link().href('https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css').rel('stylesheet'),
                link().href('./bootstrap_pricing/pricing.css').rel('stylesheet'),
            ),
            body(
                App()
            )
        ).lang('en')
    )



