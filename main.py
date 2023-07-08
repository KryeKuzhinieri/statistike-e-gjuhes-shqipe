import re
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

plt.rcParams["figure.figsize"] = (20, 9)
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"


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
        # print(sorted_result)
        return sorted_result

    @staticmethod
    def compare_lengths(text_left, text_right, should_print=True):
        left = len([x for x in text_left if x.isalpha()])
        right = len([x for x in text_right if x.isalpha()])
        percentage_smaller = ((left - right) / left) * 100
        if should_print:
            print(f"Text Left has a length of {left} whereas the right one a length of {right}.")
            print(f"The new text is {percentage_smaller:0.2f}% smaller.")
            print(f"The new text has {left - right} letters less.")
        return left, right

    @staticmethod
    def count_letters_in_words(text):
        # excludes one letter words e, i etj.
        average_length = mean([len(word) for word in text.split(" ") if word.isalpha() and len(word) > 1])
        print(f"The average length of a word is: {average_length:0.2f} letters.")
        return average_length

    @staticmethod
    def count_words_in_sentence(text):
        regex_for_only_one_full_stop = r"/(?<!\.)\.(?!\.)/"
        regex_for_only_one_full_stop = "(?<=[.!?]) +"
        sentence_lengths = [len(sentence.split(" ")) for sentence in re.split(regex_for_only_one_full_stop, text)]
        average_sentence_length = mean(sentence_lengths)
        print(f"Average Sentence Length is: {average_sentence_length}")
        return average_sentence_length

    def number_of_pages_less(self, left_text, right_text):
        left, right = self.compare_lengths(left_text, right_text, should_print=False)
        difference = (left - right) / self.DEFAULT_PAGE_SIZE
        print(f"The page difference is {difference}.")
        return difference

    def compute_relative_frequencies(self, text):
        relative_occurences = {}
        string_max_length = len(text)
        # Get the counts of each letter after the current letter.
        for letter in self.ALPHABET:
            letter_occurences = {ch: 0 for ch in self.ALPHABET}
            letter_postions = list(self.find_all(text, letter))
            for position in letter_postions:
                if position + 1 == string_max_length:
                    continue
                next_letter = text[position + 1]
                if not next_letter.isalpha() or next_letter not in self.ALPHABET:
                    continue
                letter_occurences[next_letter] += 1
            relative_occurences[letter] = letter_occurences

        # Compute percentages of each character.
        for k, v in relative_occurences.items():
            all_values = sum(v.values())
            if all_values == 0:
                continue
            for sub_k, sub_v in v.items():
                relative_occurences[k][sub_k] /= all_values

        # print(relative_occurences)
        return relative_occurences

    @staticmethod
    def find_all(s, c):
        idx = s.find(c)
        while idx != -1:
            yield idx
            idx = s.find(c, idx + 1)

    def plot_bar(self, data):
        reversed_chars = {v: k for k, v in self.COMPOUND_LETTERS.items()}
        labels = [reversed_chars[ch] if ch in reversed_chars.keys() else ch for ch in data.keys()]
        values = {
            "Përqindje e plotë": [data[k]["total"] for k, v in data.items()],
            "Përqindje e pjesshme (zanore me zanore / bashkëtingëllore me bashkëtingëllore)": [data[k]["partial"] for
                                                                                               k, v in data.items()]
        }
        bar_width = 0.2
        x_pos = np.arange(len(labels))
        fig, ax = plt.subplots()

        for i, (group, vals) in enumerate(values.items()):
            pos = x_pos + (i * bar_width)
            ax.bar(pos, vals, width=bar_width, label=group)

        ax.set_xticks(x_pos + ((len(values) - 1) / 2) * bar_width)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.set_xlabel('Germat')
        ax.set_ylabel('Përqindja')
        ax.set_title('Germat më të përdorura të gjuhës shqipe')
        plt.savefig("percentage_figure.png")
        plt.close()

    def plot_heatmat(self, data):
        reversed_chars = {v: k for k, v in self.COMPOUND_LETTERS.items()}
        names = [reversed_chars[ch] if ch in reversed_chars.keys() else ch for ch in data.keys()]
        matrix = [list(v.values()) for k, v in data.items()]
        df = pd.DataFrame(matrix, columns=names, index=names)
        # print(matrix)
        heatmap = sns.heatmap(df, cmap='coolwarm', annot=True, fmt='.1g')
        heatmap.xaxis.set_ticks_position("top")
        heatmap.xaxis.set_ticks_position("top")
        plt.title('Përqindja e germave pasuese', fontsize=13)
        plt.xlabel('Germa Pasuese', fontsize=13)
        plt.ylabel('Germa Paraprake', fontsize=13)
        plt.tight_layout()
        heatmap.figure.savefig("heatmap.png")


if __name__ == '__main__':
    with open("text.txt", "r") as file:
        raw_text = file.read()
        # print(raw_text)
    processor = SqStatistics()
    formated_text = processor.replace_compound_characters(raw_text)
    # print(formated_text)

    percentage_per_letter = processor.letter_percentage(formated_text)
    processor.plot_bar(percentage_per_letter)

    lenghts = processor.compare_lengths(text_left=raw_text, text_right=formated_text)

    processor.count_letters_in_words(text=formated_text)
    processor.count_words_in_sentence(text=formated_text)
    processor.number_of_pages_less(left_text=raw_text, right_text=formated_text)

    relative_frequencies = processor.compute_relative_frequencies(formated_text)
    processor.plot_heatmat(relative_frequencies)
