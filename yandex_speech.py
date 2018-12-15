import wave
import os.path
import logging
from hashlib import md5

import pyaudio
import requests

from private_settings import YANDEX_KEY_API

log = logging.getLogger(__name__)

__all__ = ('text_to_voice',)

s = requests.Session()
BASE_URL = 'https://tts.voicetech.yandex.net/generate'
CACHE_DIR = 'cache'


def text_to_voice(text):
    chunk = 1024

    f = wave.open(_get_file(text), 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(chunk)
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()


def _get_file(text):
    h = md5(text.encode('utf8')).hexdigest()
    filename = os.path.join(CACHE_DIR, '%s.wav' % h)
    if not os.path.exists(filename):
        r = s.request('GET', BASE_URL, params=dict(
            key=YANDEX_KEY_API,
            text=text,
            format='wav',  # <mp3|wav|opus>
            lang='ru-RU',  # <ru-RU|en-US|uk-UK|tr-TR>
            speaker='oksana',  # <jane|oksana|alyss|omazh|zahar|ermil>
            quality='hi',  # 'lo'
            emotion='evil',  # '<good|neutral|evil>]
            # & [speed=<скорость речи>]
        ))
        r.raise_for_status()
        content = r.content
        with open(filename, 'wb') as f:
            f.write(content)
    return filename


if __name__ == '__main__':
    import sys
    text_to_voice(sys.argv[1])
