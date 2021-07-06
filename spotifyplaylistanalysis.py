import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os
import unicodedata
from unicodedata import normalize
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np


def setup(CLIENT_SECRET, CLIENT_ID):
    auth_manager=SpotifyClientCredentials(
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


def make_playlists_dict(sp, USER_ID):
    playlists = sp.user_playlists(USER_ID)
    all_playlists_dict = {}
    for playlist in playlists['items']:
      all_playlists_dict[playlist['name'].lower()] = {
       'id' : playlist['id'],
       'number_of_tracks' : playlist['tracks']['total'],
       'name_stylized' : playlist['name']}
    return all_playlists_dict
    #playlists_col_names = ['id', 'playlist_name', 'number_of_tracks']
    #all_playlists_df = make_dataframe(playlists_col_names)
    #playlists_to_dataframe(all_playlists_df, playlists)
    #return all_playlists_df


# def playlists_to_dataframe(df, playlists):
#    for playlist in playlists['items']:
#        df.loc[len(df.index)] = [playlist['id'],
#                                 playlist['name'],
#                                 playlist['tracks']['total']]


def make_dataframe(col_names):
    df = pd.DataFrame(columns=col_names)
    return df


# Test 1: what if table_name already exists and you don't want to replace
def make_data_base(table_name, df, database_name):
    engine = create_engine('mysql://root:codio@localhost/' + database_name +'?charset=utf8mb4', encoding='utf-8')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)


def save_data_base(database_name):
    os.system("mysqldump -u root -pcodio " + database_name + " > " + database_name + ".sql")


def load_data_base(database_name):
    os.system("mysqldump -u root -pcodio " + database_name + " < " + database_name + ".sql")


# def playlist_to_row(df, playlist):
      # name = unicodedata.normalize('NFKD', playlist['name']).encode('UTF-8', 'ignore')
      


# def playlist_dataframe_to_table(all_playlists_df, db_name):
#    make_data_base('all_playlists', all_playlists_df, db_name)

def make_playlist_dataframe(desried_playlist, playlists, sp):
    # get playlist id using name
    playlist_id = playlists[desried_playlist]['id']
    table_name = playlist_id
    playlist_info = sp.user_playlist(USER_ID, playlist_id=playlist_id)
    list_of_songs = playlist_info['tracks']['items']
    playlist_col_names = ['id', 'song_name', 'artist', 'popularity']
    playlist_df = make_dataframe(playlist_col_names)
    song_list_to_dataframe(playlist_df, list_of_songs)
    return playlist_df


def song_list_to_dataframe(df, list_of_songs):
    for song_data in list_of_songs:
        song = song_data['track']
        df.loc[len(df.index)] = [song['id'], song['name'], song['artists'][0]['name'], song['popularity']]


# def histogram(df, col_name):
    # df.hist(column=col_name)
    # df.hist()
    # plt.show()

CLIENT_ID = '45505ed8cb474aebb71af15ea0eea7b2'
CLIENT_SECRET = 'b178b1670a9c4376b1b652d95a9d4247'
AUTH_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI='https://github.com/unwosu6'
USER_ID = '12179993316'
scope = "user-library-read, playlist-read-private"
db_name = 'spotify'
os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '+db_name+'; "')



sp = setup(CLIENT_SECRET, CLIENT_ID)
print(type(sp))
playlists = make_playlists_dict(sp, USER_ID) 

desried_playlist = input('What playlist would you like me to analyze?: ').lower()

#print(sp.track('1EjTKRH6JcaK72p1TDtSoY?si=e65d86be4410409e'))

# if desried_playlist not in playlists.loc['playlist_name']:
#    print('I can\'t seem to find the playlist you want me to analyze. Would you like to try again?')

playlist_df = make_playlist_dataframe(desried_playlist, playlists, sp)
make_data_base(playlists[desried_playlist]['id'], playlist_df, db_name)

# for playlist in playlists['items']:
#    if playlist['name'].lower().startswith(desried_playlist.lower()):

#histogram(playlist_df['popularity'], 'popularity')
#print(playlist_df['popularity'].describe())


