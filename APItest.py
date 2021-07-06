import unittest
from spotifyplaylistanalysis.py import setup


class APItest(unittest.TestCase):
    good_col_names = ['a', 'b', 'c']
    bad_col_names = []
    good_artist_id = '7d64ZVOXg02y73HB5UMqkb?si=Go8-TWgrS8CvSCkchJoMlg&dl_branch=1'
    bad_string = 'xxx'
    CLIENT_ID = '45505ed8cb474aebb71af15ea0eea7b2'
    CLIENT_SECRET = 'b178b1670a9c4376b1b652d95a9d4247'
    def test_set_up_empty(self):
        try:
            sp = set_up('', '')
        except:
            self.assertEqual(0 == 0)


    def test_set_up_happy(self):
        auth_data = setup(CLIENT_SECRET, CLIENT_ID)
        self.assertEqual(type(sp), '<class \'spotipy.client.Spotify\'>')


    if __name__ == '__main__':
        unittest.main()