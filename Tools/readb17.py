# READB17
#(c) 2026  David Shadoff
#
# Program to read B-17 encoded WAV files from TRS-80 Model 1
#
# Currently verified to read BINARY files
# Currently limited to 44100 Hz WAV files using Mono input (only one channel)


import os
import sys
import array as arr

POSITIVE            = 1
NEGATIVE            = -1
SAMPLE_BYTES        = 2
INCREASING          = 2
DECREASING          = 1
TRIGGER_DELAY       = 17   # number of samples of delay before next trigger (at 44.1KHz)
WAV_HDR_SIZE        = 44

TRS_BAUD            = 500   # baud rate
TRS_BITLEN          = 88    # samples per bit at 44100 (i.e. int(44100/500) )
TRS_BITLEN_MIN      = 79    # minimum length (10% shorter than TRS_BITLEN) 
TRS_BITLEN_MAX      = 97    # maximum length (10% longer than TRS_BITLEN)


B17_BIT0_MIN        = 20    # range of samples for bit 0 offset from sync bit
B17_BIT0_MAX        = 25
B17_BIT1_MIN        = 40    # range of samples for bit 1 offset from sync bit
B17_BIT1_MAX        = 48
B17_BIT2_MIN        = 63    # range of samples for bit 2 offset from sync bit
B17_BIT2_MAX        = 70
B17_BIT3_MIN        = 84    # range of samples for bit 3 offset from sync bit
B17_BIT3_MAX        = 93
B17_BIT4_MIN        = 106   # range of samples for bit 4 offset from sync bit
B17_BIT4_MAX        = 115
B17_BIT5_MIN        = 128   # range of samples for bit 5 offset from sync bit
B17_BIT5_MAX        = 137
B17_BIT6_MIN        = 150   # range of samples for bit 6 offset from sync bit
B17_BIT6_MAX        = 160
B17_BIT7_MIN        = 171   # range of samples for bit 7 offset from sync bit
B17_BIT7_MAX        = 183


# Tokens in loader template
#
TKN_LOADER_MSB    = 0x101     # base memory address for loader (i.e. 0x43 for 0x4300, 0x7d for 0x7d00)
TKN_PROGSTRT_LSB  = 0x102     # LSB of start of program load address
TKN_PROGSTRT_MSB  = 0x103     # MSB of start of program load address
TKN_PROGLEN_LSB   = 0x104     # LSB of size of block to load (bytes)
TKN_PROGLEN_MSB  =  0x105     # MSB of size of block to load (bytes)
TKN_PROGEXEC_LSB  = 0x106     # LSB of target execution address
TKN_PROGEXEC_MSB  = 0x107     # MSB of target execution address


