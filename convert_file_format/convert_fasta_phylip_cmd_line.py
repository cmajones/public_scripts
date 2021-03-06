""" Title: Convert fasta file to Phylip for use with codonPhyml
"""

#imports
from Bio import AlignIO
from Bio.Alphabet import IUPAC, Gapped
from Bio import SeqIO
from Bio import AlignIO
from Bio.Alphabet.IUPAC import unambiguous_dna, ambiguous_dna
from Bio.Alphabet import IUPAC, Gapped
import os
from sys import stdin,argv
import sys
from optparse import OptionParser


script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'Phylip_files')
try:
    os.makedirs(dest_dir)
except OSError:
    print "already exists"

#this file converts an aligned fasta file and converts to a phylip  file
################################################################################
###############################################################################
def convert_files(indirectory, filename_endswith):
    for filename in os.listdir(indirectory):
        if filename.endswith(filename_endswith):
            #print filename
            #full_path_to_file = "%s/%s" (indirectory, filename)
            #full_path_to_file = os.path.join(filename)
            alignment = AlignIO.read(open(filename), "fasta", alphabet=Gapped(IUPAC.ambiguous_dna))
            outfile = "./Phylip_files/%s.phy" %(filename[:-6])
            AlignIO.write(alignment, outfile, "phylip")
    return "finished"

##def convert_files(indirectory, filename_endswith, outfolder):
##    for filename in os.listdir("./duplicates_removed"):
##        if filename.endswith("cds_aligned_refined.fasta"):
##            alignment = AlignIO.read(open(filename), "fasta", alphabet=Gapped(IUPAC.ambiguous_dna))
##            outfile = "./Phylip_files/%s.phy" %(filename[:-6])
##            print outfile
##            out_file_write = open(outfile, "w")
##            out_file_write.write (alignment.format("phylip-relaxed"))
##    return finished
################################################################################
###############################################################################

#convert_files(argv[1],argv[2])

if "-v" in sys.argv or "--version" in sys.argv:
    print "v0.0.1"
    sys.exit(0)


usage = """Use as follows:

converts

$ python convert_fasta_phylip_cmd_line.py -d directory_in (default current working directory) -e file_endswith_name

make sure you run this in the folder where the file is...


walk through a folder (-d) and anything that endswith -e will be converted to a phylip file

or to do one file. make -e your specific file
"""

parser = OptionParser(usage=usage)

parser.add_option("-d", dest="directory", default=default=os.getcwd(),
                  help="directory of the files you are wanting to go through")
parser.add_option("-e", "--ends", dest="endswith", default="ed.fasta",
                  help="Output filename",
                  metavar="FILE")




(options, args) = parser.parse_args()

directory_in = options.directory
file_endswith = options.endswith

convert_files(directory_in, file_endswith)
