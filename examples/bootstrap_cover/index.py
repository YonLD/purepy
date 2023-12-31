from pure.html import html, head, meta, title, link, body, div, header, h3, nav, main, p, h1, footer, a

def BootstrapCover():
    return html(
        head(
            meta().charset('utf-8'),
            meta().name('viewport').content('width=device-width, initial-scale=1'),
            meta().name('description').content('tiny demo'),
            meta().name('author').content('Mark Otto, Jacob Thornton, and Bootstrap contributors'),
            meta().name('generator').content('Hugo 0.108.0'),
            title('Cover Template · Bootstrap v5.3'),
            link().rel('canonical').href('https://getbootstrap.com/docs/5.3/examples/cover/'),
            link().href('https://getbootstrap.com/docs/5.3/dist/css/bootstrap.min.css').rel('stylesheet').crossorigin('anonymous'),
            link().rel('apple-touch-icon').href('https://getbootstrap.com/docs/5.3/assets/img/favicons/apple-touch-icon.png').sizes('180x180'),
            link().rel('icon').href('https://getbootstrap.com/docs/5.3/assets/img/favicons/favicon-32x32.png').sizes('32x32').type('image/png'),
            link().rel('icon').href('https://getbootstrap.com/docs/5.3/assets/img/favicons/favicon-16x16.png').sizes('16x16').type('image/png'),
            link().rel('manifest').href('https://getbootstrap.com/docs/5.3/assets/img/favicons/manifest.json'),
            link().rel('mask-icon').href('https://getbootstrap.com/docs/5.3/assets/img/favicons/safari-pinned-tab.svg').color('#712cf9'),
            link().rel('icon').href('https://getbootstrap.com/docs/5.3/assets/img/favicons/favicon.ico'),
            meta().name('theme-color').content('#712cf9'),
            link().href('https://getbootstrap.com/docs/5.3/examples/cover/cover.css').rel('stylesheet')
        ),
        body(
            div(
                header(
                    div(
                        h3('Cover').class_name('float-md-start mb-0'),
                        nav(
                            a('Home').class_name('nav-link fw-bold py-1 px-0 active').aria_current('page').href('#'),
                            a('Features').class_name('nav-link fw-bold py-1 px-0').href('#'),
                            a('Contact').class_name('nav-link fw-bold py-1 px-0').href('#')
                        ).class_name('nav nav-masthead justify-content-center float-md-end')
                    )
                ).class_name('mb-auto'),
                main(
                    h1('Cover your page.'),
                    p('Cover is a one-page template for building simple and beautiful home pages. Download, edit the text, and add your own fullscreen background photo to make it your own.').class_name('lead'),
                    p(
                        a('Learn more').class_name('btn btn-lg btn-light fw-bold border-white bg-white').href('#')
                    ).class_name('lead')
                ).class_name('px-3'),
                footer(
                    p(
                        'Cover template for',
                        a('Bootstrap').class_name('text-white').href('https://getbootstrap.com/'),
                        ', by',
                        a('@mdo').class_name('text-white').href('https://twitter.com/mdo'),
                        '.'
                    )
                ).class_name('mt-auto text-white-50')
            ).class_name('cover-container d-flex w-100 h-100 p-3 mx-auto flex-column')
        ).class_name('d-flex h-100 text-center text-bg-dark')
    ).lang('en').class_name('h-100')
