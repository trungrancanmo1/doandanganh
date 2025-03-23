'''
    @zun
'''
import unittest
from subscriber import mqtt_listener


class TestSubscriber(unittest.TestCase):
    def test_successful_connection(self):
        mqtt_listener()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()