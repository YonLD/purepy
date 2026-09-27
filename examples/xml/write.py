import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.controllers.IndexController import index_controller

output = index_controller()

file = os.path.join(os.path.dirname(__file__), 'example.xml')
with open(file, 'w') as f:
    f.write(output)

print('wrote: {}'.format(file))
print('{} bytes'.format(len(output)))
