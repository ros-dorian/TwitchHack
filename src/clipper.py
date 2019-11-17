#import matplotlib
#import matplotlib.pyplot as plt
import click
import json
import numpy as np
import math
import pydub
from pydub import AudioSegment
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip

def comments_score(comments, keywords, grouping, start_time, end_time):
    scores = {}

    for comment_info in comments:
        time_since_start = int(math.ceil(comment_info['content_offset_seconds'] / grouping)) * grouping

        if (start_time and end_time) and (time_since_start < int(start_time) or time_since_start > int(end_time)):
            continue

        if time_since_start not in scores:
            scores[time_since_start] = 0 

        comment_score = [1 if w in k else 0 for w in comment_info['message']['body'].lower().split(' ') for k in keywords]
        scores[time_since_start] += sum(comment_score)

    return scores

def extract_sound(clip, name):
    clip.audio.write_audiofile(name + ".wav")

    
def create_clip(clip_name, cut_from, cut_to, output_name, ext):
    print(cut_from, cut_to)
    with VideoFileClip(clip_name) as video:
        new = video.subclip(cut_from, cut_to)
        new.write_videofile(output_name + "." + ext, audio_codec='aac')
    
    
def get_sound_score(sound_name, duration):
    start_time = 0
    end_time = 10

    song = AudioSegment.from_wav(sound_name)

    original_array = []
    final_array = []

    while end_time <= duration:
        extract = song[start_time * 1000:end_time * 1000]
        val = extract.rms + 96

        original_array.append(val)

        start_time = start_time + 10
        end_time = end_time + 10

    max_peak_value = max(original_array)

    for val in original_array:
        final_array.append(val * 1 / max_peak_value)
    return final_array


@click.command()
@click.argument('stream')
@click.option('--grouping', '-o')
@click.option('--start', '-s')
@click.option('--end', '-e')
@click.option('--threshold', '-t')
def main(stream, grouping=None, start=None, end=None, threshold=None):
    stream_ext = 'mp4'
    sound_ext = 'wav'
    chat_ext = 'json'
    keywords = [
        'pog',
        'omg',
        'gg',
        'wtf',
        'dang',
        'clip',
        'holy',
        'nice',
        'kappa',
        'trihard',
        'tryhard',
        '4head',
        'cmonburh',
        'lul',
        'cy@'
    ]

    clip = mp.VideoFileClip('res/{}.{}'.format(stream, stream_ext))
    extract_sound(clip, 'res/{}'.format(stream))
    sound = np.array(get_sound_score('res/{}.{}'.format(stream, sound_ext), clip.duration))
    sound_grad = [grad if grad > 0 else 0 for grad in np.gradient(sound)]

    print(clip.duration)

    # read file
    with open('res/{}.{}'.format(stream, chat_ext), 'r') as file:
        data=file.read()
        
    chat = json.loads(data)

    grouping = int(grouping) if grouping else 10
    start = int(start) if start else 0
    
    scores = comments_score(chat['comments'], keywords, grouping, start, end)

    end = int(end) if end else scores.keys([-1])
    
    lscore = [scores[i] if i in scores else 0 for i in range(start, end, grouping)]
    lscore = lscore / np.max(lscore)
    lscore_grad = [grad if grad > 0 else 0 for grad in np.gradient(lscore)]

    combination = np.zeros(min(len(lscore), len(sound)))

    for i in range(min(len(lscore), len(sound))):
        combination[i] = (lscore_grad[i] + sound_grad[i]) / 2

    acc = 0
    final = np.zeros(len(combination))
    for i in range(len(combination)):
        if combination[i] > 0:
            acc = acc + combination[i]
        else:
            acc = acc / 2
        final[i] = acc
    final = [grad if grad > 0 else 0 for grad in np.gradient(final)]
        
    in_highlight = False
    highlight_start = 0
    highlight_end = 0
    clip_index = 0
    threshold_highlight = float(threshold) if threshold != None else 0.1
    timestamps = []
    for i in range(len(final)):
        sec = i * 10
        if final[i] >= threshold_highlight:
            if not in_highlight:
                #print('From: {}:{}'.format(math.floor(sec/60), sec%60))
                highlight_start = sec
            in_highlight = True
        else:
            if in_highlight:
                #print('To: {}:{}'.format(math.floor(sec/60), sec%60))
                highlight_end = sec
                clip_index = clip_index + 1
                timestamps.append([highlight_start + 5, min(highlight_end + 25, clip.duration)])
            in_highlight = False
    if in_highlight:
        timestamps.append([highlight_start + 5, clip.duration])

    for i in range(len(timestamps)):
        create_clip('res/{}.{}'.format(stream, stream_ext), timestamps[i][0], timestamps[i][1], "res/output/{}-{}".format(stream, i+1), 'mp4')

if __name__ == "__main__":
    main()
