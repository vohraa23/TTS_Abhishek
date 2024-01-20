from distutils.log import error
from app import app
import io
from flask import render_template, request, send_file
from app.tts_code import synthesizer

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    try:
        text = request.form.get("text")

        if text:
            outputs = synthesizer.tts(text)
            out = io.BytesIO()
            synthesizer.save_wav(outputs, out)
            return send_file(out, mimetype="audio/wav", as_attachment=True, download_name="generated_audio.wav")
        else:
            return {"error": "Please provide the text"}, 400
    except Exception as e:
        # Log the error and return an internal server error
        app.logger.error(f"An error occurred: {e}")
        return {"error": "Internal server error"}, 500