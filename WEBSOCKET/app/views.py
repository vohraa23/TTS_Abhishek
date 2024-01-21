from distutils.log import error
import io
import time
from flask import render_template, request, Response
from flask_socketio import SocketIO
from app import app

from app.tts_code import synthesizer

socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    try:
        text = request.form.get("text")
        sid = request.form.get("sid")

        if text is not None and sid is not None:
            # Emit a message to start the conversion
            socketio.emit("start_conversion", {"sid": sid}, namespace="/")

            start_time = time.time()  # Record the start time

            outputs = synthesizer.tts(text)
            out = io.BytesIO()
            synthesizer.save_wav(outputs, out)

            end_time = time.time()  # Record the end time
            time_taken = end_time - start_time

            # Emit a message with the conversion time
            socketio.emit("audio_ready", {"time_taken": time_taken}, room=sid, namespace="/")

            # Return the audio file as a streaming response
            return Response(out.getvalue(), mimetype="audio/wav", status=200)
        else:
            return {"error": "Please provide both text and sid in the request body"}, 400
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return {"error": "Internal server error"}, 500

@socketio.on("connect", namespace="/")
def handle_connect():
    print(f"Client connected: {request.sid}")