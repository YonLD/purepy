from .Tag import Tag

class XML(Tag):
    def to_save(self, path: str, header = '<?xml version="1.0"?>'):
        with open(path, 'w') as file:
            file.write(header + str(self.to_PDom()))
