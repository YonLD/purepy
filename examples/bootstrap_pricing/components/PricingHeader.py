from pure.html import div, h1, p

def PricingHeader(title: str, desc: str):
    return div(
        h1(title).class_name('display-4'),
        p(desc).class_name('lead')
    ).class_name('pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center');
