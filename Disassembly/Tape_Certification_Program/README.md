# TRS-80_B-17 Tape Certification Disassembly

Disassembly of the "Tape Certification Program" for the B-17 cassette software
for the TRS-80 Model I, included as the third program on the B-17 cassette.

## Overview

On the B-17 cassettes, there were three programs included:
1. B-17 Main System, which added LOAD, SAVE, GET, and PUT commands to BASIC.
2. B-17 System Module, which was able to transform binary programs into self-loading
B-17 format by prepending a B-17 loader at 500 baud.
3. B-17 Tape Certification Program, which was intended to test and validate cassettes for use with B-17.

## Tape Certification Program

This program prompts the user with text, requesting the user to set up a cassette to be tested,
then the user presss ENTER, and the program writes data until the user hits ENTER again, at which
point the program prompts the user to reset the cassette to play, and press ENTER once more,
and the program reads back the data and verifies that it is readable.  The program will write
and verify multiple cassettes if desired.

There were no differences between the version supplied on the original cassette intended for
16B systems, and the "version 3" cassette intended for 48KB systems, except the filename:
* The 16KB version used "TCP   " as the filename
* The 48KB version used "B17   " as the filename


## Preparation

I took the data from the CAS file, and amended it to remove the block markers, converting this data into a
binary file [HERE](Tape_Certification.bin), and used MAME's "unidasm" program to disassemble the contents.


## High-Level Analysis

The program is quite straightforward, and is largely text.

For the "write" phase, the program writes 256 bytes of $00 as a leader, and then writes
continuously increasing byte values ($01, $02, ..., $FE, $FF, $00, ...) until the user
presses the ENTER key.

For the "verify" phase, the program reads and ignores the first 80 bytes, and then reads
bytes until it identifies a non-zero value. It then reads continuously, verifying that the
values read are continuously increasing as they were in the write phase, and stops when either:
1. The user presses ENTER
2. The value read doesn't match the expected value, at which point an error message is displayed.

[The full, commented disassembly is here](Tape_Certification_disassembly.txt)
