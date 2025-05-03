import sys
import json
from typing import List # pylint: disable=unused-import
from option import Result, Option, Ok, Err # pylint: disable=unused-import
from rust_enum import Case, enum # pylint: disable=unused-import
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from concurrent.futures import ThreadPoolExecutor, as_completed
import colorama
from colorama import Fore
from youtube_search import YoutubeSearch
from json_helper import json_to_objects
from models import Song, YtVideo, Playlist

colorama.init(autoreset=True)

# @enum
# class Error:
#     FileOpenFail = Case(inner=str)
#     Test = Case()

def read_playlist(name: str) -> Result[List[Song], str]:
    try:
        with open(f"./playlists/{name}.json", "r", encoding="utf-8") as p:
            return json_to_objects(json.load(p), Song)
    except FileNotFoundError as e:
        return Err(f"Playlist {name} not found ({e})")
    except Exception as e: # pylint: disable=broad-exception-caught
        return Err(f"{e}")


def search_song(song: Song) -> Result[YtVideo, str]:
    search = YoutubeSearch(f"{song.title} by {song.artist}", max_results=1)

    obj_res = json_to_objects(search.to_dict(), YtVideo)

    if obj_res.is_err:
        return obj_res

    obj = obj_res.unwrap()

    if len(obj) == 0:
        return Err("Found nothing")

    return obj_res.map(lambda vids: vids[0])

def create_google_context():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    flow = InstalledAppFlow.from_client_secrets_file("secret.json", scopes)

    creds = flow.run_local_server(port=42070)
    
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    return youtube

def fetch_and_insert_song(song, index, playlist_len, new_playlist_id, youtube):
    print(f"Fetching song {index + 1}/{playlist_len}: {song.title} by {song.artist}")

    video_res = search_song(song)

    if video_res.is_err:
        return (song.title, song.artist, Fore.RED + f"Failed to fetch yt video due to: {video_res.unwrap_err()}")
    
    video = video_res.unwrap()


    return (song.title, song.artist, video.id)

def insert_to_playlist(video, playlist_id, youtube_service):
    youtube_service.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,  # an actual playlistid
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video.id
                }
            }
        }
    ).execute()
    

def main():
    playlist_name = "spotify_liked_export"

    playlist_res = read_playlist(playlist_name)

    if playlist_res.is_err:
        print(Fore.RED + f"Could not deserialise playlist due to: {playlist_res.unwrap_err()}")
        sys.exit(1)

    playlist = playlist_res.unwrap()

    youtube = create_google_context()

    res = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": f"Imported playlist '{playlist_name}'",
            }
        }
    ).execute()

    print()

    new_playlist_id = res["id"]
    playlist_len = len(playlist)

    print(new_playlist_id)

    batch = youtube.new_batch_http_request()

    videos = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i, song in enumerate(playlist):
            futures.append(executor.submit(search_song, song))
    
        for future in as_completed(futures):
            result = future.result()
            if result.is_err:
                print(Fore.RED + f"{result.unwrap_err()}")
            else:
                video = result.unwrap()
                print(Fore.GREEN + f"{video}")
                videos.append(video)


    # batch = youtube.new_batch_http_request()

    # for video in videos:
    #     batch.add(youtube.playlistItems().insert(
    #         part="snippet",
    #         body={
    #           "snippet": {
    #             "playlistId": new_playlist_id,
    #             "position": 0,
    #             "resourceId": {
    #               "kind": "youtube#video",
    #               "videoId": video.id
    #             }
    #           }
    #         }
    #       )
    #     )

    # print("Executing batch");

    # responses = batch.execute()

    print("Executing")
    
    for i, video in enumerate(videos):
        print(f"{i+1}/{len(videos)}")
        insert_to_playlist(video, new_playlist_id, youtube)

    
    
    print("Done")


if __name__ == "__main__":
    main()
