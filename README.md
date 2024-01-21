# TTS_Abhishek

Welcome to the repository for TTS_Abhishek. This project convert text to audio.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Before you begin, make sure you have the following installed on your machine:

•⁠  ⁠[Python](https://www.python.org/downloads/) (version 3.8 or higher)

### Clone the Repository

Use the following command to clone the repository to your local machine:

```bash
git clone https://github.com/vohraa23/TTS_Abhishek.git
Set up Virtual Environment
Navigate to the project directory and create a virtual environment using Python's venv module:

bash
Copy code
python -m venv venv
Activate the Virtual Environment
On Windows, use:

bash
Copy code
venv\Scripts\activate
On macOS and Linux, use:

bash
Copy code
source venv/bin/activate
Your command prompt or terminal should now indicate that you are in the virtual environment.

Install Dependencies
While in the virtual environment, install the project dependencies using:

bash
Copy code
pip install -r requirements.txt

```
## This is how folder structure look like
/Abhishek 2
    /app
        _init_.py
        views.py
		    ttd_code.py
    /templates
        index.html
		/static
        style.css
  main.py
	Dockerfile
	requirements.txt
 
## 1.⁠ ⁠views.py
Purpose:
Defines the view functions and routes for the Flask application.

Functionality:
Imports necessary modules and the Flask app instance.
Defines two routes: / and /generate_audio.
The / route renders an "index.html" template.
The /generate_audio route handles a POST request for generating audio based on the provided text.
Utilizes a Text-to-Speech (TTS) synthesizer from app.tts_code to convert text to audio.
Handles exceptions and logs errors, returning appropriate responses.
Key Code:
python
Copy code
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
 ## 2.⁠ ⁠tts_code.py
Purpose:
Sets up a Text-to-Speech (TTS) synthesizer using the TTS library.

Functionality:
Imports necessary modules from the TTS library.
Uses a ModelManager to download a pre-trained TTS model and vocoder.
Initializes a Synthesizer object with the downloaded checkpoints and configurations.
Key Code:
python
Copy code
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import site
location = site.getsitepackages()[0]

path = "/config/workspace/TTS/.models.json"

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])

synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)
 ## 3.⁠ ⁠main.py
Purpose:
Entry point for the Flask application.

Functionality:
Imports the debug function from distutils.log and the Flask app instance from the app module.
Imports the view functions (index and generate_audio) from the app.views module.
Adds URL rules for the index and generate_audio routes.
Starts the Flask application using app.run().
Key Code:
python
Copy code
from distutils.log import debug
from app import app
from app.views import index, generate_audio

app.add_url_rule("/", "index", index)
app.add_url_rule("/generate_audio", "generate_audio", generate_audio)

if _name_ == "_main_":
    app.run(debug=True, host="0.0.0.0", port="9000")

## 4. index.html
Purpose:
Defines the structure and content of the webpage for a Text-to-Speech (TTS) audio generator.

HTML Structure:
 A.⁠ ⁠Document Type Declaration (DOCTYPE):
html
Copy code
<!DOCTYPE html>
Declares the document type and version of HTML being used.
 B.⁠ ⁠HTML Opening Tag:
html
Copy code
<html lang="en">
The root element of the HTML document, specifying the language as English.
 C.⁠ ⁠Head Section:
html
Copy code
<head>
    <!-- Meta tags for character set, compatibility, and viewport -->
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Link to an external CSS file for styling -->
    <link rel="stylesheet" href="/static/style.css">
    
    <!-- Title of the webpage -->
    <title>TTS Audio Generator</title>
</head>
Contains metadata about the HTML document, including character set, compatibility settings, and viewport information.
Links an external CSS file (style.css) for styling.
Sets the title of the webpage to "TTS Audio Generator."
 D.⁠ ⁠Body Section:
