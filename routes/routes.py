import os
from flask import render_template, request, redirect, url_for, Response, flash
from processing.video_processing import download_video, process_video


video_dir = './static/videos/'  # Directorio donde están almacenados los videos

def configure_routes(app):

    @app.route('/')
    def home():
        try:
            # filter only videos
            all_files = os.listdir(video_dir)
            videos = [f for f in all_files if f.endswith(('.mp4', '.avi', '.mov'))]
            videos = os.listdir(video_dir)
        except FileNotFoundError:
            flash("Error: The video directory does not exist.", 'danger')
            videos = []
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", 'danger')
            videos = []
        return render_template("home.html", videos=videos)

    @app.route('/download_and_process', methods=['POST'])
    def download_and_process():
        url = request.form['url']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        output_name = request.form['output_name']
        output_file = os.path.join(video_dir, output_name + '.mp4')

        # Check if the video exists
        if os.path.exists(output_file):
            flash(
                f"Error: A video with the name '{output_name}' already exists. Please choose a different name.",
                'danger')
            return render_template(
                "home.html",
                videos=os.listdir(video_dir),
                url=url,
                start_time=start_time,
                end_time=end_time,
                output_name=output_name
            )

        try:
            # Descargar y procesar el video
            download_video(url, start_time, end_time, output_file)
        except Exception as e:
            flash(f"Error during video download and processing: {str(e)}", 'danger')
            return redirect(url_for('home'))

        return redirect(url_for('play_video', video=output_name + '.mp4'))

    @app.route('/play_video')
    def play_video():
        video_name = request.args.get('video')
        if not video_name:
            flash(f"Error: video {video_name} not found.", 'danger')
            return redirect(url_for('home'))

        return render_template('show_video.html', video_name=video_name)

    @app.route('/video_feed')
    def video_feed():
        video_name = request.args.get('video')
        video_path = os.path.join(video_dir, video_name)

        if not os.path.exists(video_path):
            flash(f"Error: video {video_name} not found.", 'danger')
            return redirect(url_for('home'))

        try:
            return Response(process_video(video_path),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        except Exception as e:
            flash(f"Error processing video: {str(e)}", 'danger')
            return redirect(url_for('home'))



