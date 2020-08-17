from Main import *

def auto_test(pat, txt, expected_length, expected_pos):
    assert(len(pat) <= len(txt))
    #print(pat, txt, expected_length, expected_pos)
    
    #print(f"Running test on:\n\tPattern: {pat}\n\tText: {txt}\n...")
    result = find_best_pattern(txt, pat)
    #print(f"Got the following as result:\n\tLength: {result[0]}\n\tLocation: {result[1]}")

    assert(result[0] == expected_length and result[1] == expected_pos)
    #print("Test Passed!")
    
    
def unit_test():

    print("Testing unit_tests...", end = "")
    txt = "Zbb"
    pattern = "b"
    auto_test(pattern, txt, 2, 1)

    
    txt = "GEEKSFORGEEKGEEKGEEKKS"
    pat = "GEEK" 
    auto_test(pat, txt, 3, 8)
    
    
    txt = "LIE"
    pat = "L" 
    auto_test(pat, txt, 1, 0)
   

    txt = "KKKAAKKKKKAA"
    pat = "K"
    auto_test(pat, txt, 5, 5)
    
    txt = "abcCAGCAGCAGabcCAGCAGCAGCAGCAGabcCAG"
    pat = "CAG"
    auto_test(pat, txt, 5, 15)
    
    print("Passed unit test cases!")


def test_generator0():
    print("Testing test_generator0...", end = "")
    TEST_NUMBER_CASES = 100
    PATTERN_LENGTH = 100
    
    for x in range(TEST_NUMBER_CASES):
        pattern = chr(ord('a')+(x%26))*(x%PATTERN_LENGTH)
        text = "Z" + pattern + pattern
        
        if (len(pattern) == 0 or len(pattern) > len(text)):
            continue
        result = find_best_pattern(text, pattern)

        assert(result[0] == 2)
        assert(result[1] == 1)
        
    print("Passed all test cases in generator 0!!")


def test_generator1():
    print("Testing test_generator1...", end = "")
    TEST_NUMBER_CASES = 100
    PATTERN_LENGTH = 100
    
    for i in range(TEST_NUMBER_CASES):
        pattern = chr(ord('z')+(i%26))*(i%PATTERN_LENGTH)
        if (len(pattern) == 0):
            continue
        
        text = pattern + "sdjivd" + pattern*3 + "end" + pattern
        result = find_best_pattern(text, pattern)

        assert(result[0] == 3)
        assert(result[1] == len(pattern) + 6)
        
    print("Passed all test cases in generator 1!!")


def test_generator2():
    print("Testing test_generator2...", end = "")
    TEST_NUMBER_CASES = 100
    PATTERN_LENGTH = 100
    
    for x in range(TEST_NUMBER_CASES):
        pattern = chr(ord('q')+(x%26))*(x%PATTERN_LENGTH)
        if (len(pattern) == 0):
            continue
        
        text = pattern*3 + "helloworld" + pattern*4 + "sqjvqwqmcad" + pattern*8 + "sqvliqnv" + pattern + "ending"
        result = find_best_pattern(text, pattern)

        assert(result[0] == 8)
        assert(result[1] == len(pattern)*7 + 21)
        
    print("Passed all test cases in generator 2!!")


def main_run():
    unit_test()
    test_generator0()
    test_generator1()
    test_generator2()

main_run()

if __name__ == '__main__':
    main_run()



