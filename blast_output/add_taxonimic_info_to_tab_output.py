# Main title: Diamond/BLAST-12 column -tab-blast to taxonomic-id info

# can also work for 12 coloumn Blast output. - ALSO returns TOP-BLAST hits. Kingdom and Genus Distribution of these hits

#purpose: script to pare the tabular output from $ diamond view -f tab -o name.tab
# and get the description, tax id, species, kingdom information from NCBI taxonomy databse

#why: diamond is SOOO fast. But does not include tax id info in the database.

#author: Peter Thorpe September 2015. The James Hutton Insitute, Dundee, UK.

#imports
import os
import sys
from optparse import OptionParser
import datetime

####################################################################################################################

#this is how they are "described" in the catergories.dmp file
kingdom_dic ={"A": "Archaea", "B": "Bacteria", "E": "Eukaryota",
              "V": "Virus", "U": "Unclassified"}


def parse_NCBI_nodes_tab_file(folder):
    """this is a function to open nodes.dmp from the NCBI taxonomy
database and find the parent child relationship....returns a
disctionary for later use"""

    #open file - read.
    #nodes.dmp - this file is separated by \t|\t
    #empty dictionary to add to parent and child (keys,vals) to
    tax_dictionary = {}

    #nodes.dmp files goes: child, parent, etc
    #merged.dmp file goes: old, new
    #In both cases, can take key as column 0 and value as column 1
    for filename in ["nodes.dmp", "merged.dmp"]:
        with open(os.path.join(folder, filename)) as handle:
            for line in handle:
                tax_info = line.replace("\n", "\t").split("\t|\t")
                #first element
                parent = tax_info[1]
                #second element
                child = tax_info[0]
                #add these to the dictionary {parent:child}
                tax_dictionary[child]= parent
    #print tax_dictionary    
    return tax_dictionary


def taxomony_filter(tax_dictionary, tax_id_of_interst,final_tx_id_to_identify_up_to=None, tax_to_filter_out=None):
    """function to get a list of tax id of interest from the tax_dictionary
    which is produced in the parse_function (parse_NCBI_nodes_tab_file)
    nodes.dmp file. and merged.dmp. The tax id
    are added to a list for later use.

    This function walks up the tree to find the origin of the tax Id of interest. So if you wanted to find if the
    id of interest id metazoan, final_tx_id_to_identify_up_to=metazoan_tax_id ... if you want to to filter out all the
    hits in your phylmu of interest: tax_to_filter_out=arthropda_tax_id ,, for example.
    """
    tax_id_of_interst= tax_id_of_interst.strip()
    if tax_id_of_interst == "0":
        raise ValueError("0 is an unknown ID, going to assing 32644 to it instead")
        tax_id_of_interst ="32644" #assign an unknown tax_id
    if tax_id_of_interst == "N/A":
        raise ValueError("N/A as taxonomy ID")
    #get the "master" parent id
    parent = tax_dictionary[tax_id_of_interst]
    #print parent

    while True:
        #print "parent = ", parent, "\n"
        parent = tax_dictionary[parent]
        if tax_id_of_interst == "N/A":
            raise ValueError("N/A as taxonomy ID")
        #32630 is a synthetic organism
        if parent == "32630":#32630
            return "In_filter_out_tax_id"
            break            
        if parent == tax_to_filter_out:
            return "In_filter_out_tax_id"
            break
        if parent == final_tx_id_to_identify_up_to:
            #print "......................... im here"
            return True
        elif parent == "1":
            # Reached the root of the tree
            return False


def assign_cat_to_dic(categories):
    """function to add keys to a kingdom dic from catergory.dmp
    ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxcat.zip"""
    kingdom_tax_id = dict()
    with open(categories, "r") as handle:
        for line in handle:
            kingdom, tax_species, tax_id = line.rstrip("\n").split()
            kingdom_tax_id[int(tax_id)]= kingdom_dic[kingdom]
    return kingdom_tax_id

def tax_to_scientific_name_dict(names):
    """function to return a dict of speices info
    from 
    ftp://ftp.ncbi.nih.gov/pub/taxonomy/names.dmp"""
    tax_to_scientific_name_dict = dict()
    tax_to_common_name = dict()
    with open(names, "r") as handle:
        for line in handle:
            fields = [x.strip() for x in line.rstrip("\t|\n").split("\t|\t")]
            assert len(fields) == 4, "error, names files is not formatted as expected"
            # Four fields: tax_id, name_txt, unique name, name class
            taxid = int(fields[0])
            if fields[3] == "scientific name":
                tax_to_scientific_name_dict[taxid] = fields[1]
            elif fields[3] == "common name":
                tax_to_common_name[taxid] = fields[1]

    #print("Loaded %i scientific names, and %i common names"
          #% (len(tax_to_scientific_name_dict), len(tax_to_common_name)))
    return tax_to_scientific_name_dict, tax_to_common_name

