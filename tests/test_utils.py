import unittest
from pure.clx import clx
from pure.sty import sty

class UtilsTest(unittest.TestCase):

    def test_clx(self):
        self.assertEqual('class-a class-b class-c class-d', clx(
            'class-a',
            'class-b',
            {
                'class-c': True,
                'class-d': True,
                'class-e': False
            }
        ))

        self.assertEqual('class-a class-b class-c', clx(
            None,
            '',
            [
                'class-a',
                'class-b'
            ],
            {
                'class-c': True,
            }
        ))

    def test_sty(self):
        self.assertEqual('background-color: red; height: 36px; border: 1px solid #fff;', sty({
            'background-color': 'red',
            'height': '36px',
            'border': '1px solid #fff'
        }))

if __name__ == '__main__':
    unittest.main()
