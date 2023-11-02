from pydub import AudioSegment
sound1 = AudioSegment.from_file("/path/to/sound.wav", format="wav")
sound2 = AudioSegment.from_file("/path/to/another_sound.wav", format="wav")

# sound1 6 dB louder
louder = sound1 + 6


# sound1, with sound2 appended (use louder instead of sound1 to append the louder version)
combined = sound1 + sound2

# simple export
file_handle = combined.export("/path/to/output.mp3", format="mp3")