#
# This is a copy of the B-17 file loader, with tokens placed in each of:
#  - The relocation base address locations
#  - The key changeable data areas (payload start, length, xfer addresses)
#
# It is to be used to validate whether the file under review is actually a B-17 file,
# and how to get to the start of the B-17 data
#
loader = arr.array('i', [
0x21, 0x58, 0x04, 0x22, 0x1e, 0x40, 0x21, 0x00, 0x00, 0x22, 0x3a, TKN_LOADER_MSB, 0x21, 0x14, 0x04, 0x22,
0x3c, TKN_LOADER_MSB, 0x3e, 0x5a, 0xcd, 0x3e, TKN_LOADER_MSB, 0xb9, 0x20, 0xfa, 0x21, TKN_PROGSTRT_LSB, TKN_PROGSTRT_MSB, 0x11, TKN_PROGLEN_LSB, TKN_PROGLEN_MSB,
0xcd, 0x29, TKN_LOADER_MSB, 0xaf, 0xd3, 0xff, 0xc3, TKN_PROGEXEC_LSB, TKN_PROGEXEC_MSB, 0xcd, 0x3e, TKN_LOADER_MSB, 0xcd, 0x7d, TKN_LOADER_MSB, 0xcd,
0xb4, TKN_LOADER_MSB, 0x71, 0x23, 0x1b, 0x7a, 0xb3, 0x20, 0xf0, 0xc9, 0x00, 0x00, 0x14, 0x04, 0xf5, 0xd5,
0x16, 0x08, 0x3e, 0x04, 0xd3, 0xff, 0xdb, 0xff, 0x17, 0x30, 0xfb, 0x06, 0x41, 0x10, 0xfe, 0x06,
0x09, 0x3e, 0x04, 0xd3, 0xff, 0xdb, 0xff, 0x17, 0x00, 0x38, 0x0c, 0x23, 0x2b, 0x10, 0xf6, 0x18,
0x0d, 0x2b, 0x2b, 0x23, 0x23, 0xf6, 0x00, 0xf6, 0x00, 0x10, 0xf6, 0x37, 0x00, 0x00, 0xcb, 0x19,
0x06, 0x1c, 0x10, 0xfe, 0x23, 0x00, 0x2b, 0x15, 0x20, 0xd5, 0xd1, 0xf1, 0xc9, 0xf5, 0xc5, 0xd5,
0xe5, 0x3e, 0x49, 0x32, 0x33, 0x3c, 0x3e, 0x4f, 0x32, 0x3f, 0x3c, 0x21, 0x3c, TKN_LOADER_MSB, 0x35, 0x20,
0x1e, 0x36, 0x14, 0x01, 0x0a, 0x00, 0x11, 0x34, 0x3c, 0x21, 0x35, 0x3c, 0xed, 0xb0, 0x21, 0x3d,
TKN_LOADER_MSB, 0x35, 0x20, 0x06, 0x36, 0x04, 0x3e, 0x3c, 0x18, 0x02, 0x3e, 0x2d, 0x32, 0x3e, 0x3c, 0xe1,
0xd1, 0xc1, 0xf1, 0xc9, 0xf5, 0xc5, 0xe5, 0x21, 0x3b, TKN_LOADER_MSB, 0x79, 0x86, 0x77, 0x2b, 0x35, 0x20,
0x26, 0xcd, 0x3e, TKN_LOADER_MSB, 0x79, 0x23, 0xbe, 0x28, 0x1e, 0x06, 0x0f, 0x21, 0xd8, TKN_LOADER_MSB, 0x7e, 0xcd,
0x33, 0x00, 0x23, 0x10, 0xf9, 0xc3, 0xcc, 0x06, 0x43, 0x48, 0x45, 0x43, 0x4b, 0x53, 0x55, 0x4d,
0x20, 0x45, 0x52, 0x52, 0x4f, 0x52, 0x0d, 0xe1, 0xc1, 0xf1, 0xc9
])


# Given file pointer, obtain sample number
#
def curr_sample_num():
    global fileptr
    
    sample = int((fileptr - WAV_HDR_SIZE)/SAMPLE_BYTES)
    return(sample)


def read_int4(ptr, mem_block):
    byte1 = mem_block[ptr]
    byte2 = mem_block[ptr+1]
    byte3 = mem_block[ptr+2]
    byte4 = mem_block[ptr+3]
    value = (byte4 * 16777216) + (byte3 * 65536) + (byte2 * 256) + byte1
    return(value)

def read_int2(ptr, mem_block):
    byte1 = mem_block[ptr]
    byte2 = mem_block[ptr+1]
    value = (byte2 * 256) + byte1
    return(value)

def read_abs2(ptr, mem_block):
    value = read_int2(ptr, mem_block)
    if value > 32767:
        value = 65536 - value
    return(value)

def get_nextsample(mem_block):
    global fileptr
    global filesize
    global lastval
    global inc_dec

    if (fileptr >= filesize):
        print("END OF FILE FOUND")
        exit()
    nextval = read_int2(fileptr, mem_block)
    if nextval > 32767:
        nextval = nextval - 65536
    if nextval > lastval:
        inc_dec = INCREASING
    else:
        inc_dec = DECREASING
        
    fileptr = fileptr + SAMPLE_BYTES
    lastval = nextval
    return(nextval)


