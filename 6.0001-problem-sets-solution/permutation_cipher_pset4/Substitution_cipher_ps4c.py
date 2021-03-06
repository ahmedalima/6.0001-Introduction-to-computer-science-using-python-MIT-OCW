# Problem Set 4C
# Name: <Ahmed ALi Mohamed>
# Collaborators: None

import string
from permutation_ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text =  text
        self.valid_words = load_words(WORDLIST_FILENAME)    
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        perm_vow_low = vowels_permutation.lower()
        perm_vow_upp = vowels_permutation.upper()
        #initialize empty transpose dictionay
        transpose_dict = {}
        #function to map all letter to thesleves except vowels to permutation
        
        def add_trans_dict(lett, vowels, perm):
            '''
            #lett => all letter, either low or upp
            #vowels, either upp or low
            #perm of vowl, must be the same case type as vowels
            '''
            #loop through each letter in lett:
            for c in lett:
                #test for being vowels, if so
                if c in vowels:
                    #make the current letter as key and value is the shuffled charchter
                    transpose_dict[c] = perm[vowels.index(c)]
                else:
                    #otherise, both the key and value are the same
                    transpose_dict[c] = c
        #adding lowert letter to the dictionary
        add_trans_dict(string.ascii_lowercase, VOWELS_LOWER, perm_vow_low)
        #adding upper letter to the dictionary
        add_trans_dict(string.ascii_uppercase, VOWELS_UPPER, perm_vow_upp)
        #returning copy of dictionary to avoid modifying the original one
        return transpose_dict.copy()

    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        #string variable to hold building the encrypted msg incremently
        encrypted_msg = ""
        #loop through the message text and apply transpose
        for c in self.message_text:
            #add the transpose letter, other wise, leave it as it is.
            encrypted_msg = encrypted_msg + transpose_dict.get(c,c)
        #Returns: an encrypted version of the message text
        return encrypted_msg
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: (best_perm, max_decryp_msg)  => tuple
        best_perm: the permutation that make the maximum number of valid words
        max_decryp_msg: the best decrypted message that is of maximum valid words
        
        Hint: use your function from Part 4A
        '''
        perms = get_permutations("aeiou")
        best_perm = ""
        max_decryp_msg = ""
        max_num_val_words = 0
        length_encrypt_msg = len(self.message_text)
        #loop for every possible permutation
        for perm in perms:
            #create var to hold current permutation
            curr_perm = perm
            #create var to hold the sum of valid words
            curr_num_val_words = 0
            #build a dictionary for this permutations
            current_transpose_dict = self.build_transpose_dict(perm)
            #apply the encryption on the text
            curr_decryp_msg = self.apply_transpose(current_transpose_dict)
            #test for validity of words
            for w in (curr_decryp_msg.split()):
                if is_word(self.valid_words, w):
                    curr_num_val_words += 1
            #if equal to num of encrypted, return  the current encryption
            if curr_num_val_words == length_encrypt_msg:
                return (curr_perm, curr_decryp_msg)
            #if bigger than current max, update the curent max and decrypted msg
            if curr_num_val_words > max_num_val_words:
                best_perm = curr_perm
                max_decryp_msg = curr_decryp_msg
                max_num_val_words = curr_num_val_words
                
        return (best_perm, max_decryp_msg)
    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
