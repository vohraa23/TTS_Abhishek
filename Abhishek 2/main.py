from distutils.log import debug
from app import app
from app.views import index, generate_audio

app.add_url_rule("/", "index", index)
app.add_url_rule("/generate_audio", "generate_audio", generate_audio)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="9000")