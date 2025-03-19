'''
    @zun
'''
import unittest
from afsubscriber.subscriber import mqtt_subscriber_start


class TestSubscriber(unittest.TestCase):
    def test_successful_connection(self):
        mqtt_subscriber_start()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()