def gi_to_description(gi_to_des):
    """function to return a dictionary of gi
    to description. The data needs to be generated into a tab file.
    This, along with other functions a re RAM hungry. export BLASTDB=/PATH_TO/ncbi/extracted
    blastdbcmd -entry 'all' -db nr > nr.faa
    python ~/misc_python/diamond_blast_to_kingdom/prepare_gi_to_description_databse.py
    """
    gi_to_description_dict = dict()
    with open(gi_to_des, "r") as handle:
        for line in handle:
            assert len(line.split("\t")) == 2, """Error, gi_to_des.tab file is not
    formatted as expected. It wants Gi_number\tdescription. See help on how to make
    this file, or use the shell script."""
            gi, description = line.rstrip("\n").split("\t")
            gi_to_description_dict[int(gi)] = description
    return gi_to_description_dict
    

def assign_taxon_to_dic(gi_taxid_prot):
    "function to convert taxon info to dictionary"
    gi_to_taxon = dict()
    with open(gi_taxid_prot, "r") as handle:
        for line in handle:
            gi, taxon = line.rstrip("\n").split()
            gi_to_taxon[int(gi)] = int(taxon)
    return gi_to_taxon

def read_diamond_tab_file(diamond_tab_output):
    """read in the tab file. Reads whole file into memeroy.
    Could be altered for more efficiency
    """
    with open(diamond_tab_output) as file:
        return file.read().split("\n")

def get_gi_number(line):
    """gi number are embeded in the second column
    so need to split it up to get to it"""
    gi_column = line.split("\t")[1]
    if not gi_column.startswith("gi"):
        raise ValueError('colomn 2 did not start with "gi", is this tab output formatted correctly') 
    return int(gi_column.split("|")[1])


#main function
def parse_diamond_tab(diamond_tab_output, path_files, gi_taxid_prot, categories, names, gi_to_des, outfile):
    "funtion to get tax id from dtaabse from diamond blast vs NR"
    taxon_to_kingdom = assign_cat_to_dic(categories)
    gi_to_taxon = assign_taxon_to_dic(gi_taxid_prot)
    tax_to_scientific_name_dic, tax_to_common_name_dic = tax_to_scientific_name_dict(names)
    gi_to_description_dict = gi_to_description(gi_to_des)
    tax_dictionary = parse_NCBI_nodes_tab_file
    # to run taxonmy filter: - remember this take strings as arguments 
    #taxomony_filter(tax_dictionary, tax_id_of_interst,final_tx_id_to_identify_up_to, tax_to_filter_out)
    
    file_out = open(outfile, "w")
    titles_of_coloumns = """#%s\n#qseqid	sseqid	pident	length	mismatch	gapopen	qstart	qend	sstart	send	evalue	bitscore	salltitles	staxids	scientific_name	scomnames	sskingdoms\n""" %(datetime.date.today())
    file_out.write(titles_of_coloumns)
    #get function to return a "\n" split list of blast file
    try:
        diamond_tab_as_list = read_diamond_tab_file(diamond_tab_output)
    except IOError as ex:
        print("sorry, couldn't open the file: " + ex.strerror + "\n")
        print ("current working directory is :", os.getcwd() + "\n")
        print ("files are :", [f for f in os.listdir('.')])
        sys.exit('cannot continue without a valid file')
    #iterate line by line through blast file
    for line in diamond_tab_as_list:
        if not line.strip():
            continue #if the last line is blank
        #ask function to get gi number
        gi_number = get_gi_number(line)
        #use dictionary to get tax_id from gi number

        # Most of the GI numbers will match, expect them to be in dict...
        try:
            tax_id = gi_to_taxon[gi_number]
        except KeyError:
            tax_id = "32644" #this is an unknown tax_id - this may or may not be the best one to use. NEED TO CHECK
            print (("tax_id for %s is not found in database, try updating your tax info file") %(gi_number))
            
        #TAXONOMY FILTERING - default is no!
        #taxomony_filter(tax_dictionary, tax_id_of_interst,final_tx_id_to_identify_up_to, tax_to_filter_out)
            
        #get kingdom
        try:
            kingdom = taxon_to_kingdom[tax_id]
        except KeyError:
            kingdom = kingdom_dic["U"]
        #get scientific names
        try:
            scientific_name = tax_to_scientific_name_dic[tax_id]
        except KeyError:
            scientific_name = ""
        #get common names
        try:
            common_name = tax_to_common_name_dic[tax_id]
        except KeyError:
            common_name = ""
        #get description  gi_to_description_dict[gi] = description
        try:
            description = gi_to_description_dict[gi_number]
        except KeyError:
            description = "" 

        #format the output for writing    
        data_formatted = "%s\t%s\t%s\t%s\t%s\t%s\n" %(line.rstrip("\n"), description,
                                                      tax_id,scientific_name,
                                                      common_name, kingdom)
        file_out.write(data_formatted)
    file_out.close()

    
