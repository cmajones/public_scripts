#!/usr/bin/env python
from __future__ import division
from string import maketrans
#needed for at calc
#from calculate_at import calculate_at #not used anymore, this was added to the class

#from primer_excersive import * #not used anymore, this was added to the class
###################################################################################################

# make a class to add the primer info

class Primerrecord(object):
    """
    class for the primer record    
    """

    def __init__(self, primer_info, orientation, coordinate,
                 sequence):
        "always need this at start of class"
        #we dont need to specify self.at as we let python work this
        #out for itself based on the sequence info
        self.primer_info = primer_info
        self.orientation = orientation
        self.coordinate = coordinate
        self.sequence = sequence

    def count_at(self):
        a_count = self.sequence.count('A') 
        t_count = self.sequence.count('T')
        return a_count + t_count

    def count_gc(self):
        return len(self.sequence) - self.count_at()

    def get_AT(self):
        #this using the self.sequence to caluculate the at
        length = len(self.sequence)       
        at_content = self.count_at() / length 
        return at_content

    def melting_temp(self):
        """returns the melting temperature as estimated by
        http://www.sigmaaldrich.com/technical-documents/articles/biology/oligos-melting-temp.html
        the result will be a floating point number
        """
        #get formula to work out melting temp Tm = 2degree(A=T) + 4degree (G=C)
        self.melting_temp = ( 2*self.count_at() ) + ( 4*self.count_gc() )
        return self.melting_temp

    def is_palindromic(self):
        return self.sequence == reverse_complement(self.sequence)

    def mismatches(self):
        """ When passed a str(Bio.Seq seq), representing a nucleotide sequence,
        treats it as a short inverted repeat, and returns the number of 
        mismatched compared to its reverse complement for half the length
        of the sequence
        """
        #Ignores ambiguous letters like D
        complement_trans_table = maketrans("ACGTacgt", "TGCAtgca")
        #assert half_len == len(seq)/2 #TODO - for testing, this is SLOW!
        half_len = int(len(self.sequence)/2)
        #Want to use the python string's translate method to map A->T etc.
        second_half_seq_comp = self.sequence[-half_len:].translate(complement_trans_table)
        mismatches = 0
        for i in range(half_len) :
            if self.sequence[i] != second_half_seq_comp[-i-1] :
                mismatches += 1
        return mismatches

#assert 0 == count_mismatches("AAAAATTTTT", 5)
#assert 5 == count_mismatches("AAAAACCCCC", 5)


###################################################################################################

def complement(DNA):
    """function to work out the complement
    of a DNA seq"""
    DNA = DNA.upper()
    DNA_1 = DNA.replace("A", "t")
    DNA_2 = DNA_1.replace("T", "a")
    DNA_3 = DNA_2.replace("C", "g")
    complement = DNA_3.replace("G", "c")
    #print complement
    return complement.upper()

def reverse_complement(DNA):
    """function to work ou the rev compl
    this call the complim function"""
    compl = complement(DNA)
    return compl[::-1]

def all_possible_primers(DNA, k):
    """function to iterate over a DNA seq using K slices
    and return up to halfway the forward primer,
    and if over halfway along the DNAseq return the rev compl
    for the REV primer"""
    half_way = int(len(DNA)/2)+1
    for i in range(len(DNA.upper()) - k):
        kmer = DNA[i:i+k]
        if (i+k/2) < half_way:
            info = 'F' + str(i)
            orientation = 'FOR'
            coordinate = i+k
            #CLLAAASSSS
            # this assigns the info to variable, which then adds it to the class record
            p = Primerrecord(info, orientation, coordinate, kmer)
            yield p
        else:
            info = 'R' + str(i/2)
            orientation = 'REV'
            coordinate = i+k
            # this assigns the info to variable, which then adds it to the class record

            p = Primerrecord(info, orientation, coordinate, reverse_complement(kmer))
            yield p

            
###################################################################################################
    
"""
working with classes:

to iterate through to output from the generator:

first_primer = primer_list.next()

>>> first_primer
<__main__.Primerrecord object at 0x034DB8D0>

>>> first_primer.sequence
'ACGTGCATGCATGCA'

To call the class get the AT content of the sequence - 
>>> first_primer.get_AT()
0.4666666666666667

"""

###################################################################################################
#run the code

DNA ="ACGTGCATGCATGCATGCATTTGATAGATGTAGACGATGCATGCATGCATGCATGC"
DNA = DNA.upper()


#this one breaks the code due to non nucleotide base. 
#DNA ="ArCGTGCATGCATGCATGCATTTGATAGATGTAGACGATGCATGCATGCATGCATGC"

list_of_all_possible_bases = ["A", "T", "C", "G", "N"]

count = 0
for i in DNA:
    count = count+1
    assert i in list_of_all_possible_bases, "found a base that is not a nucleotide base, %s at position %d" %(i, count)


# add list infront of the generator expression to convert to a list
primer_list= list(all_possible_primers(DNA, k=15))


#make list of left and right primers
Forward_primer_list = []
Rev_primer_list = []

# way to iterate through the class object
print "#primer_info\tcoordinate_in_seq\tprimer_sequence\tAT_content\tMelting_temp\tPalindromic_mismatches\tpercentage_non_palidromic"

for i in primer_list:
    NOTES = ""
    if i.is_palindromic():
        NOTES = "IS_PALINDROMIC"

    #print "mismatches = ", i.mismatches()
    percentage_non_palidromic = 100*(i.mismatches()/float(len(i.sequence)))
    at = 100*(i.get_AT())
    print "%s\t%d\t%s\t%.1f\t%d\t%d\t%.1f\t%s" %(i.primer_info, i.coordinate, i.sequence, at,i.melting_temp(),\
                                              i.mismatches(), percentage_non_palidromic, NOTES)
    # get specific bits of info from the class by variable.class_field
    #print i.primer_info
    if i.primer_info.startswith("F"):
        Forward_primer_list.append(i)
    else:
        Rev_primer_list.append(i)
    #print('at content is : ' + str(i.get_AT()))
    #print primer_data.primer_info

#print primer_data.primer_info
#print Forward_primer_list





    
