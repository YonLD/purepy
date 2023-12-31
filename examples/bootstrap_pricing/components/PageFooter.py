from pure.html import footer, div

def PageFooter(*children):
    return footer(
        div(
            *children
        ).class_name('row'),
    ).class_name('pt-4 my-md-5 pt-md-5 border-top');
