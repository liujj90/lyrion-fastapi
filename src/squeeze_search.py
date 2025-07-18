# import sys
# sys.path.append('.')

from squeezebox_controller import SqueezeBoxController
from src.db.db_conn import query_id_from_db
import os

SERVER_IP=os.environ['SERVER_IP']
SERVER_PORT=os.environ['SERVER_PORT']
DEFAULT_PLAYER=os.environ['DEFAULT_PLAYER']
controller = SqueezeBoxController(SERVER_IP, SERVER_PORT)


def search_and_play_id(id, controller=controller, player=DEFAULT_PLAYER):
    """
        search_types = {
        "SONG": {"print": "song", "local_search":"tracks", "local_loop":"titles_loop", "local_name": "title", "local_play": "track_id"},
        "ALBUM": {"print": "album", "local_search":"albums", "local_loop":"albums_loop", "local_name": "album", "local_play": "album_id"},
        "ARTIST": {"print": "artist", "local_search":"artists", "local_loop":"artists_loop", "local_name": "artist", "local_play": "artist_id"},
        "GENRE": {"print": "genre", "local_search":"genres", "local_loop":"genres_loop", "local_name": "genre", "local_play": "genre_id"},
        "PLAYLIST": {"print": "playlist", "local_search":"playlists", "local_loop":"playlists_loop", "local_name": "playlist", "local_play": "playlist_id"},
        }
    """

    _, search_type, search_term= query_id_from_db(id)
    
    search_params = {
        "player": player,
        "term": search_term, #info[id],
        "type": search_type
    }
    
    controller.search_and_play(search_params)
    return f"Playing now: {search_type} - {search_term}"

if __name__ == "__main__":

    search_and_play_id('29-5-177-240')


