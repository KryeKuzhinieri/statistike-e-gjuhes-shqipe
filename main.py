import re


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
    # def __init__(self, raw_text):
    #     self.text = raw_text

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
        return sorted_result

    @staticmethod
    def compare_lengths(text_left, text_right):
        left = len([x for x in text_left if x.isalpha()])
        right = len([x for x in text_right if x.isalpha()])
        print(f"Text Left has a length of {left} whereas the right one a length of {right}.")
        percentage_smaller = abs(left - right) / max(left, right)
        print(percentage_smaller)
        return left, right


if __name__ == '__main__':
    with open("text.txt", "r") as file:
        text = file.read()
        print(text)
    processor = SqStatistics()
    formated_text = processor.replace_compound_characters(text)
    print(formated_text)
    percentage_per_letter = processor.letter_percentage(formated_text)
    print(percentage_per_letter)
    lenghts = processor.compare_lengths(text_left=text, text_right=formated_text)
