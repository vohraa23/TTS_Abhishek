import runpod
from app.tts_code import synthesizer  # Import from your TTS module
import io
import base64

def handler(event):
  try:
    text = event['input']['transcript']
    audio_array = synthesizer.tts(text)  # Utilize your synthesizer function
    out = io.BytesIO()
    synthesizer.save_wav(audio_array, out)  # Employ your save_wav function
    out.seek(0)
    data = out.read()
    return {
      "wav": base64.b64encode(data).decode('ascii')
    }
  except Exception as e:
    # Log the error and return an error response
    runpod.logger.error(f"An error occurred: {e}")
    return {"error": "Internal server error"}, 500

runpod.serverless.start({"handler": handler})
