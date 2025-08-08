import torch
import readline
from kokoro import KPipeline
import sounddevice as sd
import atexit
import readline
histfile = './tts_history'

try:
    readline.read_history_file(histfile)
    h_len = readline.get_current_history_length()
except FileNotFoundError:
    open(histfile, 'wb').close()
    h_len = 0

def save(prev_h_len, histfile):
    new_h_len = readline.get_current_history_length()
    readline.set_history_length(1000)
    readline.append_history_file(new_h_len - prev_h_len, histfile)
atexit.register(save, h_len, histfile)


def main():
    streamer = sd.OutputStream(samplerate=24000, channels=1, dtype='float32')
    streamer.start()
    pipeline = KPipeline(lang_code='a',repo_id='hexgrad/Kokoro-82M')
    voice = "af_heart"
    speed = 1
    vol_factor = 1
    while True:
        try:
            text = input('>')
            if text.startswith('v='):
                voice = text.lstrip('v=')
                continue
            elif text.startswith('s='):
                speed = float(text.lstrip('s='))
                continue
            elif text.startswith('f='):
                vol_factor = float(text.lstrip('f='))
                continue
            for i, (_, _, audio) in enumerate(pipeline(text, voice=voice, speed=speed)):
                audio = torch.mul(audio, vol_factor)
                streamer.write(audio)
        except (KeyboardInterrupt, SystemExit, EOFError):
            break

if __name__ == "__main__":
    main()