def get_pulse(mem_block):
    global wavestart
    global fileptr
    global inc_dec
    global threshold
    global last_trig_sample
    
    while (True):
        val = get_nextsample(mem_block)
        curr_samplenum = curr_sample_num()
        if ((val > threshold) and (inc_dec == INCREASING) and ((curr_samplenum - last_trig_sample) > TRIGGER_DELAY)):
            last_trig_sample = curr_sample_num()
            return(1)
            
        
def get_trs_bit(mem_block):
    global fileptr

    initial_samplenum = curr_sample_num()
    get_pulse(mem_block)
    gap_samples = curr_sample_num() - initial_samplenum
    
    if (gap_samples > TRS_BITLEN_MAX):      # too long - this must be an error during read
        return(2)
        
    if (gap_samples > TRS_BITLEN_MIN):      # just right for 500 baud space
        return(0)
                                            # otherwise, too short to be a zero; but could be a '1' (intermediary pulse)
    get_pulse(mem_block)
    gap_samples_2 = curr_sample_num() - initial_samplenum
    if ((gap_samples_2 > TRS_BITLEN_MIN) and (gap_samples_2 < TRS_BITLEN_MAX)):
        return(1)                           # framing pulses are within spec, so it's a '1'
    else:
        return(2)                           # something is wrong

def get_trs_byte(mem_block):
    byte = 0
    for i in range (0, 8):
        curr_position = curr_sample_num()
        bit = get_trs_bit(mem_block)
        if (bit == 2):
            print("Error reading at ", curr_position)
            exit()
        byte = (byte << 1) + bit
    return(byte)
    
#
# entry condition is that start of the byte-sync pulse has already been encountered
#
def get_b17_byte(mem_block):
    byte = 0
    start_position = curr_sample_num()
    
    while(True):
        bit = get_pulse(mem_block)
        curr_position = curr_sample_num()
        rel_position = (curr_position - start_position)
        if (rel_position > 194):
# re-enable later for debug runs
#            print((curr_position - start_position))
            return(byte)
        if ((rel_position > B17_BIT0_MIN) and (rel_position < B17_BIT0_MAX)):
            byte = byte | 0x01
        elif ((rel_position > B17_BIT1_MIN) and (rel_position < B17_BIT1_MAX)):
            byte = byte | 0x02        
        elif ((rel_position > B17_BIT2_MIN) and (rel_position < B17_BIT2_MAX)):
            byte = byte | 0x04
        elif ((rel_position > B17_BIT3_MIN) and (rel_position < B17_BIT3_MAX)):
            byte = byte | 0x08
        elif ((rel_position > B17_BIT4_MIN) and (rel_position < B17_BIT4_MAX)):
            byte = byte | 0x10
        elif ((rel_position > B17_BIT5_MIN) and (rel_position < B17_BIT5_MAX)):
            byte = byte | 0x20
        elif ((rel_position > B17_BIT6_MIN) and (rel_position < B17_BIT6_MAX)):
            byte = byte | 0x40
        elif ((rel_position > B17_BIT7_MIN) and (rel_position < B17_BIT7_MAX)):
            byte = byte | 0x80
        else:
            print("B-17 read issue - can't determine bit number - gap = ", rel_position, " at sample number ", curr_position)
            exit()





file_stat = os.stat(sys.argv[1])
filesize = file_stat.st_size
print("filesize = {0:5} KB".format(int(filesize/1024)))

f = open(sys.argv[1], 'rb') 
memory = f.read()
f.close()
print("imported")

print("")

val = read_int2(20, memory)
if val == 1:
    print("PCM")
else:
    print("Only handles PCM files")
    exit()

val = read_int2(22, memory)
print("Number of channels:", val)
if (val != 1):
    print("Currently only handles mono samples")
    exit()

val = read_int4(24, memory)
print("Sample Rate (Hz):", val)
if (val != 44100):
    print("Currently only handles 44100Hz samples")
    exit()

val = read_int4(28, memory)
print("Bytes Per Second:", val)

val = read_int2(34, memory)
print("Bits Per Sample:", val)
if (val != 16):
    print("Currently only handles 16-bit samples")
    exit()

# first file position in the actual data
fileptr = WAV_HDR_SIZE

