import os
import asyncio
import markdown
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import AsyncOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# app instance
app = Flask(__name__)

# OpenAI instance
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

CORS(app, supports_credentials=True, origins=["http://localhost:3000", "youtube-summarizer-client.vercel.app"])


### ROUTES

# /api/home
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        "message": "Hello world!",
        "people": ['Jack', 'Sarah', "Alex"]
    })

# POST route for /api/feedback
@app.route("/api/feedback", methods=['POST'])
def receive_feedback():
    # Check if the request contains JSON data
    if request.is_json:
        # Get the JSON data
        data = request.get_json()
        
        # Process or store the feedback here
        # For now, we're just returning it back as a confirmation
        return jsonify({
            "status": "success",
            "message": "Feedback received",
            "data": data
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

@app.route("/api/summarize", methods=['POST'])
async def summarize_video():
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

        # Generate summary asynchronously
        summary_response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant."},
                {"role": "assistant", "content": "Write a summary with key points and topics outlined."},
                {"role": "user", "content": output}
            ]
        )
        summary = summary_response.choices[0].message.content
        formattedSummary =  markdown.markdown(summary)

        # Generate tags asynchronously
        tag_response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a journalist."},
                {"role": "assistant", "content": "output a list of tags for this blog post."},
                {"role": "user", "content": output}
            ]
        )
        tags = tag_response.choices[0].message.content

        # Return result
        return jsonify({
            "status": "success",
            "summary": formattedSummary,
            "tags": tags,
            "transcript": output
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

if __name__ == "__main__":
    app.run(port=8080)