Twitch Highlight Generator

## Inspiration

We got inspired by the logitech challenge to make streamer's life easier. After a bit of thinking and asking around we figured that one of the most tedious tasks for a streamer is to watch his hours long VODs to extract the best moment. We decided to automate the process.

## What it does

TwitchHack will analyse the sound and the chat of a VOD and return short mp4 videos of the best and most exiting moments of the stream. 

## How I built it
We used different Python libraries to extract the chat and the sound from twitch VODs and then analyse them. Finally, we use the analysed data to extract the different highlights and return short mp4 clips.

To analyse the sound we detect the peak volume at an interval of 10 seconds and deduct an "highlight score" from the volume.

To analyse the chat we detect occurences of various keywords (e.g. "pog" or "gg" and the likes)at an interval of 10 seconds period of the video and, once more, deduct a "highlight score".

Using both "scores", we find the average between them and define a threshold over which it is considered as a "highlight".

## Challenges I ran into

We had to deal with the differences between streamers. Some streamers are really silent while they are playing and some chat are really erratic and spam for the whole duration of the stream.

## Accomplishments that I'm proud of

We created an app that manages to correctly extract the highlights from a VOD and return them to help the streamer build montages of their best moments based on the sound and the chat reactions.

## What I learned

Some of us learned to use python. We all learned the usefulness and versatility of python libraries
