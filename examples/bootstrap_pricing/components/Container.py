from pure.html import div

def Container(*children):
    return div(*children).class_name('container');
