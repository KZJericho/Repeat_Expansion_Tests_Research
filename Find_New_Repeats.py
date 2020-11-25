import json

#========================================#
#               STR Class                #
#========================================#
# STR: A short tandem repeat object  
class STR(object):
    def __init__(self, pattern, length, location):
        # The stored pattern
        self.pattern = pattern
        
        # Length of pattern in terms of repeats
        self.length = length
        
        # The start index of the pattern in the given path
        self.location = location
        
    def __repr__(self):
        pat = "\nPat: " + str(self.pattern) +"\n"
        leng = "Len: " + str(self.length) + "\n"
        loc = "Loc: " + str(self.location) + "\n"
        return pat + leng + loc
    
    def STR_to_tup(self):
        return (self.pattern, self.length, self.location)
    

#========================================#
#                   Mod                  #
#========================================#
# Computes modulo
def mod(dividend, divisor):
    mod = dividend%divisor
    if mod < 0:
        return mod + divisor
    else:
        return mod
    
#========================================#
#            Find New Patterns           #
#========================================#

# Find all patterns in the provided text with pattern unit length n
# inpath is the file name containing the genome sequence
# outpath is the file name where results will be recorded
def find_new_patterns(inpath, n):
    msg = """Choose Sort Method: \n 
        1) Pattern Length\n
        2) Repeat Length\n
        3) Location\n Input Here: """
        
    text = scrub(read_file(inpath))
    outpath = make_outname(inpath, "_RESULT")
        
    index = int(input(msg))
    if (index == 1):
        key_getter = lambda str_obj : len(str_obj.pattern)
    elif (index == 2):
        key_getter = lambda str_obj : str_obj.length
    elif (index == 3):
        key_getter = lambda str_obj : str_obj.location
        
    STR_list = []
    for length in range(3, n+1):
        STR_list.extend(patterns_search(text, length))
    
    sort_result(STR_list, key_getter)
        
    all_serialized = serialize_results(STR_list)
    
    result_list_to_json(outpath, all_serialized)
    return STR_list

#========================================#
#                  Hash                  #
#========================================#
# Computes the hash value of a given string
'''
def hash_rk(text):
    prime = 2971215073
    base = 256
    exponent = 1
    
    result = 0
    
    #Calculate exponent (not sure why there's a for loop, but it's consistent with the rest
    for i in range(pattern_length - 1):
        exponent = (base**(pattern_length-1))%prime
    for i in range(pattern_length):
        result = (base*result + ord(pat[i]))%prime #<-- it shouldnt be pat[i] but idk what to change pat to
    
    return result
'''

#========================================#
#             Pattern Search             #
#========================================#
# Go through a text document and search for STRs with pattern unit length n
def patterns_search(text, pattern_length):
        
    STRs = []
    
    # "shift" is the number of characters shifted from alignment mod pattern_length
    for shift in range(pattern_length):
        # An expression to help: i = shift + L * pattern_length, where L is the number of loops run thus far starting from 0
        curr_text = text[shift:shift+pattern_length]
        length = 1
        start = shift
        
        for i in range(shift + pattern_length, len(text), pattern_length):
            prev_text = curr_text;
            curr_text = text[i:i+pattern_length]
            
            if prev_text == curr_text:
                length += 1
                
            else:
                if length > 1:
                    STRs.append(STR(prev_text, length, start))
                length = 1
                start = i
    
    return STRs

#========================================#
#             File Reading               #
#========================================#
def read_file(path):
    with open(path, "rt") as f:
        return f.read()

    
def write_file(path, contents):
    with open(path, "wt") as f:
        f.write(contents)


def result_list_to_json(path, results):
    js = json.dumps(results)
    print(js)
    write_file(path, js)
    

def result_list_from_json(path):
    js = read_file(path)
    results = json.loads(js)

    # Copy previous results into the curent disease object
    for result in results:
        results[result] = results[result]

def sort_result(result_list, key_getter):
    result_list.sort(key = key_getter)
    return result_list


def serialize_results(results_unserialized):
    result = []
    for result_unserialized in results_unserialized:
        result.append(result_unserialized.STR_to_tup())
    return result

# .txt
def make_outname(inpath, tag):
    n = len(inpath) - 1
    while (inpath[n] != '.'):
        n -= 1
    file_ext = inpath[n:]
    name = inpath[:n]
    return name + tag + file_ext
    
def scrub(text):
    return "".join(text.strip().splitlines())
        
    
if __name__ == "__main__":
    result_list = find_new_patterns("C:\\Users\\KZJer\\Documents\\Repeat_Expansion_Tests_Research\\Testing Results\\New Repeats\\KM610327.1.txt", 10)
    print(result_list)
    #result_to_json("C:\Users\KZJer\Documents\Repeat_Expansion_Tests_Research\Testing Results\New Repeats", result_dict)