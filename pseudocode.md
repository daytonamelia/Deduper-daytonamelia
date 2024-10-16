*Deduper Psuedocode*

**Goal:**

Read a single-end sorted sam file and remove all PCR-duplicates, retaining only a single copy of each read. A PCR-duplicate is a read with the same alignment position (same chromosome, 5’ start of read, strand) and same unique molecular index (UMI). A list of valid UMIs is provided by the user.

**Examples:**

See unit-tests directory for test input and output sam files. See README.md for explanation of tests.

**High Level Functions:**

```
def valid_umis(file: str, sep: str = "\n") -> set:
"""Takes an input text file of UMIs separated by an optional separator, parses and returns a set of valid UMIs."""
    return: set object of valid UMIs
Test Input: file with contents: "AAA\tTTT\tCCC\tGGG"
Test Output: {AAA, TTT, CCC, GGG}
```

```
def umi_finder(qname: str) -> str:
"""Takes a valid input QNAME string, parses, and returns just the UMI at the end of the read."""
    return: a string object of just the UMI
Test Input: "NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC"
Test Output: "CTGTTCAC"
```

```
def softclip_corrector(cigar: str, position: int) -> int:
"""Takes an input CIGAR string and position and corrects for soft-clipping. Returns the position corrected for soft clipping"""
    return: an int object of the position taking into account the CIGAR string
Test Input: "1S70M", 101
Test Output: 100
```

**Algorithm:**

```
use valid_umis function to save our set of valid UMIs

open input sam file and output files:
    for each line in file:
    if line is a header:
        write to output

    else: # line is a read and we can check if its a valid read, a dupe, etc
        save read to memory as our "working read"
        pull out the chromosome (grab col 3)
            if the chromosome has changed from the previous "working read", then clear memory and make some sets to save information:
                make a set for each UMI (using valid_umis return) and strand configuration (+ or -). should have 96 * 2 = 192 sets for our test deduper.
            else:
                if the chromosome is the same from the previous "working read", then we can continue! we dont even have to save the chromosome to a separate variable! we might want to anyway though for debugging purposes.
        pull out the UMI (use umi_finder function)
        check if the UMI is valid. if not, just break out of this read and move onto the next as we won't want to write this yucky read.
            - or... write it to another file as an optional "invalid UMIs" file return ? hm...
        pull out the strand (use & 16 on the bitwise flag)
        check if theres a soft clipping flag in the cigar string, and pull out the corrected position (use softclip_corrector function)
        otherwise, just pull the position

        now we have the chromosome, strand, position, and UMI. we can determine if this read is in fact a PCR-duplicate
        we do this by checking if the position is in the corresponding UMI-strand set. this also saves some searching time.
            if it is in that set, this read is a PCR-duplicate! 
            if it is not in that set, then we save the position to the corresponding UMI-strand set and we write this read (with original start position) to our output file.
        clear working read to save memory and loop back to our next line!

Once this loop is done, we should have looped through the file only once and saved all of the non-duped reads to a file.
```
