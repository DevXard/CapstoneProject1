import requests


def movies_muse(title):
    res = requests.get(f'https://tastedive.com/api/similar?q={title}&type=movies&info=1')
    
    data = res.json()
    return {
        'info': data['Similar']['Info'],
        'results': data['Similar']['Results']
    }


def song_l(artist, title):
    res = requests.get(f'https://api.lyrics.ovh/v1/{artist}/{title}')
    
    return res.json()