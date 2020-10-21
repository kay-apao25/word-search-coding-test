import unittest

from word_search import WordSearchPuzzle
from exceptions import InputError


test_dir = 'test_files/'
import sys

class TestWordSearchPuzzle(unittest.TestCase):
    def general_check_file_contents_test(self, filename):
        puzzle = WordSearchPuzzle('{}{}.pzl'.format(test_dir, filename))
        output = puzzle.search()

        f = open('{}.output'.format(filename), "r")
        text = f.read()
        f.close()

        self.assertIsNotNone(text)
        self.assertEqual(
            len([line for line in text.split('\n') if line]),
            len(puzzle.find_words)
        )
        self.assertTrue(
            set(puzzle.find_words) <= set(text.replace('\n', ' ').split(' '))
        )

        return output

    def test_sunny_scenario(self):
        filename = 'animals'
        output = self.general_check_file_contents_test(filename)
        self.assertTrue(
            output['CAT'] == ((1, 1), (1, 3))
        )
        self.assertTrue(
            output['DOG'] == ((2, 2), (4, 2))
        )
        self.assertTrue(
            output['COW'] == ((2, 4), (4, 4))
        )

    def test_some_words_not_found(self):
        filename = 'some-missing-animals'
        output = self.general_check_file_contents_test(filename)
        self.assertTrue(
            output['CAT'] == ((1, 1), (1, 3))
        )
        self.assertTrue(
            output['DOG'] == ((2, 2), (4, 2))
        )
        self.assertTrue(
            output['BEAR'] == 'Word not found'
        )
        self.assertTrue(
            output['DUCK'] == 'Word not found'
        )

    def test_file_not_provided(self):
        with self.assertRaises(TypeError):
            WordSearchPuzzle()

    def test_no_words_or_grid_provided(self):
        with self.assertRaises(ValueError) as err:
            WordSearchPuzzle(test_dir+'noGrid.pzl')
            WordSearchPuzzle(test_dir+'noWords.pzl')
        self.assertEqual(
            'No grid or words to search',
            str(err.exception)
        )

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            WordSearchPuzzle(test_dir+'does-not-exist.pzl')

    def test_empty_file(self):
        with self.assertRaises(InputError) as err:
            WordSearchPuzzle(test_dir+'empty.pzl')
        self.assertEqual(
            'Empty file',
            str(err.exception)
        )

    def test_new_lines_before_grid(self):
        filename = 'new-lines-before-grid'
        output = self.general_check_file_contents_test(filename)
        self.assertTrue(
            output['DIAMOND'] == ((7, 1), (1, 1))
        )
        self.assertTrue(
            output['HEART'] == ((5, 7), (5, 3))
        )

    def test_multiple_new_lines_before_words(self):
        filename = 'multiple-lines-before-words'
        output = self.general_check_file_contents_test(filename)
        self.assertTrue(
            output['DIAMOND'] == ((7, 1), (1, 1))
        )
        self.assertTrue(
            output['HEART'] == ((5, 7), (5, 3))
        )

    def test_new_lines_between_grids(self):
        with self.assertRaises(InputError) as err:
            WordSearchPuzzle(test_dir+'new-lines-between-grids.pzl')
        self.assertEqual(
            'Failed to initialize puzzle: '
            'Unequal number of rows and columns',
            str(err.exception)
        )

    def test_other_unicode_characters_attached_to_grid(self):
        filename = 'unique-characters-in-grid'
        output = self.general_check_file_contents_test(filename)
        self.assertTrue(
            output['SPRING'] == ((17, 14), (17, 19))
        )
        self.assertTrue(
            output['AUTUMN'] == ((25, 11), (30, 11))
        )
        self.assertTrue(
            output['WINTER'] == ((10, 18), (10, 23))
        )
        self.assertTrue(
            output['SUMMER'] == ((13, 2), (13, 7))
        )

    def test_grid_filled_with_non_alphabet_characters(self):
        with self.assertRaises(InputError) as err:
            WordSearchPuzzle(test_dir+'symbols.pzl')
        self.assertEqual(
            'Text grid should only contain letters',
            str(err.exception)
        )

    def test_unequal_number_of_rows_and_columns(self):
        with self.assertRaises(InputError) as err:
            WordSearchPuzzle(test_dir+'unequal-grid.pzl')
        self.assertEqual(
            'Failed to initialize puzzle: '
            'Unequal number of rows and columns',
            str(err.exception)
        )

    def test_words_in_capitalize_form(self):
        filename = 'words-in-capitalize-form'
        output = self.general_check_file_contents_test(filename)
        self.assertTrue(
            output['DIAMOND'] == ((7, 1), (1, 1))
        )
        self.assertTrue(
            output['HEART'] == ((5, 7), (5, 3))
        )

    def test_text_grid_letters_mixed_case(self):
        with self.assertRaises(InputError) as err:
            WordSearchPuzzle(test_dir+'mixed-case-text-grid.pzl')
        self.assertEqual(
            'Text grid letters should be consistent '
            'uppercase or lowercase form',
            str(err.exception)
        )


if __name__ == '__main__':
    unittest.main()
