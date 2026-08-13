# Audio Treatment

Discussion of some of the possible issues with audio files from 1980's cassette tapes,
and how they may be dealt with.

## Overview

I wrote the "readb17.py" tool to read B-17 files, and it works well with recordings
that are quite homogeneous. However, while testing, I found that some recordings
may have oddities which may best be addressed by editing the audio file (not yet
incorporated into the program).

All descriptions below will be based on using Audacity as the tools to adjust and
make minor corrections.


## Example 1 - "END OF FILE FOUND"

For the first type of failure, I found the "readb17" script looked as follows:
```
python readb17.py B17_Track01_GALAXY.wav PCMNumber of channels: 1Sample Rate (Hz): 44100Bytes Per Second: 88200Bits Per Sample: 16 num_samples =  2552641max_val =  19221 Setting:general peak =  7296threshold    =  4377END OF FILE FOUND
```

The "END OF FILE FOUND" appeared before it had even recognized the B-17 header and filename.

This means that it probably didn't even locate the sync byte - so we look there.

Zooming in to a certain degree, we find that the start of audio looks like this:

![Treatment1_leadin_overview.png](../images/Treatment1_leadin_overview.png)

Two things to note here:
1. The immediate startup period is especially loud, but settles down into a normal range
2. Just before the 1.5 second mark, there is a strange wobble to the audio. There are actually a few more of these wobbles during the lead-in section.

This entire section - actually, up to the 4.87 second mark - is the leadin section of the 500 baud portion.
The bits are all identical until that 4.87 second mark, where the sync byte appears.  At that point, the waveform
will change to look something like this:

![Treatment1_leadin_sync.png](../images/Treatment1_leadin_sync.png)

In this case, the solution was simple - simply delete the roughly 1.6 seconds of bizarre-looking lead-in, since it's not important.
Just be sure not to delete anything after the sync byte (or even close to the sync byte).


