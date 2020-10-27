def my_mod(dividend, divisor):
    mod = dividend%divisor
    if mod < 0:
        return mod + divisor
    else:
        return mod
    
def find_new_patterns(text, n):
    pass
    # while length < n+1
    # loop through and run patterns_search for each pattern length
    # return sets 

    
class short_tandem_repeat(object):
    def __init__(self, length, location, pattern, path = None):
        self.path = path
        self.length = length
        self.location = location
        self.pattern = pattern

# Consider how to handle case where we have a large STR
# Instead of dealing with patterns within patterns, we will print it all out
# 
        
# Go through a text document and search for STRs with pattern unit length n
def patterns_search(text, pattern_length):
    def my_mod(dividend, divisor):
        mod = dividend%divisor
        if mod < 0:
            return mod + divisor
        else:
            return mod
    # Define variables for hashing
    text_length = len(text)
    
    prev_hash = 0
    curr_hash = 0
    
    prime = 2971215073
    base = 256
    exponent = 1
    i = 0
    
    #calculate exponent 
    for i in range(pattern_length - 1):
        exponent = (base**(pattern_length-1))%prime
    
    # Find our prev text chunk by sampling the first n characters.
    # Look at curr text chunk n characters away (123) then (456)
    prev_text = text[0:pattern_length]
    curr_text = txt[pattern_length:2*pattern_length] 
    
    # Hash prev text chunk
    # Hash the curr text chunk
    for i in range(pattern_length):
        prev_hash = (base*prev_hash + ord(pat[i]))%prime
        curr_hash = (base*curr_hash + ord(pat[i]))%prime
    
    # "shift" is the number of characters shifted from alignment mod pattern_length
    #do i need a while statement here?
    for shift in range(pattern_length):
        for i in range(shift, len(text), pattern_length): # <-- should pattern length be -1?
            
            #compare first two chunks
            if prev_text == curr_text and prev_hash == curr_hash:
                #record the pattern name (prev_text or curr_text) into class
                #+1 to the first term in tuple associated to dict key (length)
                #record index of prev_text as second term in tuple associated to dict key (location)
                prev_text = curr_text
                curr_text = #next text chunk
                
                #rehash curr_hash (PROBABLY INCORRECT RN)
                for i in range(pattern_length):
                    curr_hash = my_mod((base*(curr_hash-ord(txt[i])*exponent) + ord(txt[i+pattern_length])),prime)
            pass
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