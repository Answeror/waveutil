from . import io
import pyaudio


class Microphone(object):

    def __init__(self, channel_count=2, sample_width=2, framerate=44100, input_device_index=0):
        self.channel_count = channel_count
        self.sample_width = sample_width
        self.framerate = framerate
        self.input_device_index = input_device_index

    def open(self):
        assert self.sample_width == 2
        if self.sample_width == 2:
            FORMAT = pyaudio.paInt16

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()

        # Open input stream, 16-bit mono at 44100 Hz
        # Ace Tree's device_index is 0, others' may be differ
        self.stream = self.p.open(
            format = FORMAT,
            channels = self.channel_count,
            rate = self.framerate,
            input_device_index = self.input_device_index,
            input = True
        )

    def read(self, time):
        """
        time: seconds
        """
        frames = self.stream.read(self.framerate * time)
        return io.parse(
            frames,
            channel_count=self.channel_count,
            sample_width=self.sample_width
        )

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


class Context(object):

    def __enter__(self, *args, **kargs):
        self.m = Microphone(*args, **kargs)
        self.m.open()
        return self.m

    def __exit__(self, *args, **kargs):
        self.m.close()


def open_microphone(*args, **kargs):
    return Context(*args, **kargs)
