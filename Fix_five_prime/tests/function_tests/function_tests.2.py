def find_positive_next_ATG(transcriptome_record, position, strand):
    "function to find the next ATG"
    print ("start position = %d" % position)
    transcriptome_record= transcriptome_record[position:]
    if strand =="+":
        next_codon = ""
        start = 0
        end = 3
        for i in range(len(transcriptome_record)-60):
            start = start+3
            end = end+3
            print "start, end: ", start, end
            next_codon = transcriptome_record[start:end]
            print next_codon
            #next_codon = transcript.seq[position+3:position+6]
            if next_codon == "ATG":
                print "fucking yes"
                next_methionine = int(position+start)
                return next_methionine
                
 


c002 = """AAATATCTCGTCGTGCCGTACCGGATAGCGATTTTTAACAACATGGGAAGTTACAAATTG
TACCTGGCCGTCATGGCAATAGCTGTCATAGCTGCAGTTCAGGAAATTAGTTGCAAGGTT
CAGACTTCCGAACAGGACGATGATCAGGAAGGATATTACGATGATGAGGGAGGAGTGAAC
GATAATCAGGGAGAAGAGAACGATAATCAGGGAGAAGAGAACGATAATCAGGGAGAAGAG
AACGATAATCAGGGAGAAGAGAAGGAAGAAGTTTCCGAACCAGAGATGGAGCACCATCAG
TGCGAAGAATACAAATCGAAGATCTGGAACGATGCATTTAGCAACCCGAAGGCTATGAAC
CTGATGAAACTGACGTTTAATACAGCTAAGGAATTGGGCTCCAACGAAGTGTGCTCGGAC
ACGACCCGGGCCTTATTTAACTTCGTCGATGTGATGGCCACCAGCCCGTACGCCCACTTC
TCGCTAGGTATGTTTAACAAGATGGTGGCGTTTATTTTGAGGGAGGTGGACACGACATCG
GACAAATTTAAAGAGACGAAGCAGGTGGTCGACCGTATCTCGAAAACTCCAGAGATCCGT
GACTATATCAGGAACTCGGCCGCCAAGACCGTCGACTTGCTCAAGGAACCCAAGATTAGA
GCACGACTGTTCAGAGTGATGAAAGCCTTCGAGAGTCTGATAAAACCAAACGAAAACGAA
GCATTAATCAAACAGAAGATTAAGGGGTTAACCAATGCTCCCGTCAAGTTAGCCAAGGGT
GCCATGAAAACGGTTGGACGTTTCTTTAGACATTTTTAA""".replace("\n", "")

transcript = """CAAATATCTCGTCGTGCCGTACCGGATAGCGATTTTTAACAACATGGGAAGTTACAAATT
GTACCTGGCCGTCATGGCAATAGCTGTCATAGCTGCAGTTCAGGAAATTAGTTGCAAGGT
TCAGACTTCCGAACAGGACGATGATCAGGAAGGATATTACGATGATGAGGGAGGAGTGAA
CGATAATCAGGGAGAAGAGAACGATAATCAGGGAGAAGAGAACGATAATCAGGGAGAAGA
GAACGATAATCAGGGAGAAGAGAAGGAAGAAGTTTCCGAACCAGAGATGGAGCACCATCA
GTGCGAAGAATACAAATCGAAGATCTGGAACGATGCATTTAGCAACCCGAAGGCTATGAA
CCTGATGAAACTGACGTTTAATACAGCTAAGGAATTGGGCTCCAACGAAGTGTGCTCGGA
CACGACCCGGGCCTTATTTAACTTCGTCGATGTGATGGCCACCAGCCCGTACGCCCACTT
CTCGCTAGGTATGTTTAACAAGATGGTGGCGTTTATTTTGAGGGAGGTGGACACGACATC
GGACAAATTTAAAGAGACGAAGCAGGTGGTCGACCGTATCTCGAAAACTCCAGAGATCCG
TGACTATATCAGGAACTCGGCCGCCAAGACCGTCGACTTGCTCAAGGAACCCAAGATTAG
AGCACGACTGTTCAGAGTGATGAAAGCCTTCGAGAGTCTGATAAAACCAAACGAAAACGA
AGCATTAATCAAACAGAAGATTAAGGGGTTAACCAATGCTCCCGTCAAGTTAGCCAAGGG
TGCCATGAAAACGGTTGGACGTTTCTTTAGACATTTTTAATAAGCACGTCCATATAGACT
AGTACTATATACTATATATATATATACTTAAAACATAGTACATAAAGTGCAGATTTTCCA
AAAAAAATGTTGACCTAAAATCTCACTTCCTCAGCCCTCCGCAGTCATTTTCAGTTTTTT
GTACAGTACCATTACACATTAGGTATATCTGACTCACCACTCACCACGTTGTTCTTGCAA
TAAATATTATCGCTATTACTATTA""".replace("\n", "")

#print transcript[140:]

#transcript = "ATGzzzGGGTTTbbbATGeeeCC"

#broken_up_for_reading = "ATG NNN GGG TTT NNN ATG GGCCC"

start_pos = transcript.find(c002)

print "start_pso = ", start_pos

start = find_positive_next_ATG(c002,0,"+")
#print c002[start:]

print "next start = ", start
