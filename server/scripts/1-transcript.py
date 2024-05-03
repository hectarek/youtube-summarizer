from youtube_transcript_api import YouTubeTranscriptApi

url = 'https://www.youtube.com/watch?v=czLh5guCFtM'
print(url)

# Extract the video ID part from the URL by first splitting on '?v=' and then on '&'
video_id = url.split('v=')[1].split('&')[0]
print(video_id)

transcript = YouTubeTranscriptApi.get_transcript(video_id)

print(transcript)

output=''

for x in transcript:
  sentence = x['text']
  output += f' {sentence}\n'

print(output)