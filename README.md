# TRS-80_B-17
Information about ABS Suppliers' B-17 Software-based Tape System for the TRS-80 Model I.

## Introduction

In 1980, The TRS-80 Model I computer was capable of 500 baud cassette storage
from its Level II BASIC ROM.  This was quite slow (although not as slow as the
250 baud in its Level I BASIC ROM)

While floppy disks were available - and were also much faster than cassette - they
required the additional purchase of an Expansion Interface as well as at least one
floppy drive; the cost of these two things totalled more than the orgiinal computer,
so many people couldn't justify such a cost.

As a result, there were multiple companies who created many different ways of
improving cassette I/O speed. ABS Suppliers was one such company, with their B-17
software.

## Overview

The B-17 software was released, which reportedly improved cassette I/O speeds to 1700
baud - an over 3-fold improvement over base Model I speeds.

When the Model 3 was released, it had tape speeds of 1500 baud, which was close to B-17
speed, and probably played a role in reducing the market size and lifespan of the B-17
software. But for the Model I users, this was an inexpensive way to achieve higher data
rates and satisfied a number of people.

In order to save programs at the higher data rate, a utility program was required, but
B-17 was unique in that the utility was **NOT** required for loading most programs - when saving
files, B-17 would automatically save a pre-loader at 500 baud which, without any user
invovlement, would auto-start, and load the 'payload' program at 1700 baud. So, the program
load could be started in the usual way, loading the loader which would automatically start,
and load the remainder of the program at high speed.  Seamlessly.

Surprisingly, this pre-loader required less than 256 bytes of storage !

## This Repository

In this repository, I aim to recover as much information as possible about this software
and how it functioned - for users, historians, and researchers wishing to understand
the technology of the late 1970s and early 1980s.

### [Cassette](Cassette) Folder

In this folder, I will archive B-17 related software recordings I can locate.

Where possible, I will also try to locate B-17 format recordings so that they can also
be analyzed.

Commented disassemblies may follow at some point for any programs within the B-17 system,
including the pre-loader (such disassemblies will reside in the Disassembly folder).


### [Documents](Documents) Folder

In this folder, I will archive any of the documents I can find which describe the software
and its usage:
- Usage instructions
- Advertising materials
etc.

### [Disassembly](Disassembly) Folder

In this folder, I will include information about disassemblies of the pre-loader and
other software, as I am able.

### [Tools](Tools) Folder

In this folder, I will use the documentation found in any documents and disassemblies of B-17
pre-loaders and programs, in order to be able to read B-17 recordings on modern computers.