val = read_int2(fileptr, memory)
fileptr = fileptr + 2
polarity = POSITIVE
if val > 32767:
    val = val - 65536
    polarity = NEGATIVE

count = 1
wavestart = fileptr

# ------------------------------------------------------------------
# Try to determine appropriate levels for peak-to-peak max, pulse threshold, and noise floor
#
print(" ")
num_samples = int((filesize - fileptr)/SAMPLE_BYTES)
print("num_samples = ", num_samples)

a = arr.array('i', [0])
for i in range(1,65536):
    a.append(0)

#
# count number of samples with a specific value
#
for i in range(0, num_samples):
    ptr = WAV_HDR_SIZE + (i * SAMPLE_BYTES)
    val = read_abs2(ptr, memory)
    a[val] = a[val] + 1

#
# Determine maximum sample value (peak-to-peak max)
#
max_val = 0
for i in range(0, 65536):
    if (a[i] > 0):
        max_val = i
        
print("max_val = ", max_val)

#
# Determine distribution of number of samples, aggregating, counting in bands of 128 from peak-to-peak max
#
# Actual "pulse peak" will vary - even within same track
#   - but generally should be where roughly 7.5% of samples are contained (on B-17 tapes)
# (on test sample track, this level was the range from 7552 to 7680)
#
# Threshold cross should be a level about 60%-70% of whatever that level was
# (on test sample track, this would be the range from 4531 to 5286)
#
# Noise floor is where the "percentage of samples" jumps quickly in each group, near the zero sample value group
# (on test sample, this would be between 1024 and 1280, where numbers jump from 33.6% to 39.8%,
#     and each 128 group after that jumps roughly another 5%)
#
grp_cnt = 0
gen_peak = 0
for i in range(int(max_val/128), 0, -1):
    grp_base = i * 128
    if (grp_base>max_val):
        continue
    for j in range(0,128):
        grp_cnt = grp_cnt + a[grp_base + j]
        
    aggregate = int(1000*(grp_cnt/num_samples))/10
# enable later for debug runs
#    print("group ", grp_base, " = ", grp_cnt, " = ", aggregate,"%")
    if ((gen_peak == 0) and (aggregate > 7.5)):
        gen_peak = grp_base

threshold = int(gen_peak * 0.6)
print(" ")
print("Setting:")
print("general peak = ", gen_peak)
print("threshold    = ", threshold)


# NOTES:
#  A '1' on the input comparator will be signified by a sample which is:
#   1) rising
#   2) in excess of threshold value
#   3) at least 17.2 samples (at 44100Hz) past the initial trigger ( = 0.39 millisecobds ) 
#

lastval = 0
inc_dec = DECREASING
last_trig_sample = 0

#
# Search for 500 baud 0's leader first:
#
# Gap between one pulse and the next pulse should be between 1,800 and 2,270 microseconds
# (or between 80 and 100 samples at 44100 samples per second)
#

# seek out a train of at least 10 consecutive pulses in that range (still in the zero-train range)
#
last_fileptr = fileptr
for i in range(0, 300):      # first 300 pulses - discard these in order to synchronize on leader pulses
    pulse = get_pulse(memory)
    sample_gap = int((fileptr - last_fileptr)/SAMPLE_BYTES)
    if ((sample_gap > 80) and (sample_gap < 100)):
        bit_startsample = int((last_fileptr - WAV_HDR_SIZE)/SAMPLE_BYTES)
#        print("start = ", bit_startsample)
#    print("sample gap = ", sample_gap)
    last_fileptr = fileptr


#
# Now, continue reading leader until the sync btye appears (0xA5)
#
curr_byte_bits = 0
sync = False
while (sync == False):
    curr_position = curr_sample_num()
    bit = get_trs_bit(memory)
#    if (bit == 1):
#        print("First 1 bit at ", curr_position)
#        exit()
    if (bit == 2):
        print("Error reading at ", curr_position)
        exit()
    curr_byte_bits = (curr_byte_bits << 1) + bit
    if (curr_byte_bits == 0xA5):
#        print("Last bit of sync byte at ", curr_position)
        sync = True

