from .Tag import Tag

SELF_CLOSE_HTML_TAGS = [
    'area',
    'base',
    'br',
    'col',
    'embed',
    'hr',
    'img',
    'input',
    'link',
    'meta',
    'source',
    'track',
    'wbr'
]

class HTML(Tag):
    def __init__(self, tag_name: str):
        super().__init__(tag_name)
        if tag_name.lower() in SELF_CLOSE_HTML_TAGS:
            self.set_self_close(True)

    def to_save(self, path: str, header = '<!DOCTYPE html>'):
        with open(path, 'w') as file:
            file.write(header + str(self.to_PDom()))
