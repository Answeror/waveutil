#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: io
    :synopsis: Matlab like IO.

.. moduleauthor:: Answeror <answeror@gmail.com>

"""

import wave
import numpy as np


def parse(data, channel_count=2, sample_width=2):
    assert sample_width == 2
    data = np.fromstring(data, dtype=np.short)
    data.shape = -1, channel_count
    data = data / 32768.0
    return data


def wavread(f):
    """Just like ``wavread`` in Matlab.

    :param f: filename or file object
    :return: frames (range [-1,1]), framerate
    :rtype: (matrix, int)
    """
    reader = wave.open(f, 'rb')
    try:
        framerate = reader.getframerate()
        frame_count = reader.getnframes()
        channel_count = reader.getnchannels()
        sample_width = reader.getsampwidth()
        if sample_width != 2:
            raise RuntimeError('Sample width must be 2 byte.')
        byte_data = reader.readframes(frame_count)
    finally:
        reader.close()
    frames = np.fromstring(byte_data, dtype=np.short)
    frames.shape = -1, channel_count
    frames = frames / 32768.0
    return frames, framerate
    return parse(
        byte_data,
        channel_count=channel_count,
        sample_width=sample_width
    ), framerate


def wavwrite(f, frames, framerate=44100, nbits=16):
    """Just like ``wavwrite in Matlab.

    WAVWRITE(Y,FS,NBITS,WAVEFILE) writes data Y to a Windows WAVE
    file specified by the file name WAVEFILE, with a sample rate
    of FS Hz and with NBITS number of bits.  NBITS must be 8, 16,
    24, or 32.  Stereo data should be specified as a matrix with two
    columns.

    WAVWRITE(Y,FS,WAVEFILE) assumes NBITS=16 bits.
    WAVWRITE(Y,WAVEFILE) assumes NBITS=16 bits and FS=8000 Hz.

    Input Data Ranges
    The range of values in Y depends on the number of bits specified by NBITS
    and the data type of Y.  Some examples of valid input ranges based on the
    value of NBITS and Y's data type are listed in the tables below.

    If Y contains integer data:

        NBITS   Y's data type    Y's Data range          Output Format
       -------  ---------------- ---------------------   -------------
          8         uint8             0 <= Y <= 255         uint8
         16         int16        -32768 <= Y <= +32767      int16
         24         int32         -2^23 <= Y <= 2^23-1      int32

    If Y contains floating point data:

        NBITS   Y's data type    Y's Data range          Output Format
       -------  ---------------- ---------------------   -------------
          8     single or double   -1.0 <= Y <  +1.0        uint8
         16     single or double   -1.0 <= Y <  +1.0        int16
         24     single or double   -1.0 <= Y <  +1.0        int32
         32     single or double   -1.0 <= Y <= +1.0        single

    Note that for floating point data where NBITS < 32, amplitude values
    are clipped to the range -1.0 <= Y < +1.0.

    8-, 16-, and 24-bit files are type 1 integer PCM.
    32-bit files are written as type 3 normalized floating point.
    """
    # wrap list with 2d numpy.array
    frames = np.array(frames)
    #frames.shape = -1, 1

    writer = wave.open(f, 'wb')
    writer.setframerate(framerate)
    assert frames.ndim == 1 or frames.ndim == 2
    sample_count, channel_count = frames.shape
    writer.setnchannels(channel_count)
    if frames.dtype in (np.float, np.double):
        scaled = frames * 32768
    else:
        scaled = frames
    if nbits == 8:
        dtype = np.uint8
    elif nbits == 16:
        dtype = np.int16
    elif nbits == 24:
        dtype = np.int32
    elif nbits == 32:
        dtype = np.float32
    else:
        assert False
    writer.setsampwidth(nbits // 8)
    writer.writeframes(scaled.astype(dtype).tostring())
    writer.close()
