import json
from analyzers import get_analysis_data
from song_generator import generate_song
from words import save_example_words


if __name__ == '__main__':
    chain_length = 1
    tag = 'eppu_normaali_lyrics'

    print(f"TAG: {tag}")
    print(f"CHAIN LENGTH: {chain_length}")

    with open(f"data/analysis_results_{tag}_{chain_length}.json", encoding='utf-8') as f:
        analysis_data = json.load(f)

    while True:

        print(generate_song(analysis_data=analysis_data, chain_length=1))

        user_input = input(f"Press ENTER to generate more, s to save words to file, number to set chain length, q to quit...").strip().lower()

        try:
            chain_length = int(user_input)
            analysis_data = get_analysis_data(chain_length, tag)
            continue
        except ValueError:
            pass

        if user_input == 'q':
            break
        elif user_input == 's':
            save_example_words(analysis_data, chain_length, tag, 100)