html
Copy code
<body>
    <div class="container">
        <!-- Page heading -->
        <h1>TTS Audio Generator</h1>
        
        <!-- Form for user input -->
        <form action="/generate_audio" method="post">
            <label for="text">Enter your text:</label>
            <!-- Textarea for entering text -->
            <textarea id="text" name="text" rows="4" cols="50"></textarea>
            <br>
            <!-- Button to submit the form and generate audio -->
            <button type="submit">Generate Audio</button>
        </form>
   </div>
</body>
 E.⁠ ⁠HTML Closing Tag:
html
Copy code
</html>
Closes the HTML document.

## 5. Docker File
A.⁠ ⁠Use an official Python runtime as a parent image
Dockerfile
Copy code
FROM python:3.9

Purpose: Specifies the base image for the Docker container.

Functionality: Uses the official Python 3.9 image as the parent image.

 
 B.⁠ ⁠Set the working directory in the container
Dockerfile
Copy code
WORKDIR /app

Purpose: Sets the working directory inside the Docker container to /app.

Functionality: Subsequent commands will be executed in this directory.

 
 C.⁠ ⁠Install system dependencies including Rust compiler
Dockerfile
Copy code
RUN apt-get update \
    && apt-get install -y libsndfile1 curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y

Purpose: Installs system dependencies required for the application, including the Rust compiler.

Functionality:Updates the package lists (apt-get update).Installs the libsndfile1 library and curl.Downloads and installs the Rust compiler using the official Rust installer script.


 D.⁠ ⁠Add Rust binaries to the PATH
Dockerfile
Copy code
ENV PATH="/root/.cargo/bin:${PATH}"

Purpose: Adds the Rust binaries to the system's PATH.

Functionality: Ensures that the Rust binaries are available for use in subsequent commands.

 
 E.⁠ ⁠Install Rust
Dockerfile
Copy code
RUN rustup update

Purpose: Updates the Rust toolchain.
Functionality: Runs rustup update to ensure that the Rust compiler and tools are up-to-date.

 
 F.⁠ ⁠Copy requirements.txt to the container
Dockerfile
Copy code
COPY ./requirements.txt /app/requirements.txt

Purpose: Copies the requirements.txt file from the local machine to the /app directory in the container.

Functionality: Prepares the container for installing Python dependencies.

 
 G.⁠ ⁠Update pip and install libraries in requirements.txt
Dockerfile
Copy code
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

Purpose: Updates the pip package manager and installs Python libraries specified in requirements.txt.

Functionality: Upgrades pip to the latest version. Installs the Python dependencies listed in requirements.txt.

 
 H.⁠ ⁠Copy the rest of your application code
Dockerfile
Copy code
COPY . /app

Purpose: Copies the entire content of the local directory to the /app directory in the container.

Functionality: Transfers the application code, including source code and any additional files, into the container.

 
 I.⁠ ⁠Set the entry point
Dockerfile
Copy code
ENTRYPOINT ["python"]

Purpose: Sets the default executable when the container starts.

Functionality: Specifies that the default command to execute is python.


J.⁠ ⁠Set the default command to run your application
Dockerfile
Copy code
CMD ["main.py"]

Purpose: Sets the default command to run when the container starts if no other command is provided.

Functionality: Specifies that the default command is to run the main.py script.

## Result foR get and post request
**GET::

<img width="1280" alt="GET" src="https://github.com/vohraa23/TTS_Abhishek/assets/144794427/19fe41bd-56dc-42a2-be4d-261db3277259">

**POST::

<img width="1280" alt="POST" src="https://github.com/vohraa23/TTS_Abhishek/assets/144794427/4fa9105f-6855-45f9-8381-cc48669c495a">

## Websocket
Dislpaying the result through websocket

<img width="1344" alt="Screenshot 2024-01-21 at 4 22 14 PM" src="https://github.com/vohraa23/TTS_Abhishek/assets/144794427/22185591-d025-407a-8eb5-0c2ceb68f4aa">


























##                                                                                THANK YOU

