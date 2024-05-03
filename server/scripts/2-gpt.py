from youtube_transcript_api import YouTubeTranscriptApi
import openai

# openai.api_key = 'MyAPIKey'

url = 'https://www.youtube.com/watch?v=czLh5guCFtM'
print(url)

# Extract the video ID part from the URL by first splitting on '?v=' and then on '&'
video_id = url.split('v=')[1].split('&')[0]
print(video_id)

transcript = YouTubeTranscriptApi.get_transcript(video_id)

output=''
for x in transcript:
  sentence = x['text']
  output += f' {sentence}\n'

response = openai.ChatCompletion.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": "You are a an executive assistant."},
    {"role": "assistant", "content": "write a summary of the following video transcript with only key points and topics outlined in the video"},
    {"role": "user", "content": output}
  ]
)
summary = response["choices"][0]["message"]["content"]

response = openai.ChatCompletion.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": "You are a journalist."},
    {"role": "assistant", "content": "output a list of tags for this blog post in a python list such as ['item1', 'item2','item3']"},
    {"role": "user", "content": output}
  ]
)
tag = response["choices"][0]["message"]["content"]

print('>>>SUMMARY:')
print(summary)
print('>>>TAGS:')
print(tag)
print('>>>OUTPUT:')
#print(output)

#print(transcript)