##############################################################################################
# fucntion to get the top blast hits, kingdom and genus distribution of these. They
# are not called by the main function above
##############################################################################################

def wanted_genes(blast_file):
    """function to retunr a list of wanted genes from file.
    This function is called by a function to get the first
    instance of a query to get the top hit. The function is slightly reduncant
    as it may not be eassential"""
    wanted = open(blast_file, "r")
    names = wanted.readlines()
    blast_data = [line.rstrip() for line in names
              if line.strip() != "" if not line.startswith("#")]
    wanted.close()
    #print "wanted_data :", blast_data
    return blast_data

def get_top_blast_hit_based_on_order(in_file, outfile,  bit_score_column="12"):
    "parse through file and get top hit. Prints to a file reduced info."
    blast_data = wanted_genes(in_file)
    bit_score_column = int(bit_score_column)-1

    got_list = set([])
    outfile_name = outfile+"_based_on_order_tax_king.tab"
    f = open(outfile_name, "w")
    for line in blast_data:
        name = line.split("\t")[0]
        #print name
        description = line.split("\t")[bit_score_column+1]
        line = line.rstrip("\n")
        if not name in got_list:
            wanted_info = "%s\n" %(line)
            f.write(wanted_info)
            got_list.add(name)
    f.close()

##############################################################################################
    
def get_genus_count(genus_dict, blast_line, sci_name_column="15"):
    """this function count the distribution of the genus for the top hit"""
    sci_name_column = int(sci_name_column)-1
    scinetific_name = blast_line[sci_name_column]
    try:
        genus = scinetific_name.split()[0]
    except:
        return genus_dict
    try:
        genus_dict[genus]+=1
    except:
        genus_dict[genus]=1
    return genus_dict


def get_to_blast_hits(in_file, outfile, bit_score_column="12",):
    """this is a function to open up a tab file blast results, and
    produce the percentage of kingdom blast hit based on the top
    blast match"""
    get_top_blast_hit_based_on_order(in_file, outfile, bit_score_column)
    #open files, read and write.
    blast_file = open (in_file, "r")
    out_file = open(outfile,"w")
    bit_score_column = int(bit_score_column)-1

    
    #set of blast_file_entry gene names
    blast_file_entry_Genes_names = set([])
    kingdoms = set("")

    # dictionary of all the kingdoms in our blast file
    kingdoms_handles_counts = {'Eukaryota':0, 'N/A':0, 'Bacteria;Eukaryota':0, \
                               'Archaea;Eukaryota':0, 'Virus':0, 'Bacteria;Viruses':0,\
                               'Eukaryota;Viruses':0, 'Archaea':0, 'Bacteria':0,\
                               'Unclassified':0}
    
    #this is out list of so called top matches which we will append and remove as applicable
    top_hits = []
    #current bit score value "to beat"
    current_bit_score = float(0.0)
    last_gene_name = ""
    last_blast_line = ""
    
    for line in blast_file:
        if line.startswith("#"):
            continue
        #print line
        blast_line = line.rstrip("\n").split("\t")
        #names of the query seq
        blast_file_entry_Genes = blast_line[0]
        #print blast_file_entry_Genes
        bit_score = float(blast_line[bit_score_column])
        kings_names = blast_line[-1]
        #print kings_names
        
        ##############################################################################
        #first block: if the names are the same, is the new bit score more?
        if blast_file_entry_Genes == last_gene_name:
            #print "im here"
            if bit_score > current_bit_score:
                #print "current_bit_score", current_bit_score
                current_bit_score = bit_score
                #print "current_bit_score", current_bit_score
                #remove the last entry if so and put the new one in
                del top_hits[-1]
                top_hits.append(blast_line)

                
        #############################################################################
        # second block: if the name is new, put it in the name set.
        # use this bit score as the new one to "beat"

        #print current_bit_score
        if not blast_file_entry_Genes in blast_file_entry_Genes_names:
            #print ".......should be first line"
            blast_file_entry_Genes_names.add(blast_file_entry_Genes)
            current_bit_score = bit_score
            top_hits.append(blast_line)

        ############################################################################
        # assign value to the variables for testing in the new batch of for loops
        
        last_gene_name = blast_file_entry_Genes
        last_blast_line = line
        
    genus_dict = dict()
    
    total_blast_hit_count = 0 
    for i in top_hits:
        genus_dict = get_genus_count(genus_dict, i)
        total_blast_hit_count = total_blast_hit_count+1
        king_name = i[-1]
        kingdoms_handles_counts[king_name]+=1
        new_line = ""
        for element in i:
            new_line = new_line+element+"\t"
            
        data_formatted = new_line.rstrip("\t")+"\n"
        out_file.write(data_formatted)



    #for blast_file_entry_Genes, bit_score, kings_names in top_hits:
        #print >> out_file, "%s\t%s\t%s" % (blast_file_entry_Genes, bit_score, kings_names)
        #kingdoms_handles_counts[kings_names]+=1

    print "Kingdom hit distribution of top hits = ", kingdoms_handles_counts
    print "number with blast hits =", total_blast_hit_count
    #print "genus distirbution =", genus_dict

    top_hits_out_king = open("kingdom_top_hits.out", "w")
    file_tile = "#top kingdom hit for %s\n" %(in_file)
    top_hits_out_king.write(file_tile)

    top_hits_out_genus = open("Genus_distribution_top_hits.out", "w")
    file_tile = "#Genus_of_top hits for %s\n" %(in_file)
    top_hits_out_genus.write(file_tile)

    for kingdom, count in kingdoms_handles_counts.items():
        data_form = "%s:\t%i\n" %(kingdom, count)
        top_hits_out_king.write(data_form)

    for genus, count in genus_dict.items():
        data_form = "%s:\t%i\n" %(genus, count)
        top_hits_out_genus.write(data_form)

    top_hits_out_king.close()
    out_file.close()
    top_hits_out_genus.close()
    
    return kingdoms_handles_counts





