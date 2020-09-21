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
        print("boo")
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
        
        #calculate first hash and pattern hash    
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
        if best_length < self.thresholds[0]:
            result = "Negative", best_length
        elif self.thresholds[0] <= best_length < self.thresholds[1]:
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
        print(Disease.name, Disease.results)
    

if __name__ == "__main__":
    Disease_list = []
    HD = Disease("HD", "4", "HTT", ["CAG"], (27,36))
    Disease_list.append(HD)
    SCA10 = Disease("SCA10", "22", "ATXN10", ["ATTCT"], (33,850))
    Disease_list.append(SCA10)
    DRPLA = Disease("DRPLA", "12", "ATN1", ["CAG"], (35,48))
    Disease_list.append(DRPLA)
    
    
    all_sequences_test(Disease_list, "C:\\Users\\KZJer\\Documents\\Repeat_Expansion_Tests_Research\\Genomes\\DRPLA_NEG_D63808.1.txt")
    
'''        
    #determine diseaase positive/negative    
    if best_length < 1:
        return None
    elif best_length <= 44:
        return "CGG Repeat Length:", best_length, "Location: Index", current_best_location, "Negative Result: Normal Allele"
        
    elif best_length in range (28, 34):
        return "CGG Repeat Length:", best_length, "Location: Index", current_best_location, "Unmutable Normal Result"
        
    elif best_length in range (34, 37):
        return "CGG Repeat Length:", best_length, "Location: Index", current_best_location, "Positive Result: Reduced Penetrance"
        
    elif best_length > 36:
        return "CGG Repeat Length:", best_length, "Location: Index", current_best_location, 
        "Positive Result: Full Penetrance
        
'''