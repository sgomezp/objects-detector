#from pytube import YouTube
import yt_dlp

def download_video(url, start_time, end_time, output_file):
    """
        Downloads a specific portion of a YouTube video in MP4 format.

        This function uses `yt-dlp` to download a YouTube video from the specified
        URL, trims it to the given start and end times, and saves it in MP4 format
        with the provided output filename.

        Args:
            url (str): The URL of the YouTube video to download.
            start_time (str): The start time of the video portion to download in the format 'hh:mm:ss'.
            end_time (str): The end time of the video portion to download in the format 'hh:mm:ss'.
            output_file (str): The name (and path, if needed) of the output file where the trimmed video will be saved.

        Example:
            download_video(
                url='https://www.youtube.com/watch?v=DqeXX8wkux0',
                start_time='00:00:51',
                end_time='00:01:30',
                output_file='output.mp4'
            )

        This will download and save a 39-second clip (from 00:00:51 to 00:01:30) of
        the specified YouTube video as 'output.mp4' in MP4 format.
    """
    ydl_opts = {
        'format': 'bestvideo+bestaudio[ext=mp4]/best[ext=mp4]',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': output_file,  # Output filename
        'postprocessor_args': [
            '-ss', start_time,  # Start time
            '-to', end_time,    # End time
            '-vf', 'scale=1280:720',  # Reescalar a 360p
            '-c:v', 'libx264',  # Codificar en H.264
            '-crf', '28',  # Factor de calidad, 28 es una buena referencia para reducir tamaño
            '-preset', 'fast'  # Preset para calidad de compresión
        ],
        'merge_output_format': 'mp4',  # Ensure the output is in MP4 format
    }
    with yt_dlp.YoutubeDL(ydl_opts)as ydl:
        ydl.download([url])


video_url = 'https://www.youtube.com/watch?v=JKsmzu6rX2o'


# Tiempo de inicio y fin en formato hh:mm:ss
start_time = '00:02:38'
end_time = '00:03:30'

output_file = 'output_cars.mp4'

download_video(video_url,start_time,end_time,output_file)

