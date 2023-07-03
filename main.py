import re
from statistics import mean


class SqStatistics:
    COMPOUND_LETTERS = {
        "dh": "ð",
        "gj": "ɟ",
        "ll": "ɫ",
        "nj": "ɲ",
        "rr": "r̪",
        "sh": "ʃ",
        "th": "θ",
        "xh": "ҳ",  # "d͡ʒ", (NOT STANDART)
        "zh": "ʒ",
    }

    ALPHABET = [
        "a", "b", "c", "ç", "d", "ð", "e",
        "ë", "f", "g", "ɟ", "h", "i", "j",
        "k", "l", "ɫ", "m", "n", "ɲ", "o",
        "p", "q", "r", "r̪", "s", "ʃ", "t",
        "θ", "u", "v", "x", "ҳ", "y", "z",
        "ʒ"
    ]

    VOWELS = ["a", "e", "ë", "i", "o", "u", "y"]

    CONSONANTS = [
        "b", "c", "ç", "d", "ð", "f", "g",
        "ɟ", "h", "j", "k", "l", "ɫ", "m",
        "n", "ɲ", "p", "q", "r", "r̪", "s",
        "ʃ", "t", "θ", "v", "x", "ҳ", "z",
        "ʒ"
    ]

    DEFAULT_PAGE_SIZE = 3000  # characters

    def replace_compound_characters(self, text):
        temp_text = text
        for k, v in self.COMPOUND_LETTERS.items():
            temp_text = re.sub(k, v, temp_text.lower())
        return temp_text

    def letter_percentage(self, text):
        total_characters = len([x for x in text if x.isalpha()])
        total_vowels = len([x for x in text if x.isalpha() and x in self.VOWELS])
        total_consontants = len([x for x in text if x.isalpha() and x in self.CONSONANTS])
        result = {}
        for letter in self.ALPHABET:
            frequency = text.lower().count(letter)
            partial_total = total_vowels if letter in self.VOWELS else total_consontants
            result[letter] = {
                "total": frequency / total_characters,
                "partial": frequency / partial_total
            }
        sorted_result = {
            k: v for k, v in
            sorted(result.items(), key=lambda x: x[1]["total"], reverse=True)
        }
        print(sorted_result)
        return sorted_result

    @staticmethod
    def compare_lengths(text_left, text_right):
        left = len([x for x in text_left if x.isalpha()])
        right = len([x for x in text_right if x.isalpha()])
        print(f"Text Left has a length of {left} whereas the right one a length of {right}.")
        percentage_smaller = ((left - right) / left) * 100
        print(f"The new text is {percentage_smaller:0.2f}% smaller.")
        print(f"The new text has {left - right} letters less.")
        return left, right

    @staticmethod
    def count_letters_in_words(text, should_print=True):
        # excludes one letter words e, i etj.
        average_length = mean([len(word) for word in text.split(" ") if word.isalpha() and len(word) > 1])
        if should_print:
            print(f"The average length of a word is: {average_length:0.2f} letters.")
        return average_length

    @staticmethod
    def count_words_in_sentence(text):
        regex_for_only_one_full_stop = r"/(?<!\.)\.(?!\.)/"
        sentence_lengths = [len(sentence.split(" ")) for sentence in text.split(regex_for_only_one_full_stop)]
        average_sentence_length = mean(sentence_lengths)
        print(f"Average Sentence Length is: {average_sentence_length}")
        return average_sentence_length

    def number_of_pages_less(self, left_text, right_text):
        left = self.count_letters_in_words(left_text, should_print=False)
        right = self.count_letters_in_words(right_text, should_print=False)
        left_pages = left / self.DEFAULT_PAGE_SIZE
        right_pages = right / self.DEFAULT_PAGE_SIZE
        difference = left_pages - right_pages if left_pages - right_pages >= 1 else 0
        print(f"The page difference is {difference}.")
        return difference

    # def compute_relative_frequencies(self, text):
    #     relative_occurences = {}
    #     for word in text.split(" "):
    #         if word.isalpha() and len(word) > 1:
    #             for letter in word:


if __name__ == '__main__':
    with open("text.txt", "r") as file:
        raw_text = file.read()
        print(raw_text)
    processor = SqStatistics()
    formated_text = processor.replace_compound_characters(raw_text)
    print(formated_text)
    percentage_per_letter = processor.letter_percentage(formated_text)
    lenghts = processor.compare_lengths(text_left=raw_text, text_right=formated_text)
    processor.count_letters_in_words(text=formated_text)
    processor.count_words_in_sentence(text=formated_text)
    processor.number_of_pages_less(left_text=raw_text, right_text=formated_text)
