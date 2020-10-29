'''
Preliminary to the following - I may need to consider it a bit more, but I'm not entirely sure we can fully take advantage of Karp-Rabin in this version of the code. I will explain this tomorrow as I'm not entirely sure at the moment.

A larger note - you should separate the hashing process into its own functions so that we can improve the readability of the main process
in this code - as it stands now, at least as someone coming in and reading this code, it takes me some time to differentiate the lines that are hashing and rehashing vs actually collecting pattern information from the text.

Separating these will allow us to mutually exclude the two functions from each other when we do testing, and thus we will be able to test and debug them separately. I've added headers for hash and rehash to the top of this file, but you'll need to implement them.

To get you motivated a bit, identify the lines where you hash, identify the lines where you rehash, and finally replace those lines with the appropriate function calls (hint - you may not need to write rehash separately from hash, as their is never overlap between the curr and prev chunks and thus you will be rehashing a number of characters equal to the size of the pattern with every hash, which is, by our scheme, equivalent to just calling hash on those characters).

Additionally, consider how many things that you actually need to hash per loop - if we have a previous and a current chunk, and then proceed to the next iteration, what will our new previous block be (big hint: you've already computed the hash for this chunk (bigger hint: the old current chunk becomes the new previous chunk))?

I also ran through the code and modified a few of the simpler lines: 
Modified the following lines:
- 15: Changed class name to STR to follow class naming style
- 66: Flipped the terms in the 'and' expression as the order has non-trivial effect on efficiency
- Throughout: Removed a few lines and moved a few lines around, mostly concerning the current and previous text to ensure that they are set properly

Added comments on the following lines:
- STR Definition: Added a few explanatory comments
- 64: A note about how to interpret i's value
- Added a lot of hints and other notes in the "patterns_search" code - I recommend you read over these
'''
#========================================#
#               STR Class                #
#========================================#
# STR: A short tandem repeat object  
class STR(object):
    def __init__(self, length, location, pattern, path = None):
        # Allows us to associate a result with a particular file
        self.path = path
        
        # Length of pattern in terms of repeats
        self.length = length
        
        # The start index of the pattern in the given path
        self.location = location
        
        # The stored pattern
        self.pattern = pattern

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
def find_new_patterns(text, n):
    pass
    # while length < n+1
    # loop through and run patterns_search for each pattern length
    # return sets 

#========================================#
#                  Hash                  #
#========================================#
# Computes the hash value of a given string
def hash(text):
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
#========================================#
#             Pattern Search             #
#========================================#
# Go through a text document and search for STRs with pattern unit length n
def patterns_search(text, pattern_length):
        
    # Define variables for hashing
    # These should be lumped into the hash we use/ passed as parameters into the hash
    text_length = len(text)
    
    prev_hash = 0
    curr_hash = 0
    
    # Hash prev text chunk
    # Hash the curr text chunk
    for i in range(pattern_length):
        prev_hash = (base*prev_hash + ord(pat[i]))%prime
        curr_hash = (base*curr_hash + ord(pat[i]))%prime
    
    # "shift" is the number of characters shifted from alignment mod pattern_length
    #do i need a while statement here?
    for shift in range(pattern_length):
        # The inner loop is going to do the search work - we should use the outer loop to set up for the inner loop,
        # like finding the initial curr chunk.
        
        # An expression to help: i = shift + L * pattern_length, where L is the number of loops run thus far starting from 0
        for i in range(shift + pattern_length, len(text), pattern_length): 
            prev_text = curr_text;
            curr_text = # WRITE ME!
            
            if prev_hash == curr_hash and prev_text == curr_text :
                # We need an STR object to track the information in if one doesn't exist yet.
                
                prev_text = curr_text
                curr_text = #next text chunk
                
                #rehash curr_hash (PROBABLY INCORRECT RN)
                for i in range(pattern_length):
                    curr_hash = mmod((base*(curr_hash-ord(txt[i])*exponent) + ord(txt[i+pattern_length])),prime)
            else:
                pass 
                # What do we need to do if we FAIL to match?
                # A few ideas... 
                # Well, if we have an STR, we need to store it somewhere, as we're going to likely make many.
                # We also need to indicate that whatever STR we WERE modifying is no longer relevant
                
    #Compare one last time
    if prev_text == curr_text and prev_hash == curr_hash:
        #record the pattern name (prev_text or curr_text) into class
        #+1 to the first term in tuple associated to dict key (length)
        #record index of prev_text as second term in tuple associated to dict key (location)

    #in case of negative hash value
        if curr_hash < 0:
            curr_hash = curr_hash + prime
        else: 
            curr_hash = curr_hash

'''
#---#
def patterns_search(text, n):
    # "GCA" "Index 3" "5"
    # pat -> {(location, length)} TUPLE
    # We want to track the repeats (where they start, length)
    # Look for patterns up to length n
    # Define repeat as 2 or more
    patterns_dict = {}
    
    text_length = len(text)
    prime = 2971215073
    
    first_text_hash = 0
    first_hashes_dict = {}
    current_text_hash = 0
    length = 0
    exponent = 1
    exponents_dict = {}
    base = 256
    i = 0
    
    #calculate exponents
    for pattern_length in range(3,n+1):
        for i in range(pattern_length - 1):
            exponent = (base**(pattern_length-1))%prime
            exponents_dict[pattern_length] = exponent
            
    #calculate first hash chunks
    for pattern_length in range(3, n+1):
        for i in range(pattern_length):
            first_text_hash = my_mod((base*first_text_hash + ord(text[i])),prime)
            first_hashes_dict[pattern_length] = first_text_hash
    
    #calculate current text hash
    for length in range (3,n+1):
        for i in range(length):
            curr_hash = my_mod((base*curr_hash + ord(txt[i])),prime)
    
    # n+1 for inclusivity
    for pattern_length in range(3,n+1):
        for offset in range(pattern_length):
            prev_text = None
            prev_hash = None
            for location in range(offset, len(text), pattern_length):
                curr_text = text[location:location+pattern_length-1]
                #should it be -1?
                if pattern_prev == None or pattern_prev != pattern_curr:
                    if length > 1:
                        patterns_dict[pattern_prev] = length
                    length = 1
                    pattern_prev = pattern_curr
                else:
                    if prev_text == curr_text and prev_hash == curr_hash:
                        length += 1
                        
'''
'''
Hash value of [i,i+x] = a
Hash value of [i+x+1,i+2x] = b
if a = b:
    pattern = [i,i+x]
    location = [i]
    length += 1
'''

'''
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
'''