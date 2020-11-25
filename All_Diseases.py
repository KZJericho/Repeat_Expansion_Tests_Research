#distinguish between gene, chromosome, and WGS
#figure out how to interpret results
#test cases



import json

# Text loading and storing functions obtained from:
# cs.cmu.edu/~112/notes/notes-strings.html
def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

class Disease(object):
    
    # Initialize
    def __init__(self, name, chromosome, gene, patterns, thresholds):
        self.name = name
        self.chromosome = chromosome
        self.gene = gene
        self.patterns = patterns
        self.thresholds = thresholds # (M0,M1)
        self.results = {} # map a tagged gene to the result for this disease
        self.best_length = 0
        self.best_location = 0
        self.result = ""
    

    # txt is the text representing our genome
    # pats is a list of the patterns to look for
    def group_patterns_test(self, path = None, text = None):
        if path != None: 
            txt = read_file(path).replace("\n", "") # Assume a well formatted gene
        else: 
            txt = text
            
        # Used in group_patterns_test
        def my_mod(dividend, divisor):
            mod = dividend%divisor
            if mod < 0:
                return mod + divisor
            else:
                return mod
    
    
        # print("Testing for Group Patterns...", end = "")
    
        for pat in self.patterns:
            assert(len(pat) <= len(txt))
    
        pattern_length = len(self.patterns[0])
        text_length = len(txt)
        prime = 2971215073
    
        current_txt_hash = 0

        best_length = 0
        current_best_location = None
    
        current_length = 0
        current_location = None
    
        exponent = 1
        base = 256
        i = 0
    
        if pattern_length > text_length:
            return None
    
        #calculate exponent
        for i in range(pattern_length - 1):
            exponent = (base**(pattern_length-1))%prime
    
        # Create a dictionary of patterns mapped to their hashes
        pats_dictionary = {}
        for pat in self.patterns:
            pattern_hash = 0
            for i in range(pattern_length):
                pattern_hash = (base*pattern_hash + ord(pat[i]))%prime
            pats_dictionary[pat] = pattern_hash
        
        #calculate first hash   
        for i in range(pattern_length):
            current_txt_hash = my_mod((base*current_txt_hash + ord(txt[i])),prime)

        i = 0
        #rolling hash
        while i < (len(txt)):
            number_of_letters_rolling_over = 0 
            current_chunk = txt[i:i+pattern_length]
            for pat in self.patterns:
                pattern_hash = pats_dictionary[pat]
                if current_txt_hash == pattern_hash and current_chunk == pat:
                    current_length += 1  
                    current_location = i 

                    number_of_letters_rolling_over = pattern_length
                    break
        
            #record best lengths
            else:
                if current_length > best_length:
                    best_length = current_length
                    current_best_location = current_location - (pattern_length)*((current_length)-1)

                current_length = 0
                number_of_letters_rolling_over = 1 
        
            #re-hash
            if i + number_of_letters_rolling_over <= text_length - pattern_length:
                for j in range(number_of_letters_rolling_over):
                    current_txt_hash = my_mod((base*(current_txt_hash-ord(txt[i])*exponent) + ord(txt[i+pattern_length])),prime)
                    i += 1
            
                #in case of negative hash value
                if current_txt_hash < 0:
                    current_txt_hash = current_txt_hash + prime
            else:
                i += number_of_letters_rolling_over

        #record best lengths last time
        if current_length > best_length:
            best_length = current_length
            current_best_location = current_location - (len(pat))*((current_length)-1)
            
        # For each pattern, we track 
            
        self.process_results(best_length, current_best_location, path)
    
    
    def process_results(self, best_length, current_best_location, path):
        # Interpret location data with length, and use threshholds to determine disease status
        if best_length <= self.thresholds[0]:
            result = "Negative", best_length
        elif self.thresholds[0] < best_length < self.thresholds[1]:
            result = "Indeterminate", best_length
        else:
            result = "Positive", best_length
        # Tag current result with name of file that we ran on and store in results
        self.results[path] = result
    
    # For a given disease object, call this on a gene input and store the data in the object
    def test_on_genes(self, paths = None, texts = None, store_results = True):
        # Ok make sure to properly incorporate information about the type of sequence
        for path in paths:
            self.group_patterns_test(path = path)
        for text in texts:
            self.group_patterns_test(text = text)
        if store_results: self.result_to_json(path + "_result")

    def result_to_json(self, path):
        js = json.dumps(self.result)
        write_file(path, js)
        
    def result_from_json(self, path):
        js = read_file(path)
        results = json.loads(js)
        
        # Copy previous results into the curent disease object
        for result in results:
            self.results[result] = results[result]
        



