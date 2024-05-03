from youtube_transcript_api import YouTubeTranscriptApi
import openai

# openai.api_key = 'MyAPIKey'

url = 'https://www.youtube.com/watch?v=czLh5guCFtM'
print(url)

# Extract the video ID part from the URL by first splitting on '?v=' and then on '&'
video_id = url.split('v=')[1].split('&')[0]
print(video_id)

transcript = YouTubeTranscriptApi.get_transcript(video_id)

response = openai.ChatCompletion.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": "You are a database computer"},
    {"role": "assistant", "content": "data is stored in JSON {text:'', start:'', duration:''}"},
    {"role": "assistant", "content": str(transcript)},
    {"role": "user", "content": "what are the topics discussed in this video. Provide start time codes in seconds and also in minutes and seconds"}
  ]
)
timecode = response["choices"][0]["message"]["content"]

print(timecode)