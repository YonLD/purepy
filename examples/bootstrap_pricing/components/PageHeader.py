from pure.html import div, h5, nav, a

def PageHeader(company_name: str, navs: list, sign_up: str):
    return div(
        h5(company_name).class_name('my-0 mr-md-auto font-weight-normal'),
        nav(
            list(map(lambda nav: a(nav['text']).class_name('p-2 text-dark').href(nav['href']), navs)),
        ).class_name('my-2 my-md-0 mr-md-3'),
        a(sign_up['text']).class_name('btn btn-outline-primary').href(sign_up['href'])
    ).class_name('d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow');