#test for all diseases

#Diseases is a list of diseases duh
def all_sequences_test(Diseases, path = None, txt = None):
    for Disease in Diseases:
        Disease.group_patterns_test(path)
    for Disease in Diseases:
        print(Disease.name)
        for p in Disease.results: print(Disease.results[p])
        
    

if __name__ == "__main__":
    Disease_list = []
    
    DRPLA = Disease("DRPLA", "12", "ATN1", ["CAG"], (34,48))
    Disease_list.append(DRPLA)
    
    HD = Disease("HD", "4", "HTT", ["CAG"], (26,36))
    Disease_list.append(HD)
    
    SBMA = Disease("SBMA", "X", "AR", ["CAG"], (34,38))
    Disease_list.append(SBMA)
    
    SCA1_uninterrupted = Disease("SCA1 Uninterrupt", "6", "ATXN1", ["CAG"], (35,39))
    Disease_list.append(SCA1_uninterrupted)
    
    SCA1_interrupted = Disease("SCA1 Interrupt", "6", "ATXN1", ["CAG", "CAT"], (44,46))
    Disease_list.append(SCA1_interrupted)
    
    SCA2 = Disease("SCA2", "12", "ATXN2", ["CAG"], (30,33))
    Disease_list.append(SCA2)
    
    SCA3 = Disease("SCA3", "14", "ATXN3", ["CAG"], (44,53))
    Disease_list.append(SCA3)
    
    SCA6 = Disease("SCA6", "19", "CACNA1A", ["CAG"], (18,20))
    Disease_list.append(SCA6)
    
    SCA7 = Disease("SCA7", "3", "ATXN7", ["CAG"], (27,34))
    Disease_list.append(SCA7)
    
    SCA17 = Disease("SCA17", "6", "TBP", ["CAG", "CAA"], (40,41))
    Disease_list.append(SCA17)
    
    FXS = Disease("FXS", "X", "FMR1", ["CGG", "AGG"], (199,200))
    Disease_list.append(FXS)
    
    #how to make an upper boundary of 200 for fxpoi and fxtas? add an if else statement in code for if fxs positive, fxpoi and fxtas are negative?
    FXPOI = Disease("FXPOI", "X", "FMR1", ["CGG", "AGG"], (44,55))
    Disease_list.append(FXPOI)
    
    FXTAS = Disease("FXTAS", "X", "FMR1", ["CGG", "AGG"], (44,55))
    Disease_list.append(FXTAS)
    
    #should there be a 3rd boundary for 55-200
    FRAXE = Disease("FRAXE", "X", "AFF2", ["CCG"], (40,200))
    Disease_list.append(FRAXE)
    
    FRAXF = Disease("FRAXF", "X", "FAM11A", ["GCC"], (26,300))
    Disease_list.append(FRAXF)
    
    FRA2A = Disease("FRA2A", "2", "AFF3", ["CGG"], (20,300))
    Disease_list.append(FRA2A)
    
    FRA7A = Disease("FRA7A", "7", "ZNF713", ["CGG"], (22,68))
    Disease_list.append(FRA7A)
    
    FRA10A = Disease("FRA10A", "10", "FRA19AC1", ["CGG"], (14,200))
    Disease_list.append(FRA10A)
    
    FRA11A = Disease("FRA11A", "11", "FRA11A", ["CGG"], (100,101))
    Disease_list.append(FRA11A)
    
    FRA11B = Disease("FRA11B", "X", "CBL2", ["CCG", "CGG"], (500,501))
    Disease_list.append(FRA11B)
    
    FRA12A = Disease("FRA12A", "12", "DIP2B", ["CGG"], (23,270))
    Disease_list.append(FRA12A)
    
    FRA16A = Disease("FRA16A", "16", "FRA16A", ["CCG"], (49,300))
    Disease_list.append(FRA16A)
    
    NIID = Disease("NIID", "X", "FMR1", ["CGG"], (44,55))
    Disease_list.append(NIID)
    
    FRDA = Disease("FRDA", "9", "FXN", ["GAA"], (33,66))
    Disease_list.append(FRDA)
    
    BSS = Disease("BSS", "16", "XYLT1", ["GCC"], (35,200))
    
    DM1 = Disease("DM1", "19", "DMPK", ["CTG"], (34,50))
    Disease_list.append(DM1)
    
    CDM1 = Disease("CDM1", "19", "DMPK", ["CTG"],(999,1000))
    Disease_list.append(DM1)
    
    SCA12 = Disease("SCA12", "5", "PPP2R2B", ["CAG"], (40,43))
    Disease_list.append(SCA12)
    
    OPMD = Disease("OPMD", "14", "PABPN1", ["GCA", "GCG", "GCT", "GCC"], (10,11))
    Disease_list.append(OPMD)
    
    HDL2 = Disease("HDL2", "16", "JPH3", ["CTG"], (28,40))
    Disease_list.append(HDL2)
    
    FECD = Disease("FECD", "18", "TCF4", ["CTG"], (69,120))
    Disease_list.append(FECD)
    
    GAD = Disease("GAD", "2", "GLS", ["GCA"], (89,90))
    Disease_list.append(GAD)
    
    PSACH = Disease("GAC", "19", "COMP", ["GAC"], (5,6))
    Disease_list.append(PSACH)
    
    MED = Disease("GAC", "19", "COMP", ["GAC"], (5,6))
    Disease_list.append(MED)
    
    BPES = Disease("BPES", "14", "FOXL2", ["GCA", "GCG", "GCT", "GCC"], (14,15))
    Disease_list.append(BPES)
    
    CCD = Disease("CCD", "6", "RUNX2", ["GCA", "GCG", "GCT", "GCC"], (14,27))
    Disease_list.append(CCD)
    
    CCHS = Disease("CCHS", "4", "PHOX2B", ["GCA", "GCG", "GCT", "GCC"], (23,26))
    Disease_list.append(CCHS)
    
    #HFGS
    #COMPLICATED, LOOK MORE INTO
    
    HPE5 = Disease("HPE5", "13", "ZIC2", ["GCA", "GCG", "GCT", "GCC"], (24,25))
    Disease_list.append(HPE5)
    #MORE INFO ON BOUNDARIES
    
    SPD = Disease("SPD", "2", "HOXD13", ["GCA", "GCG", "GCT", "GCC"], (15,22))
    Disease_list.append(SPD)
    
    #XLMD
    
    XLAG = Disease("XLAG", "X", "ARX", ["GCA", "GCG", "GCT", "GCC"], (16,20))
    Disease_list.append(XLAG)
    
    XLMR = Disease("XLMR", "X", "SOX3", ["GCA", "GCG", "GCT", "GCC"], (11,26))
    Disease_list.append(XLMR)
    
    #XLMRGHD
    
    EIEE = Disease("EIEE", "X", "ARX", ["GCA", "GCG", "GCT", "GCC"], (16,27))
    Disease_list.append(EIEE)
    
    PRTS = Disease("PRTS", "X", "ARX", ["GCA", "GCG", "GCT", "GCC"], (16,20))
    Disease_list.append(PRTS)
    
    DM2_uninterrupted = Disease("DM2 uninterrupted", "3", "CNBP", ["CCTG"], (30,75))
    Disease_list.append(DM2_uninterrupted)
    
    DM2_interrupted = Disease("DM2 interrupted", "3", "CNBP", ["CCTG", "GCTC", "TCTG"], (26,75))
    Disease_list.append(DM2_interrupted)
    
    BAFME = Disease("BAFME", "8", "SAMD12", ["TTTCA", "TTTTA"], (300,440))
    Disease_list.append(BAFME)
    
    SCA10 = Disease("SCA10", "22", "ATXN10", ["ATTCT"], (33,850))
    Disease_list.append(SCA10)
    
    SCA31 = Disease("SCA31", "16", "BEAN1", ["TGGAA"], (2499, 3800))
    Disease_list.append(SCA31)
    
    SCA36 = Disease("SCA36", "20", "NOP56", ["GGCCTG"], (14,650))
    Disease_list.append(SCA36)
    
    XDP = Disease("XDP", "X", "TAF1", ["CCCTCT"], (34,35))
    #MORE INFO ON BOUNDARIES
    
    C9ORF72 = Disease("C9ORF72", "9", "C9PORF72", ["GGGGCC"], (24,60))
    Disease_list.append(C9ORF72)
    
    EPM1 = Disease("EPM1", "21", "CSTB", ["CCCCGCCCCGCG"], (3, 30))
    Disease_list.append(EPM1)

    
    
    
    all_sequences_test(Disease_list, "C:\\Users\\KZJer\\Documents\\Repeat_Expansion_Tests_Research\\Genomes\\DRPLA_NEG_D63808.1.txt")
    
