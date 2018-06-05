import os
from ffmpy import FFmpeg
import wave


def convert(input_audio):
    # ================ Audio converter =================
    #   - mp3 to wav
    #   - sample rate(22050Hz to 44100Hz)
    #   - channel(mono to stereo)
    # ==================================================

    convert_audio = "convert_audio.wav"
    cmd_convert = "ffmpeg -i {} -ar 44100 -ac 2 -y {}".format(input_audio, convert_audio)
    os.system(cmd_convert)
    print("Convert mp3 to wav")

    return convert_audio


def pcm2wav(path):
    ff = FFmpeg(
            inputs={path: ['-f', 's16le', '-ar', '16000', '-ac', '2']},
            outputs={''.join([path, '.wav']): '-y'})
    ff.run()


def combine_audios(out_audio, audio_list):
    with wave.open(out_audio, "wb") as output:
        for file_in in audio_list:
            with wave.open(file_in, 'rb') as wav_in:
                if not output.getnframes():
                    output.setparams(wav_in.getparams())
                output.writeframes(wav_in.readframes(wav_in.getnframes()))