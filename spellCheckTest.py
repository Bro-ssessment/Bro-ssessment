import os
from datetime import datetime
from excelParser import stripHTML


from symspellpy.symspellpy import SymSpell  # import the module

def main():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 3
    prefix_length = 7
    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return

    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 3
    f = open("note.html", "r")
    noteString = f.read()
    noteString = stripHTML(noteString)
    print(noteString)
    input_term = ("whereis th elove hehad dated forImuch of thepast who "
                  "couqdn'tread in sixtgrade and ins pired him. But who aree yooui to say its not. I am.")

    tstart = datetime.now()
    suggestions = sym_spell.lookup_compound(noteString,
                                            max_edit_distance_lookup)
    # display suggestion term, edit distance, and term frequency
    for suggestion in suggestions:
        print("{}, {}, {}".format(suggestion.term, suggestion.distance,
                                  suggestion.count))

    tend = datetime.now()
    time = tend - tstart
    print(time.seconds)

if __name__ == '__main__':
    main()
