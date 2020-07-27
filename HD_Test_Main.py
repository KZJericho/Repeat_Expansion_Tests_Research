def hash_mul31(s):
    result = ord(s[0])
    for i in range(1, len(s)):
        result = result*31+ord(s[i])
    return result

def find_best_pattern(pat, s):

    pattern_length = len(pat)
    pattern_hash = hash_mul31(pat)

    best_length = 0
    current_best_location = None
    
    current_length = 0
    current_location = None

    i = 0
    #rolling hash
    while i < (len(s)):
        
        current_chunk = s[i:i+pattern_length]
        current_hash = hash_mul31(current_chunk)
        if current_hash == pattern_hash and s[i:i+pattern_length] == pat:
                current_length += 1   
                current_location = i 

                i += len(pat) 
        
        #record best lengths
        else:
            if current_length > best_length:
                best_length = current_length
                current_best_location = current_location - (len(pat))*((current_length)-1)

            current_length = 0
            i += 1

    if current_length > best_length:
        best_length = current_length
        current_best_location = current_location - (len(pat))*((current_length)-1)

    
    return (best_length, current_best_location)
    
def open_genome_file_as_string(filename): 
    file = open(filename, 'r')
    lines = file.readlines()
    result = "".join(lines) 
    return result 

def run_best_pattern_on_genome(file, pattern):
    genome = open_genome_file_as_string(file)
    print(find_best_pattern(pattern, genome))

    
def run_main_for_HTT():
    genomes = ['Test_1_NM_002111.6.txt'] #add all genome names here
    pattern = "CAG"
    for file in genomes: 
        repetitions, location = run_best_pattern_on_genome(file, pattern)
        print("For file %s, the pattern %s repeats %d times starting at index %d" % (file, pattern, repetitions, location))

if __name__ == '__main__':
    run_main_for_HTT()
