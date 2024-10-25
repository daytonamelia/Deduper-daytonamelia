#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="Read a single-end sorted sam file and remove all PCR-duplicates, retaining only a single copy of each read. A PCR-duplicate is a read with the same alignment position (same chromosome, 5’ start of read, strand) and same unique molecular index (UMI). A list of valid UMIs is provided by the user.")
    parser.add_argument("-f", "--file", help="Designates absolute file path to sorted sam file", type=str, required=True)
    parser.add_argument("-o", "--outfile", help="Designates absolute file path to deduplicated sam file", type=str, default="./daytondeduper_output.sam")
    parser.add_argument("-u", "--umi", help="Designates file containing the list of valid UMIs", type=str, required=True)
    return parser.parse_args()

def valid_umis(file: str, sep: str = "\n") -> set:
    """Takes an input text file of UMIs separated by an optional separator, parses and returns a set of valid UMIs."""
    return {line.strip() for line in open(file, "r")}

def workingreader(read: str) -> dict:
    """Parses a sam read for the QNAME, bitwiseflag, chromosome, position, and cigar string and places them in a list for usage."""
    # clean up read
    splitread = re.split(r"\s", read)
    cleanread = []
    for ele in splitread: # get rid of any empty places
        if ele != "":
            cleanread.append(ele)
    # make return dictionary
    working_read = {}
    working_read["qname"] = cleanread[0]
    working_read["bitflag"] = int(cleanread[1])
    working_read["chromosome"] = cleanread[2] # keep as string for X and Y
    working_read["position"] = int(cleanread[3])
    working_read["cigar"] = cleanread[5]
    return working_read

def umi_finder(qname:str) -> str:
    """Takes a valid input QNAME string, parses, and returns just the UMI at the end of the read."""
    split_qname = qname.split(":")
    return(split_qname[-1])

def softclip_corrector(strand: str, cigar: str, position: int) -> int:
    """Takes an input strand (+ = 1, - = 0), CIGAR string and position and corrects for soft-clipping. Returns the position corrected for soft clipping"""
    yuckcigar = re.split(r"(\d*[a-zA-z])", cigar)
    splitcigar = []
    for ele in yuckcigar: # get rid of any empty places that exist for some reason
        if ele != "":
            splitcigar.append(ele)
    if strand == "+": # positive strand
        for i, ele in enumerate(splitcigar):
            if i == 0 and "S" in ele:
                softclip = re.split(r"[a-zA-Z]", ele)
                return(int(position) - int(softclip[0]))
        return(position)
    else: # negative strand
        last_element = len(splitcigar) - 1
        ms = 0
        ds = 0
        ns = 0
        ss = 0
        for i, ele in enumerate(splitcigar):
            if "M" in ele:
                cigsplit = re.split(r"[a-zA-Z]", ele)
                ms = int(cigsplit[0])
            if "D" in ele:
                cigsplit = re.split(r"[a-zA-Z]", ele)
                ds = int(cigsplit[0])
            if "N" in ele:
                cigsplit = re.split(r"[a-zA-Z]", ele)
                ns = int(cigsplit[0])
            if "S" in ele and i == last_element:
                cigsplit = re.split(r"[a-zA-Z]", ele)
                ss = int(cigsplit[0])
        return (ms + ds + ss + ns + position - 1)

args = get_args()
umis = valid_umis(args.umi)
current_chromosome = "0" # initialize chromosome for checking chromosome change, needs to be string in case of X and Y

with open(args.file, "r") as rf, open(args.outfile, "w") as wf:
    for line in rf:
        line = line.strip()
        if line.startswith("@"): # header line - write to file
            wf.write(line)
            wf.write("\n")
        else: # line is a read - check validity
            working_read = workingreader(line)
            # print("------")
            # print(line)
            # print(working_read)
            if working_read["chromosome"] != current_chromosome: # we are in a new chromosome!
                working_chromosome = {}
                for umi in umis: # make a dictionary of empty sets for each umi and strand combo
                    working_chromosome[f"{umi}+"] = []
                    working_chromosome[f"{umi}-"] = []
                current_chromosome = working_read["chromosome"]
            umi = umi_finder(working_read["qname"])
            if umi not in umis: # check if umi is valid before we do any more work on this read
                continue
            if working_read["bitflag"] & 16 == 0:
                strand = "+" # strand is negative
            else:
                strand = "-" # strand is positive
            fiveprimeposition = softclip_corrector(strand, working_read["cigar"], working_read["position"])
            # print(f"\nChromosome: {working_read['chromosome']}")
            # print(f"UMI: {umi}")
            # print(f"Strand: {strand}")
            # print(f"Five Prime: {fiveprimeposition}")
            umiset = f"{umi}{strand}"
            if fiveprimeposition not in working_chromosome[umiset]:
                wf.write(f"{line}\n")
                working_chromosome[umiset].append(fiveprimeposition)
            
