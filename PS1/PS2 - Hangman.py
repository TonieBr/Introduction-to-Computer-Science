# Hangman Game
# -----------------------------------

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
        
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    
    tmp = list()
    
    for letter in secret_word:
        if letter not in letters_guessed: tmp.append('_')
        else: tmp.append(letter)
        
        tmp.append(' ')
        
    return ''.join(tmp)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    
    tmp = list()
    
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            tmp.append(letter)
            
    return ''.join(tmp)

def get_unique_letters(secret_word):
    
    letters = list()
    unique = 0
    
    for letter in secret_word:
        if letter not in letters:
            letters.append(letter)
            unique = unique + 1
        
        return unique
        
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    GUESSES = 6
    letters_guessed = list()
    warnings = 3
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    ABC = string.ascii_lowercase
    
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long')
    
    while True:
        
        if GUESSES <= 0:
            print('You ran out of guesses! The word was:', secret_word)
            break
            
        if is_word_guessed(secret_word, letters_guessed):
            finalScore = GUESSES * get_unique_letters(secret_word)
            print('Congratulations, you won!')
            print('Your total score for this game is:', finalScore)
            break
        
        print('-------------')
        print('You have', GUESSES, 'guesses left')
        print('Available letters:', get_available_letters(letters_guessed))
        
        while True:
            letter = input('Please guess a letter: ').lower()
            
            if warnings == 0:
                warnings = 3
                print('Too many warnings!')
                GUESSES = GUESSES - 1
                break
            
            if len(letter) != 1 or letter not in ABC:
                print('Wrong input! Try again: ')
                warnings = warnings - 1
                continue
                
            if letter in letters_guessed:
                print('Letter already guessed!')
                warnings = warnings -1 
                continue
                
            letters_guessed.append(letter)      
            if letter in secret_word: 
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            else: 
                print('Wrong guess:', get_guessed_word(secret_word, letters_guessed))
                if letter in VOWELS: 
                    GUESSES = GUESSES - 2
                else: 
                    GUESSES = GUESSES - 1
                    
            break
                
def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    
    my_word = my_word.replace(' ', '')
    index = 0
    
    if len(my_word) is not len(other_word):
        return False
    
    for letter in my_word:
        if letter == '_':
            if other_word[index] in my_word:
                return False
            else:
                index = index + 1
                continue
        
        if letter is not other_word[index]:
            return False
        
        index = index + 1
        
    return True
    
def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word, end=' ')
            
def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    GUESSES = 6
    letters_guessed = list()
    warnings = 3
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    ABC = string.ascii_lowercase
    
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long')
    
    while True:
        
        if GUESSES <= 0:
            print('You ran out of guesses! The word was:', secret_word)
            break
            
        if is_word_guessed(secret_word, letters_guessed):
            finalScore = GUESSES * get_unique_letters(secret_word)
            print('Congratulations, you won!')
            print('Your total score for this game is:', finalScore)
            break
        
        print('-------------')
        print('You have', GUESSES, 'guesses left')
        print('Available letters:', get_available_letters(letters_guessed))
        
        while True:
            letter = input('Please guess a letter: ').lower()
            
            if letter == '*':
                myWord = get_guessed_word(secret_word, letters_guessed)
                show_possible_matches(myWord)
                continue
            
            if warnings == 0:
                warnings = 3
                print('Too many warnings!')
                GUESSES = GUESSES - 1
                break
            
            if len(letter) != 1 or letter not in ABC:
                print('Wrong input! Try again: ')
                warnings = warnings - 1
                continue
                
            if letter in letters_guessed:
                print('Letter already guessed!')
                warnings = warnings -1 
                continue
                
            letters_guessed.append(letter)      
            if letter in secret_word: 
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            else: 
                print('Wrong guess:', get_guessed_word(secret_word, letters_guessed))
                if letter in VOWELS: 
                    GUESSES = GUESSES - 2
                else: 
                    GUESSES = GUESSES - 1
                    
            break



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
