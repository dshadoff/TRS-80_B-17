# TRS-80_B-17 Disassembly Folder

Disassembly of the 500-baud pre-loader for reading tapes written by the B-17 cassette software
for the TRS-80 Model I

## Overview

I was able to locate some tapes I had created using B-17 back in the early 1980s,
and wanted to investigate the recording format, and how it was superior to the
native TRS-80 format without requiring any special hardware.

I played the cassette recordings into Audacity, which captured them at 44.1KHz
(however I used mono).  For there, I used Knut Roll-Lund's **excellent** WAV2CAS utility
to detect the contents of the 500-baud header information.
[See Knut Roll-Lund's webpage for more details on the utility](https://knut.one/wav2cas.htm)

In the near future, I plan to write a program in Python to be able to decode WAV files and
display output of the data contained therein.


## Results - Header

I had fed WAV2CAS a sound file of a B-17-encoded game from the early 1980s, and
WAV2CAS was easily able to decipher the following information from the header:

* NAME = PATROL
* Load Block 1: 2 bytes at 0x401E (pointing to address 0x4300), as an auto-start
* Load Block 2: Block from 0x4300 to 0x43EB, the "B-17 Loader" 
* Entry point: 0x0000 (not used)

WAV2CAS then tried to identify follow-on data which was not correct, as the following data was
encoded in B-17 format.

Here is what WAV2CAS showed as the contents for Load Block 2:
![B-17_loader_preamble.JPG](B-17_loader_preamble.JPG)

I then hand-entered this data into a binary file [HERE](B-17_loader.bin), and used MAME's "unidasm"
program to disassemble the contents.

[The full disassembly is here](B-17_loader_disassembly.txt)




