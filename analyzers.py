import json
from collections import defaultdict, Counter
from os.path import isfile


def markov_analyze_letter_frequencies(input_json_filename: str, chain_length: int, tag: str):
    """Save markov analysis data_processed (not percents but numbers) to file"""

    print(f"Analyzing letter frequencies with Markov chain length {chain_length} - language {tag}")
    with open(input_json_filename, encoding='utf-8') as f:
        words = json.load(f)

    print(f"{len(words)} words loaded")

    i = 0

    results = defaultdict(Counter)

    for word in words:
        if not i % 1000:
            print(f"{i} words analyzed...")

        i += 1

        previous_letters = ""
        for current_letter in word:
            results[previous_letters][current_letter] += 1

            previous_letters += current_letter
            previous_letters = previous_letters[-chain_length:]

        results[previous_letters][""] += 1

    output_filename = f"data_processed/analysis_results_{tag}_{chain_length}.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, sort_keys=True, indent=4, ensure_ascii=False)

    print(f"Done.")


def markov_analyze_word_frequencies(chain_length: int, tag: str) -> None:
    """Save markov analysis data_processed (not percents but numbers) to file"""

    print(f"Analyzing words with Markov chain length {chain_length} - tag {tag}")
    with open(f"data_processed/{tag}.json", encoding='utf-8') as f:
        words = json.load(f)

    print(f"{len(words)} words loaded")

    i = 0

    results = defaultdict(Counter)

    previous_words = ""  # comma-separated - needs to be a str to be able to use as a dict key
    for current_word in words:
        if not current_word:
            continue

        if not i % 1000:
            print(f"{i} words analyzed...")

        i += 1

        results[previous_words][current_word] += 1

        print(f"previous words for {current_word} is: {previous_words}")
        previous_words = f"{previous_words},{current_word}"
        previous_words = ",".join(previous_words.split(",")[-chain_length:])
        print(f"previous words for {current_word} is now: {previous_words}")

    output_filename = f"data_processed/analysis_results_{tag}_{chain_length}.json"
    with open(output_filename, 'w') as f:
        json.dump(results, f, sort_keys=True, indent=4, ensure_ascii=False)

    print(f"Done.")


def get_analysis_data(chain_length, tag):
    analysis_data_filename = f"data_processed/analysis_results_{tag}_{chain_length}.json"

    if not isfile(analysis_data_filename):
        markov_analyze_letter_frequencies(input_json_filename=f"data_processed/{tag}.json",
                                          chain_length=chain_length,
                                          tag=tag)

    with open(analysis_data_filename, encoding='utf-8') as f:
        analysis_data = json.load(f)

    return analysis_data


if __name__ == '__main__':
    # markov_analyze_word_frequencies(1, tag='eppu_normaali_lyrics')
    tag = 'finnish_names_male'
    markov_analyze_letter_frequencies(input_json_filename=f'data_raw/{tag}.json',
                                      chain_length=1,
                                      tag=tag)