#############################################################################################################################################################


if "-v" in sys.argv or "--version" in sys.argv:
    print "v0.0.3"
    sys.exit(0)


usage = """Use as follows:

$ python Diamond_blast_to_taxid.py -i diamond_tab_output -t /PATH_TO/NCBI_gi_taxid_prot.dmp -c /PATH/To/categories.dmp
-n /PATH/To/names.dmp -d /PATH_TO_/description_database -o outfile.tab

        or


$ Diamond_blast_to_taxid.py -i diamond_tab_output -p /PATH_TO/FILES -o outfile.tab


This script opens up a diamond tab output (-i) and looks up the relavant tax_id info (-t), look up the kingdom (-c)
looks for the species names (-n), looks up the descrtiption of the blast hit (-d):

# NOTE: this will also work on standard blast output which does not have kingdom assignmnets.

    Prot to tax_id: ftp://ftp.ncbi.nih.gov/pub/taxonomy/gi_taxid_prot.dmp.gz).
    catergories file: ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxcat.zip
    speices names: ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz

all files need to be uncompressed

do the following:

    wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/gi_taxid_prot.dmp.gz
    gunzip gi_taxid_prot.dmp.gz

    wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxcat.zip
    unzip taxcat.zip

    wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
    tar -zxvf taxdump.tar.gz


To generate the gi_to_des.tab databse:
blastdbcmd -entry 'all' -db nr > nr.faa


python ~/misc_python/diamond_blast_to_kingdom/prepare_gi_to_description_databse.py

# Note: this return the top description in the NR discrition for each fasta file entry. This can be modified to return "all". But the file will be much larger and therefore require more RAM


    BLAST DATA we be returned as:

qseqid = Query Seq-id (ID of your sequence)
sseqid = Subject Seq-id (ID of the database hit)
pident = Percentage of identical matches
length = Alignment length
mismatch = Number of mismatches
gapopen = Number of gap openings
qstart = Start of alignment in query
qend = End of alignment in query
sstart = Start of alignment in subject (database hit)
send = End of alignment in subject (database hit)
evalue = Expectation value (E-value)
bitscore = Bit score
salltitles = TOP description of the blast hit
staxids = tax_id
scientific_name
scomnames = common_name
sskingdoms = kingdom


TOP BLAST HITS FINDER:
By default this script will find the top hits by two methods. 1) assuming order in BLAST out file 2) Explicitly looking for the BLAST entry with the greatest bit score per query.
Script will also return the distribution of the kindgom and genus for these top hits.



Some notes on using Diamond:


# script to get the latest NR database and NT database and make a diamond blastdatabse.


# to install diamond from source
export BLASTDB=/PATH/TO/ncbi/extracted


blastdbcmd -entry 'all' -db nr > nr.faa

/diamond-0.7.9/bin/diamond makedb --in nr.faa -d nr

diamond makedb --in uniprot_sprot.faa -d uniprot

diamond makedb --in uniref90.faa -d uniref90

covert output to tab:
$ diamond view -a diamond.daa -f tab -o name.tab


# warning: running to script uses a lot of RAM ~25GB. 

"""

