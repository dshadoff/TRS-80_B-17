# TRS-80_B-17 Disassembly Folder

Disassembly of the 500-baud pre-loader for reading tapes written by the B-17 cassette software
for the TRS-80 Model I

## Introduction

I was able to locate some tapes I had created using B-17 back in the early 1980s,
and wanted to investigate the recording format, and how it was superior to the
native TRS-80 format without requiring any special hardware.

I played the cassette recordings into Audacity, which captured them at 44.1KHz
(however I used mono).  For there, I used Knut Roll-Lund's **excellent** WAV2CAS utility
to detect the contents of the 500-baud header information.
[See Knut Roll-Lund's webpage for more details on the utility](https://knut.one/wav2cas.htm)

A more in-depth analysis of the B-17 format can be found [HERE](Theory_of_Operation.md).


## Overview

I had two different versions of the B-17 System tape - one for 16K systems, and one for 48K systems.

I intend to disasemble and comment all of the other programs, and to draw attention to any differences
between the base 16K version and the later 48K version.

On the B-17 cassettes, there were three programs included:
1. B-17 Main System, which added LOAD, SAVE, GET, and PUT commands to BASIC.
   - Disassembly not yet available
2. B-17 System Module, which was able to transform binary programs into self-loading
B-17 format by prepending a B-17 loader at 500 baud.
   - [Disassemblies of the program HERE](System_Module), calling out changes between 16K and 48K (later) versions.
   - [Disassemblies of the Preloader HERE](Preloader), the preloader which is prepended to programs output by the System Module, calling out changes between 16K and 48K (later) versions.
3. B-17 Tape Certification Program, which was intended to test and validate cassettes for use with B-17.
   - [Disassembly HERE](Tape_Certification_Program), no difference between 16K and 48K versions.


