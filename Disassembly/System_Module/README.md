# TRS-80_B-17 System Module Disassembly

Disassembly of the "System Module" for the B-17 cassette software
for the TRS-80 Model I, included as the second program on the B-17 cassette.


## Overview

On the B-17 cassettes, there were three programs included:
1. B-17 Main System, which added LOAD, SAVE, GET, and PUT commands to BASIC.
2. B-17 System Module, which was able to transform binary programs into self-loading
B-17 format by prepending a B-17 loader at 500 baud.
3. B-17 Tape Certification Program, which was intended to test and validate cassettes for use with B-17.

## System Module

This program prompts the user with text, requesting the user to set up a cassette with an
existing machine-language program file (recorded at 500 baud). When the user presses ENTER,
it loads the program into a buffer, checking for correct format, checksums, and to ensure that
the program is a contiguous block of memory.  It then prompts the user to setup a cassette to
save the program to, and it saves the program to tape at B-17 speeds, including a custom
pre-loader at 500 baud which automatically transitions to B-17 speed loading.

There were minor differences between the version supplied on the original cassette intended for
16B systems, and the "version 3" cassette intended for 48KB systems, but these haven't yet been 
ully explored.


## Preparation

I took the data from the CAS file, and amended it to remove the block markers, converting this data into
two binary files [HERE - the 4300 block](System_Module_Version3_16K_4300.bin), and
[HERE - the 7D00 block](System_Module_Version3_16K_7D00.bin). I then used MAME's "unidasm" program to
disassemble the contents.


## High-Level Analysis

The program is quite straightforward.

The two potential locations for the pre-loader are loaded into memory at their respective
memory locations, and I have not disassembled them as the pre-loader is disassembled and
commented separately.

For both the "read" and "write" phase, ROM calls are used for the 500-baud tape I/O.
For the B-17 write phase, it is a custom implementation with precision-timed loops for
timimng.

[The full, commented disassembly is here](System_Module_Version3_16K.txt)
