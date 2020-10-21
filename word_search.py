import re
import sys

from exceptions import InputError


class WordSearchPuzzle(object):
    def __init__(self, input_file):
        self.find_words = []
        self.grid = []
        self.filename = input_file.split('.')[0]

        self.setup_puzzle(input_file)

    def setup_puzzle(self, input_file):
        with open(input_file) as f:
            ftext = f.read().strip().split('\n')

        if len(ftext) == 1 and ftext[0] == '':
            raise InputError('Empty file')

        if not re.search('[a-zA-Z]', ftext[0]):
            raise InputError('Text grid should only contain letters')

        if not(ftext[0].isupper() or ftext[0].islower()):
            raise InputError(
                'Text grid letters should be consistent '
                'uppercase or lowercase form'
            )
        letter_case = 'upper' if ftext[0].isupper() else 'lower'
        text = [self.check_if_valid_letters(line.split(), letter_case)
                for line in ftext]

        if '' not in text:
            raise ValueError('No grid or words to search')

        index = text.index('')
        text_grid = text[:index]

        if not self.check_if_valid_grid(text_grid):
            raise InputError(
                'Failed to initialize puzzle: '
                'Unequal number of rows and columns'
            )
        self.grid = text_grid

        '''
        Line 53: Remove empty strings in cases of
        multiple next lines before the words to be searched.
        Refer to file: multiple-lines-before-words.pzl
        '''
        words = [word for word in text[index+1:] if word]
        self.find_words = words

    def check_if_valid_grid(self, grid):
        row_length = len(grid)
        for t in grid:
            if len(t) != row_length:
                return False
        return row_length

    def get_column(self, i):
        return ''.join(row[i] for row in self.grid)

    def find_in_row(self, index, word):
        line_word = self.grid[index]

        # Find string both in forward and backward position
        if word in line_word:
            return (
                (line_word.index(word) + 1, index + 1),
                (line_word.index(word)+len(word), index+1)
            )
        elif word[::-1] in line_word:
            return (
                (line_word.index(word[::-1]) + len(word), index + 1),
                (line_word.index(word[::-1])+1, index+1)
            )

    def find_in_column(self, index, word):
        column_word = self.get_column(index)

        # Find string both in forward and backward position
        if word in column_word:
            return (
                (index+1, column_word.index(word) + 1),
                (index+1, column_word.index(word)+len(word))
            )
        elif word[::-1] in column_word:
            return (
                (index+1, column_word.index(word[::-1]) + len(word)),
                (index+1, column_word.index(word[::-1])+1)
            )

    def search(self):
        output = {}
        for word in self.find_words:
            for index in range(0, len(self.grid)):
                result = self.find_in_row(index, word)
                if result:
                    break

                result = self.find_in_column(index, word)
                if result:
                    break

            if result:
                output[word] = result
            else:
                output[word] = 'Word not found'

        self.create_output_file(output)
        return output

    def create_output_file(self, output):
        try:
            f = open("{}.output".format(self.filename), "x")
            f.close()
        except FileExistsError:
            pass

        f = open("{}.output".format(self.filename), "w")
        for key in output:
            if 'not found' in output[key]:
                f.write('{} {}\n'.format(key, output[key]))
            else:
                f.write('{} {} {}\n'.format(
                    key,
                    output[key][0],
                    output[key][1])
                )
        f.close()

    def check_if_valid_letters(self, line, letter_case):
        """
        1. Checks if non-alphabet characters are in grid
        2. Checks if text grid letters are in consistent
           uppercase or lowercase form
        """
        string = ''.join(line)
        if string and not self.grid:
            if (letter_case == 'upper' and not string.isupper()) \
               or (letter_case == 'lower' and not string.lower()):
                raise InputError(
                    'Text grid letters should be consistent '
                    'uppercase or lowercase form'
                )
        elif not string and not self.grid:
            self.grid = True
        elif self.grid:
            string = string.upper() if letter_case == 'upper' \
                     else string.lower()

        return string


if __name__ == '__main__':
    try:
        puzzle = WordSearchPuzzle(sys.argv[1])
        puzzle.search()
    except FileNotFoundError:
        print('File does not exist')
    except IndexError:
        print('Please provide input file')