print("")

if (get_trs_byte(memory) != 0x55):
    print("Not a machine language program")
    exit()

name1 = get_trs_byte(memory)
name2 = get_trs_byte(memory)
name3 = get_trs_byte(memory)
name4 = get_trs_byte(memory)
name5 = get_trs_byte(memory)
name6 = get_trs_byte(memory)
print("Filename = '{0:c}{1:c}{2:c}{3:c}{4:c}{5:c}'".format(name1,name2,name3,name4,name5,name6))

#---------------------------------------------------------------------------
# read the auto-start block: load the auto-start vector into address 0x401E
# this address will also be the base address of the preloader
#---------------------------------------------------------------------------

blk = get_trs_byte(memory)
if (blk != 0x3c):
    print("Error in block header - should be a 0x3C block")
    exit()

blklen = get_trs_byte(memory)
if (blklen != 0x02):
    print("Not a B-17 loader - block len (auto-start vector) = 0x{0:02X}; should be 0x02".format(blklen))
    exit()

cksum = 0
blkaddr_lsb = get_trs_byte(memory)
if (blkaddr_lsb != 0x1E):
    print("Not a B-17 loader - block addr (LSB) (auto-start vector) = 0x{0:02X}; should be 0x1E".format(blkaddr_lsb))
    exit()
cksum = cksum + blkaddr_lsb

blkaddr_msb = get_trs_byte(memory)
if (blkaddr_msb != 0x40):
    print("Not a B-17 loader - block addr (MSB) (auto-start vector) = 0x{0:02X}; should be 0x40".format(blkaddr_msb))
    exit()
cksum = cksum + blkaddr_msb

blkbyte1 = get_trs_byte(memory)
if (blkbyte1 != 0x00):
    print("Not a B-17 loader - auto-start address (LSB)  (auto-start vector) = 0x{0:02X}; should be 0x00".format(blkbyte1))
    exit()
cksum = cksum + blkbyte1

block_boot_base = get_trs_byte(memory)
cksum = cksum + block_boot_base
cksum = cksum & 0xFF

checksum = get_trs_byte(memory)
if (checksum != cksum):
    print("Checksum error on auto-start vector block - calculated = 0x{0:02X}; read = 0x{1:02X}".format(cksum, checksum))
    exit()

#-----------------------------------------------------------------------------
# read the preloader block: load the preloader into address starting at 0x??00
# where '??' is block_boot_base from the auto-start vector
#-----------------------------------------------------------------------------

blk = get_trs_byte(memory)
if (blk != 0x3c):
    print("Error in block header - block 2 should be a 0x3C block")
    exit()

blklen = get_trs_byte(memory)
if (blklen != 0xEB):
    print("Not a B-17 loader - block len (preloader) = 0x{0:02X}; should be 0xEB".format(blklen))
    exit()

cksum = 0
blkaddr_lsb = get_trs_byte(memory)
if (blkaddr_lsb != 0x00):
    print("Not a B-17 loader - block addr (LSB) (preloader) = 0x{0:02X}; should be 0x00".format(blkaddr_lsb))
    exit()
cksum = cksum + blkaddr_lsb

blkaddr_msb = get_trs_byte(memory)
if (blkaddr_msb != block_boot_base):
    print("Not a B-17 loader - block addr (MSB) (preloader) = 0x{0:02X}; should be 0x{1:02X}".format(blkaddr_msb, block_boot_base))
    exit()
cksum = cksum + blkaddr_msb

print("B-17 Preloader resides at: 0x{0:02X}00 through 0x{1:02X}EA".format(block_boot_base, block_boot_base))

print(" ")

#--------
# this should compare the complete loader against template
#--------
for i in range(0,0xEB):
    byte = get_trs_byte(memory)
    cksum = cksum + byte
