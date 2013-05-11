#!/usr/bin/env python
# -*- coding: utf-8 -*-

from waveutil import io
import wave
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
try:
    from StringIO import StringIO
except ImportError:
    # py3k
    from io import BytesIO as StringIO


def test_wavread():
    f = gen_test_wav()
    frames, framerate = io.wavread(f)
    assert_almost_equal(frames, [[0.5]], 3)
    assert_equal(framerate, 44100)


def test_wavwrite():
    frames = np.array([[0.5]])
    framerate = 44100
    f = StringIO()
    io.wavwrite(f, frames, framerate)
    f.seek(0)
    data, fs = io.wavread(f)
    assert_almost_equal(data, frames)
    assert_equal(fs, framerate)
    f = StringIO()
    io.wavwrite(f, data, fs)
    f.seek(0)
    frames, fs = io.wavread(f)
    assert_almost_equal(data, frames)


def gen_test_wav():
    f = StringIO()
    writer = wave.open(f, 'wb')
    writer.setnchannels(1)
    writer.setsampwidth(2)
    writer.setframerate(44100)
    writer.writeframes(np.array([32768 / 2]).astype(np.short).tostring())
    writer.close()
    f.seek(0)
    return f