parser = OptionParser(usage=usage)

parser.add_option("-i", "--in", dest="diamond_tab_output", default=None,
                  help="the tab output from diamond. use: $ diamond view -a diamond.daa -f tab -o name.tab",
                  metavar="FILE")

parser.add_option("-p", "--path", dest="path", default=os.getcwd(),
                  help="Directory containing relevant taxonomy/database files "
                       "(set by -t, -c, -n, -d). Default is the current working "
                       "directory. This is not used with the main input and output "
                       "filenames.")

parser.add_option("-t", "--taxid_prot", dest="gi_taxid_prot", default="gi_taxid_prot.dmp",
                  help="NCBI provided file gi_taxid_prot.dmp (from FTP site, "
                       "gi_taxid_prot.dmp.gz after unzipping). These file required file options can be left blank if -p is specified with a path to where all these can be found. If -p /PATH/ is specified python will look in the folder by default.",
                  metavar="FILE")
parser.add_option("-c", "--cat", dest="categories", default="categories.dmp",
                  help="NCBI provided kingdom catergories file categories.dmp "
                       "(from FTP site inside taxcat.zip).",
                  metavar="FILE")
parser.add_option("-n", "--names", dest="names", default="names.dmp",
                  help="NCBI provided names file names.dmp (from FTP site "
                       "inside taxdump.tar.gz",
                  metavar="FILE")
parser.add_option("-d", "--des", dest="gi_to_des", default="gi_to_des.tab",
                  help="""a databse of gi number-to-descrition. Generate either using the shell script or by the following:

    export BLASTDB=/PATH_TO/blast/ncbi/extracted

    # can only use protein databases with this program.
    blastdbcmd -entry 'all' -db nr > nr.faa
    python ~/misc_python/diamond_blast_to_kingdom/prepare_gi_to_description_databse.py
    """,
                  metavar="FILE")



parser.add_option("-o", "--out", dest="outfile", default="_tab_blast_with_txid.tab",
                  help="Output filename - default= infile_tab_blast_with_txid.tab",
                  metavar="FILE")




(options, args) = parser.parse_args()

def apply_path(folder, filename):
    """If filename is not absolute, assumed relative to given folder.

    Here filename is a relative path (does not start with slash):

    >>> apply_path("/mnt/shared/taxonomy", "names.dmp")
    '/mnt/shared/taxonomy/names.dmp'

    Here filename is already an absolute path, so no changes:

    >>> apply_path("/mnt/shared/taxonomy", "/tmp/ncbi/taxonomy/names.dmp")
    '/tmp/ncbi/taxonomy/names.dmp'
    
    """
    if os.path.isabs(filename):
        return filename
    else:
        return os.path.join(folder, filename)
# -i
diamond_tab_output = options.diamond_tab_output
#-t
gi_taxid_prot = apply_path(options.path, options.gi_taxid_prot)
# -c
categories = apply_path(options.path, options.categories)
#-n
names = apply_path(options.path, options.names)
#-d
gi_to_des = apply_path(options.path, options.gi_to_des)
# -p
path_files = options.path
#-o
outfile= options.outfile

#call the main function
parse_diamond_tab(diamond_tab_output, path_files, gi_taxid_prot, categories, names, gi_to_des, outfile)

# fucntion to get the top hits and the kingdom and genus distribution

top_hits_out = outfile+"top_blast_hits.out"
get_to_blast_hits(outfile, top_hits_out)


# more notes
"""############################################################################################
Some notes on using Diamond:


# script to get the latest NR database and NT database and make a diamond blastdatabse.


# to install diamond from source
export BLASTDB=/PATH/TO/ncbi/extracted


blastdbcmd -entry 'all' -db nr > nr.faa

/diamond-0.7.9/bin/diamond makedb --in nr.faa -d nr

diamond makedb --in uniprot_sprot.faa -d uniprot

diamond makedb --in uniref90.faa -d uniref90

covert output to tab:
$ diamond view -a diamond.daa -f tab -o name.tab


from stdin:
diamond makedb --in /dev/stdin -d tiny_from_stdin < tiny.faa
"""
