import os
from flask import render_template, request, redirect, url_for, Response
from processing.video_processing import download_video, process_video

video_dir = './static/videos/'  # Directorio donde están almacenados los videos

def configure_routes(app):

    @app.route('/')
    def home():
        videos = os.listdir(video_dir)
        return render_template("home.html", videos=videos)

    @app.route('/download_and_process', methods=['POST'])
    def download_and_process():
        url = request.form['url']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        output_name = request.form['output_name']
        output_file = os.path.join(video_dir, output_name + '.mp4')

        print(f"URL: {url}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")

        # Descargar y procesar el video
        download_video(url, start_time, end_time, output_file)

        return redirect(url_for('home'))

    @app.route('/play_video')
    def play_video():
        video_name = request.args.get('video')
        if not video_name:
            return redirect(url_for('home'))

        #video_path = os.path.join(video_dir, video_name)
        return render_template('show_video.html', video_name=video_name)

    @app.route('/video_feed')
    def video_feed():
        video_name = request.args.get('video')
        video_path = os.path.join(video_dir, video_name)
        return Response(process_video(video_path),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

