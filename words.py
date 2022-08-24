from random import choices
from analyzers import get_analysis_data


def generate_word(analysis_data, chain_length):
    previous_letter = ""
    word = ""
    while True:
        next_letter_frequencies = analysis_data[previous_letter]

        letters = []
        weights = []

        for letter, weight in next_letter_frequencies.items():
            letters.append(letter)
            weights.append(weight)

        chosen_letter = choices(letters, weights)[0]
        word = f"{word}{chosen_letter}"

        previous_letter += chosen_letter
        previous_letter = previous_letter[-chain_length:]
        if chosen_letter == "":
            break

    return word


def save_example_words(analysis_data, chain_length, language, number_of_words):
    words = []

    for _ in range(number_of_words):
        words.append(generate_word(analysis_data, chain_length))

    output_filename = f'example_words_{language}_{chain_length}.txt'

    with open(output_filename, 'w') as f:
        for word in words:
            f.write(f"{word}\n")

    print(f"{number_of_words} words saved to {output_filename}")


if __name__ == '__main__':
    chain_length = 2
    tag = 'finnish_names_female'
    words_to_generate = 20
    analysis_data = get_analysis_data(chain_length=chain_length, tag=tag)
    #print(analysis_data)
    words = []
    for _ in range(words_to_generate):
        words.append(generate_word(analysis_data=analysis_data, chain_length=chain_length).capitalize())
    print(words)

    with open(f'example_output/example_{tag}.txt', 'w', encoding='utf-8') as f:
        for w in words:
            f.write(f"{w}\n")
