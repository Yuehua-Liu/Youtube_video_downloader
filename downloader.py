#%%
import os
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context
from pytubefix import YouTube, Playlist


def download_youtube_video(url_list, output_path="downloads"):
    try:
        for dir, url in url_list:
            # 建立下載資料夾（如果不存在）
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # 取得 YouTube 影片
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()  # 選擇最高畫質
            print(f"正在下載：{yt.title}")

            if dir:
                # 下載影片
                stream.download(f"{output_path}/{dir}")
                print(f"下載完成！影片已儲存於：{output_path}/{dir}/{yt.title}")
            else:
                # 下載影片
                stream.download(output_path)
                print(f"下載完成！影片已儲存於：{output_path}/{yt.title}")
            print("="*40)

    except Exception as e:
        print(f"發生錯誤：{e}")


# 分析是影片還是播放清單
def parse_url(url_list, output_path="downloads"):
    video_url_list = []
    for url in url_list:
        if "playlist" in url:
            playlist = Playlist(url)
            print(f"偵測到播放清單：{playlist.title}")
            # 建立下載資料夾（如果不存在）
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            # 針對播放清單建立資料夾
            playlist_path = f"{output_path}/{playlist.title}"
            if not os.path.exists(playlist_path):
                os.makedirs(playlist_path)

            for url in playlist.video_urls:
                video_url_list.append([playlist.title, url])
        else:
            video_url_list.append([None, url])
    return video_url_list


if __name__ == "__main__":
    video_url_list = ["https://youtu.be/wckNGrZuoO8",
                      "https://youtu.be/WFG0nL-of2k",
                      "https://youtu.be/jNUWS6_5bNU?si=RVryWYN49IidO1_h",
                      "https://youtube.com/playlist?list=PLTpYQm9I7B0Zw0KU7qkjqLOIVqLljNf8G&si=P6pZTDmT9DWSryp-",
                      "https://youtube.com/playlist?list=PLTpYQm9I7B0ZPgE_LP_GfaPxrxydawDIP&si=eg2xrhAcIO3vUWzz"]
    video_url_list = parse_url(video_url_list)
    download_youtube_video(video_url_list, output_path="downloads")