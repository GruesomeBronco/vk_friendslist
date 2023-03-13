import unittest
import os
from unittest.mock import patch
from io import StringIO
from get_vk_friends import main


class TestVKFriends(unittest.TestCase):
    
    def test_no_friends(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['vk_friends.py', 'https://vk.com/1'])
            self.assertEqual(fake_out.getvalue(), "No friends found for user ID 1\n")
    
    def test_max_friends(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(['vk_friends.py', 'https://vk.com/id655729556'])
            self.assertGreater(len(fake_out.getvalue()), 0)
    
    def test_wrong_username(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(ValueError):
                main(['vk_friends.py', 'https://vk.com/ifvirngofvk'])
    
    def test_http_error(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('vk_friends.requests.get') as mock_get:
                mock_get.side_effect = Exception('An error occurred')
                with self.assertRaises(Exception):
                    main(['vk_friends.py', 'https://vk.com/id123456'])