#    print("0x{0:02X}".format(byte), end = " ")
    if (loader[i] == TKN_LOADER_MSB):
        if (byte != block_boot_base):
            print ("Byte ", i, " mismatch; bootblock = ", block_boot_base, " read from file = ", byte)
    elif (loader[i] == TKN_PROGSTRT_LSB):
        loadaddr_lsb = byte
    elif (loader[i] == TKN_PROGSTRT_MSB):
        loadaddr_msb = byte
    elif (loader[i] == TKN_PROGLEN_LSB):
        loadlen_lsb = byte
    elif (loader[i] == TKN_PROGLEN_MSB):
        loadlen_msb = byte
    elif (loader[i] == TKN_PROGEXEC_LSB):
        xferaddr_lsb = byte
    elif (loader[i] == TKN_PROGEXEC_MSB):
        xferaddr_msb = byte
    elif (loader[i] != byte):
        print ("Byte ", i, " mismatch; array = ", loader[i], " read from file = ", byte)
        exit()
#    if ((i & 0x0F) == 0x0f):
#        print(" ")

#print(" ")

print("LOAD ADDRESS = 0x{0:02X}{1:02X}".format(loadaddr_msb, loadaddr_lsb))
print("PROGRAM LEN  = 0x{0:02X}{1:02X}".format(loadlen_msb,  loadlen_lsb))
print("XFER ADDRESS = 0x{0:02X}{1:02X}".format(xferaddr_msb, xferaddr_lsb))

cksum = cksum & 0xFF

checksum = get_trs_byte(memory)
if (checksum != cksum):
    print("Checksum error on boot loader block - calculated = 0x{0:02X}; read = 0x{1:02X}".format(cksum, checksum))
    exit()

blk = get_trs_byte(memory)
if (blk != 0x78):
    print("Error in third block (not a transfer)")
    exit()

blkaddr_lsb = get_trs_byte(memory)
if (blkaddr_lsb != 0x00):
    print("Error in transfer address (LSB) = 0x{0:02X}; should be 0x00".format(blkaddr_lsb))
    exit()

blkaddr_msb = get_trs_byte(memory)
if (blkaddr_msb != 0x00):
    print("Error in transfer address (MSB) = 0x{0:02X}; should be 0x00".format(blkaddr_msb))
    exit()

print(" ")
curr_position = curr_sample_num()

print("Boot loader transition to B-17 format at sample number ", curr_position)

#
# Find B-17 Sync Byte (0x5A):
#
sync = False
while (sync == False):
    byte = get_b17_byte(memory)
    if (byte == 0x5A):
        sync = True

cksum = 0
counter = 0
start = (loadaddr_msb * 256) + loadaddr_lsb
num_of_bytes = (loadlen_msb * 256) + loadlen_lsb
end = start + num_of_bytes

blkstart = start
blkend = start + 255

while (blkend < end):
    address = (blkstart & 0xFFF0)
    string = ""
    if (address < blkstart):
        print("0x{0:04X}:".format(address), end=" ")
    while (address < blkstart):
        print("  ", end=" ")
        string= string + " "
        address = address + 1
    
    while (address <= blkend):
        if ((address & 0xF) == 0):
            print("  ", string)
            print("0x{0:04X}:".format(address), end=" ")
            string = ""
        nextbyte = get_b17_byte(memory)
        if (nextbyte < 0x20) or (nextbyte > 0x7f):
            string = string + "."
        else:
            string = string + chr(nextbyte)
        cksum = cksum + nextbyte
        print("{0:02X}".format(nextbyte), end=" ")
        
        address = address + 1

    if ((address & 0xF) != 0):
        for sp in range(0, 16 - (address & 0x0f)):
            print("  ", end=" ")
            
    print("  ", string)

    checksum = get_b17_byte(memory)
    cksum = (cksum & 0xFF)
    if (checksum == cksum):
        print("--> CHECKSUM OK = {0:02X}".format(checksum))
    else:
        print("--> CHECKSUM BAD = {0:02X}, read from file = {1:02X}".format(cksum, checksum))

    if ((address & 0x0f) != 0):
        print(" ")
 
    if (blkend == end):
        finished = True
    else:
        blkstart = blkstart + 256
        blkend = blkend + 256
        if (blkend > end):
            blkend = end

print("END of FILE. samplenum = ", curr_sample_num())
print(" ")

exit()
