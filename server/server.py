import os
import time
import markdown
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# app instance
app = Flask(__name__)

# OpenAI instance
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://youtube-summarizer-client.vercel.app"])

### ROUTES

@app.route("/api/summarize", methods=['POST'])
def summarize_video():
    if request.is_json:
        data = request.get_json()
        url = data.get('url', {}).get('url')

        if not url:
            return jsonify({"status": "error", "message": "URL not provided"}), 400

        # Extract video ID
        try:
            video_id = url.split('v=')[1].split('&')[0]

        except IndexError:
            return jsonify({"status": "error", "message": "Invalid URL format"}), 400

        # Retrieve transcript asynchronously if possible (this part is synchronous in your case)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)  # This call is synchronous
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400

        # Process transcript into text
        output = ' '.join([x['text'] for x in transcript])


        start_time = time.time()  # Start time before the request

        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant."},
                {"role": "assistant", "content": "Write a summary with key points and topics outlined."},
                {"role": "user", "content": output}
            ]
        )

        summary_duration = time.time() - start_time  # Calculate duration
        summary = summary_response.choices[0].message.content
        formattedSummary =  markdown.markdown(summary)

        start_time = time.time()  # Reset time before the next request

        tag_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a journalist."},
                {"role": "assistant", "content": "output a list of tags for this blog post."},
                {"role": "user", "content": output}
            ]
        )
        
        tag_duration = time.time() - start_time  # Calculate duration
        tags = tag_response.choices[0].message.content

        # Return result
        return jsonify({
            "status": "success",
            "summary": formattedSummary,
            "summary_time": summary_duration,
            "tags": tags,
            "tags_time": tag_duration,
            "transcript": output,
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

if __name__ == "__main__":
    app.run(port=8080)