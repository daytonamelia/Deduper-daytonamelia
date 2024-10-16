*Test Files:*

**Input:**
Header information from test.sam.
QNAME information is formatted as:
TEST : Retain or toss? : Is the sequence chromosome and position valid? : UMI valid or invalid? : Soft clipping or no? : Strand? : UMI

When sorted, reads are as follows:

***CHROMOSOME 1:***

Read 1: Valid sequence (UMI: AACGCCAT, CIGAR: no soft clipping)
Read 2-3: Read duped two times (UMI: AAGGTACG, CIGAR: one read with soft clipping - first read)
Read 4: Valid sequence (UMI: AACGCCAT, CIGAR: soft clipping)
Read 5: Invalid UMI (UMI: TTCGCCGA, CIGAR: no soft clipping)
Read 6: Invalid UMI (UMI: TTCGCCGA, CIGAR: soft clipping)
Read 7-9: Read duped three times (UMI: AACGCCAT, CIGAR: one read with soft clipping - second read)

***CHROMOSOME 2:***

Read 10: Read duped three times(UMI: AACGCCAT, CIGAR: two reads with soft clipping - first and third read)
Read 11: Valid sequence (UMI: AAGGTACG, CIGAR: soft clipping)
Read 12-14: Read duped two times with a valid sequence in the middle (UMI: All AGAGGAGA, CIGAR: All soft clipped)
