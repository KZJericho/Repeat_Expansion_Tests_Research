def my_mod(dividend, divisor):
    mod = dividend%divisor
    if mod < 0:
        return mod + divisor
    else:
        return mod

# txt is the text representing our genome
# pats is a list of the patterns to look for
def SCA1_Test(txt):
    pats = ["CAG", "CAT"]
    pat1 = "CAG"
    results = None 
    print("Testing for SCA1...", end = "")
    
    for pat in pats:
        assert(len(pat) <= len(txt))
    
    pattern_length = len(pats[0])
    text_length = len(txt)
    prime = 2971215073
    
    current_txt_hash = 0
    current_txt_hash_onepat = 0
    pattern_hash_1 = 0

    best_length_w_interrupt = 0
    current_best_location_w_interrupt = None
    best_length_without_interrupt = 0
    current_best_location_without_interrupt = None
    
    current_length_w_interrupt = 0
    current_location_w_interrupt = None
    current_length_without_interrupt = 0
    current_location_without_interrupt = None
    
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
    for pat in pats:
        pattern_hash = 0
        for i in range(pattern_length):
            pattern_hash = (base*pattern_hash + ord(pat[i]))%prime
        pats_dictionary[pat] = pattern_hash
        
    #calculate first hash and pattern hash    
    for i in range(pattern_length):
        current_txt_hash = my_mod((base*current_txt_hash + ord(txt[i])),prime)
        current_txt_hash_onepat = my_mod((base*current_txt_hash_onepat + ord(txt[i])),prime)
        pattern_hash_1 = (base*pattern_hash + ord(pat1[i]))%prime

    i = 0
    #rolling hash
    while i < (len(txt)):
        number_of_letters_rolling_over = 0 
        number_of_letters_rolling_over_onepat = 0
        current_chunk = txt[i:i+pattern_length]
        
        if current_txt_hash_onepat == pattern_hash_1 and current_chunk == pat1:
            current_length_without_interrupt += 1
            current_location_without_interrupt = i
            
            number_of_letters_rolling_over_onepat = pattern_length
            
        for pat in pats:
            pattern_hash = pats_dictionary[pat]
            if current_txt_hash == pattern_hash and current_chunk == pat:
                current_length_w_interrupt += 1  
                current_location_w_interrupt = i 

                number_of_letters_rolling_over = pattern_length
                break
                
        
        
        #record best lengths
        else:
            if current_length_w_interrupt > best_length_w_interrupt:
                best_length_w_interrupt = current_length_w_interrupt
                current_best_location_w_interrupt = current_location_w_interrupt - (pattern_length)*((current_length_w_interrupt)-1)

            current_length_w_interrupt = 0
            number_of_letters_rolling_over = 1 
            
            if current_length_without_interrupt > best_length_without_interrupt:
                best_length_without_interrupt = current_length_without_interrupt
                current_best_location_without_interrupt = current_location_without_interrupt - (pattern_length)*((current_length_without_interrupt)-1)
                
                current_length_without_interrupt = 0
                number_of_letters_rolling_over_onepat = 1
        
        #re-hash
        if i + number_of_letters_rolling_over <= text_length - pattern_length:
            for j in range(number_of_letters_rolling_over):
                current_txt_hash = my_mod((base*(current_txt_hash-ord(txt[i])*exponent) + ord(txt[i+pattern_length])),prime)
                i += 1
        
            if current_txt_hash < 0:
                current_txt_hash = current_txt_hash + prime
        else:
            i += number_of_letters_rolling_over
                
        if i + number_of_letters_rolling_over_onepat <= text_length - pattern_length:
            for j in range(number_of_letters_rolling_over_onepat):
                current_txt_hash_onepat = my_mod((base*(current_txt_hash_onepat-ord(txt[i])*exponent) + ord(txt[i+pattern_length])),prime)
                i += 1

            
            if current_txt_hash_onepat < 0:
                current_txt_hash_onepat = current_txt_hash_onepat + prime
        else:
            i += number_of_letters_rolling_over_onepat

    #record best lengths last time
    if current_length_w_interrupt > best_length_w_interrupt:
        best_length_w_interrupt = current_length_w_interrupt
        current_best_location_w_interrupt = current_location_w_interrupt - (len(pat1))*((current_length_w_interrupt)-1)
        
    if current_length_without_interrupt > best_length_without_interrupt:
        best_length_without_interrupt = current_length_without_interrupt
        current_best_location_without_interrupt = current_location_without_interrupt - (pattern_length)*((current_length_without_interrupt)-1)
        
    #determine diseaase positive/negative   
    
    if best_length_w_interrupt <= 44 or best_length_without_interrupt <= 35: 
        return "CAG/CAA Repeat Length with interrupt:", best_length_w_interrupt, "Location: Index", current_best_location_w_interrupt, "CAG/CAA Repeat Length without interrupt", best_length_without_interrupt, "Location: Index", current_best_location_without_interrupt, "Negative Result: Normal Allele"
        
    elif best_length_w_interrupt >= 45:
        return "CAG/CAA Repeat Length:", best_length_w_interrupt, "Location: Index", current_best_location_w_interrupt, "Positive Result: Pathogenic Allele WITH INTERRUPTION"

        
    elif best_length_without_interrupt in range (36,39):
        return "CAG/CAA Repeat Length:", best_length_without_interrupt, "Location: Index", current_best_location_without_interrupt, "Undetermined Result: Intermediate Allele WITHOUT INTERRUPTION"
        
    elif best_length_without_interrupt >= 39:
        return "CAG/CAA Repeat Length:", best_length_without_interrupt, "Location: Index", current_best_location_without_interrupt, "Positive Result: Pathogenic Allele WITHOUT INTERRUPTION"
            
    


print(SCA1_Test("CAG"))

'''
4-35 repeats

36-44 repeats w interruption

Intermediate Allele (Unclear): 
36-38 repeats without interruption

Pathogenic Allele (Diseased):
39-44 repeats without interruption

46-70 uninterrupted repeats with interruptions 
'''
