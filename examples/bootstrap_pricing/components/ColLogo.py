from pure.html import div, small, img

def ColLogo(image: str, text: str):
    return div(
        img().class_name('mb-2').src(image['src']).width(image['width']).height(image['height']),
        small(text).class_name('d-block mb-3 text-muted')
    ).class_name('col-12 col-md');
