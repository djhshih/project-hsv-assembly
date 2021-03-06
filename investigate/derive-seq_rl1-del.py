#!/usr/bin/env python3

# Modify reference sequences based on known structural variants

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna

ref_fasta = "../ref/hsv/hsv_lacz-ins.fasta"
out_fasta = "../ref/hsv/hsv_lacz-ins_rl1-del.fasta"

contig = "GU734771.1.FA6"
#g.576_1527, g.124670_125621
# second coordinates need to be incremented by previous lacZ insertion
# of 3089 bases (replacing 1 base)
insert_size = 3089 - 1
regions = [(576 - 1, 1527), (124670 - 1 + insert_size, 125621 + insert_size)]

# read reference fasta
ref = SeqIO.to_dict(SeqIO.parse(ref_fasta, "fasta"))[contig]

# deletion target regions
out_seq = ref.seq[:regions[0][0]] + ref.seq[regions[0][1]:regions[1][0]] + ref.seq[regions[1][1]:]

print(ref.seq[:10])

# deleted sequence
print(ref.seq[(regions[0][0]):(regions[0][1])])
print(len(ref.seq[(regions[0][0]):(regions[0][1])]))

# deleted sequence
print(ref.seq[(regions[1][0]):(regions[1][1])])
print(len(ref.seq[(regions[1][0]):(regions[1][1])]))

# check that sequence created by deletion breakpoints exist
print(out_seq.find("TCCCAGGTAACCCTTGTTCCGCTTCCCGGTA"))
#                   uuuuuuuuuuudddddddddddddddddddd
print(out_seq.find("GGAAGCGGAACAAGGGTTACCTGGGACTGTGC"))
#                   uuuuuuuuuuuuuudddddddddddddddddd

# output modified sequence
out_record = SeqRecord(out_seq,
    id = contig + ".G207",
    description = "Human herpesvirus 1 strain G207, derived from strain FA6, with {contig}:{s1}_{e1}del and {contig}:{s2}_{e2}del".format(
        contig = contig,
        s1 = regions[0][0] + 1,
        e1 = regions[0][1],
        s2 = regions[1][0] + 1,
        e2 = regions[1][1]
    )
)
SeqIO.write(out_record, out_fasta, "fasta")

