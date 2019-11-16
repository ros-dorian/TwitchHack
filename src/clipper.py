#import matplotlib
#import matplotlib.pyplot as plt
import json
import numpy as np
import math
import pydub
from pydub import AudioSegment
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip

def comments_score(comments, keywords, grouping, start_time, end_time):
    scores = {}

    grouping = int(grouping) if grouping else 10
    for comment_info in comments:
        time_since_start = int(math.ceil(comment_info['content_offset_seconds'] / grouping)) * grouping

        if (start_time and end_time) and (time_since_start < int(start_time) or time_since_start > int(end_time)):
            continue

        if time_since_start not in scores:
            scores[time_since_start] = 0 

        comment_score = [1 if w in k else 0 for w in comment_info['message']['body'].lower().split(' ') for k in keywords]
        scores[time_since_start] += sum(comment_score)

    return scores

def extract_sound(video_name, ext):
    clip = mp.VideoFileClip(video_name + "." + ext)
    clip.audio.write_audiofile(video_name + ".wav")

    
def create_clip(original_video, cut_from, cut_to, clip_name, ext):
    with VideoFileClip(original_video) as video:
        new = video.subclip(cut_from, cut_to)
        new.write_videofile(clip_name + "." + ext, audio_codec='aac')
    
    
def generate_plot(sound_name):
    start_time = 0
    end_time = 10

    song = AudioSegment.from_wav(sound_name)

    original_array = []
    final_array = []

    while end_time <= 45 * 60:
        extract = song[start_time * 1000:end_time * 1000]
        val = extract.rms + 96

        original_array.append(val)

        start_time = start_time + 10
        end_time = end_time + 10

    max_peak_value = max(original_array)

    for val in original_array:
        final_array.append(val * 1 / max_peak_value)
    return final_array


if __name__ == "__main__":
    tfrom = 16560
    tto = 19260
    grouping = 10

    movie_name = "G2-SKT"
    movie_ext = "mp4"
    sound_ext = "wav"
    json_ext = "json"
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

    extract_sound('../res/' + movie_name, movie_ext)
    sound = np.array(generate_plot('../res/{}.{}'.format(movie_name, sound_ext)))
    sound_grad = [grad if grad > 0 else 0 for grad in np.gradient(sound)]

    # read file
    with open('../res/{}.{}'.format(movie_name, json_ext), 'r') as file:
        data=file.read()
        
    chat = json.loads(data)

    scores = comments_score(chat['comments'], keywords, grouping, tfrom, tto)
    lscore = []
    for i in range(tfrom, tto, grouping):
        if i in scores:
            lscore.append(scores[i])
        else:
            lscore.append(0)
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
    start = 0
    end = 0
    clip = 0
    threshold = 0.1
    for i in range(len(final)):
        sec = i * 10
        if final[i] >= threshold:
            if not in_highlight:
                print('From: {}:{}'.format(math.floor(sec/60), sec%60))
                start = sec
            in_highlight = True
        else:
            if in_highlight:
                print('To: {}:{}'.format(math.floor(sec/60), sec%60))
                end = sec
                clip = clip + 1
                create_clip('../res/{}.{}'.format(movie_name, movie_ext), start, end + grouping, "../res/output/{}-{}".format(movie_name, clip), 'mp4')
            in_highlight = False
            
        
    #t = np.arange(0, 45*60, 10)

    #fig, ax = plt.subplots()

    #ax.plot(t, final)

    #ax.set(xlabel='time (s)', ylabel='score', title='bla')
    #ax.grid()

    #plt.show()

    #plt.plot(sound_grad)
    #plt.plot(lscore_grad)

    #plt.show()
