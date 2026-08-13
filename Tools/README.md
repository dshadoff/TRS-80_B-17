# TRS-80_B-17 Tools Folder

Tools for reading tapes written by the B-17 System for the TRS-80 Model 1

## Overview

I was able to locate some tapes I had created using B-17 back in the early 1980s,
and wanted to investigate the recording format, and how they were able to improve
on the speed of the native TRS-80 format.

Based on a disassembly of the B-17 Loader program which is prepended to B-17 files,
I was able to piece together enough information to decode binary (machine language) files.

I have written a program in Python to be able to decode WAV files and display output
of the data contained therein.

You can find more information about the actual tape encoding in the
[Theory Of Operation](../Disassembly/Theory_of_Operation.md) file.

### Internals:

At a high level, the program has several major stages which it passes through; there
is considerable complexity so it may not currently read all files reliably. I will
continue to make adjustments to improve the reliability.

**MAJOR STEPS**
1. The python program reads the entire WAV file into memory and performs a rudimentary
analysis on it, to attempt to determine the appropriate threshold levels for a pulse.
   - All samples are placed into an array - as absolute values - to determine the distribution of levels.
   - The "realistic peak" values are determined based on having a certain percentage of samples at that range of values.
   - The "threshold value" is determined as 60% of the "realistic peak" value.
2. The file is initially read using TRS-80 Model 1 methods, searching for pulses spaced at 2ms apart, with or without an intermediate pulse in-between.
3. This segment of the audio file is validated against the loader in the [Disassembly](../Disassembly) folder.
4. Key information such as name, start address, length, and transfer address are extracted from the loader.
5. As the preloader validation completes, the program switches to decode B-17 data, including validating checksums.
6. The data is displayed as it is successfully extracted.

### Prerequisites:

The B-17 cassette recording must be recorded into a WAV file using an audio program;
something like 'Audactiy' will work fine.

The program currently only supports WAV files with the following parameters:
* 44100 samples per second (like a CD)
* Mono (1-channel) recording
* 16-bit samples

Files like this should be easy to create, but I may add support for stereo files in the future.

### Audio Data Treatment

In some rare cases, the audio data may be difficult to read as it isn't 100% consistent.
For prescriptive measures, see the [Audio Treatment](Audio_Treatment.md) file.

### Supported file types:

Currently, only B-17 BINARY files are supported, while I continue to investigate the capabilities of
the B-17 system.
* BINARY (SUPPORTED)
* BASIC (Not supported by these tools; B-17 support is not yet known)
* Other (Not yet fully investigated)

### Command-line:

The program can be invoked by using:
```
python readb17.py <filename>
```

### Output:

Currently, the program only displays the data it reads; it does not currently reformat
it into CAS or other data formats, but that should now be possible for BINARY files, as
the relevant data is decoded and displayed.


**HEADER INFORMATION is as follows:**
```
PCMNumber of channels: 1Sample Rate (Hz): 44100Bytes Per Second: 88200Bits Per Sample: 16 num_samples =  2226660max_val =  18818 Setting:general peak =  7424threshold    =  4454Filename = 'PATROL'B-17 Preloader resides at: 0x4300 through 0x43EA LOAD ADDRESS = 0x6300PROGRAM LEN  = 0x1D00XFER ADDRESS = 0x6300 Boot loader transition to B-17 format at sample number  407079```

This is followed by a data dump of the actual program data.

**PROGRAM DATA (excerpt)**:
```
 B-17 Payload Program:   0x6300: 31 00 55 CD 09 63 C3 6B 6A 21 00 3C 11 01 3C 01    1.U..c.kj!.<..<.0x6310: FF 03 36 80 ED B0 21 00 3C 06 40 36 BF 23 10 FB    ..6...!.<.@6.#..
     .
     .
     .
0x7FE0: 09 35 2C 41 9E 50 3C 03 F0 3C 02 98 3D 01 73 3E    .5,A.P<..<..=.s>0x7FF0: 03 04 3F 02 09 4C 44 09 4C 2C 32 35 35 B2 07 06    ..?..LD.L,255...--> CHECKSUM OK = 55END of FILE. samplenum =  2002898
```

