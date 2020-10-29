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
        pat = "Pat: " + str(self.pattern) +"\n"
        leng = "Len: " + str(self.length) + "\n"
        loc = "Loc: " + str(self.location) + "\n"
        return pat + leng + loc
    

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
def print_results(Dict):
    for key in Dict:
        print(Dict[key])

# Find all patterns in the provided text with pattern unit length n
def find_new_patterns(text, n):
    STR_dict = {}
    for length in range(3, n+1):
        STR_dict[length] = patterns_search(text, length)
        
    return STR_dict 

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

if __name__ == "__main__":
    result_dict = find_new_patterns("CAGCAGCAGCAGCCGCCGATTACGAACGATCGTACGATTC", 4)
    print_results(result_dict)

        
        

