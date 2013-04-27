# Waveutil

Just some wave (`.wav`) file related utilities.

## Installation

```
pip install git+https://github.com/Answeror/waveutil
```

## Dependencies

`numpy`, `nose`(for unit test).

## Testing

Under project root:

```
nosetests
```

Tested on Python `2.7.1` and `3.2.3`.

## Usage

### Matlab style IO

```python
from waveutil.io import waveread, wavewrite

# work for both filename and file object
frames, framerate = waveread('foo.wav')
# default frame rate is 44100
wavewrite('bar.wav', frames, framerate)
```
