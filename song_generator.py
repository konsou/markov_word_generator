from random import choices


def generate_song(analysis_data, chain_length):
    previous_words = "NEWSONG"
    song = ""
    while True:
        print(f"previous words are: {previous_words}")
        next_word_frequencies = analysis_data[previous_words]

        words = []
        weights = []

        for word, weight in next_word_frequencies.items():
            words.append(word)
            weights.append(weight)

        chosen_word = choices(words, weights)[0]
        print(chosen_word)
        song = f"{song} {chosen_word}"

        previous_words = f"{previous_words},{chosen_word}"
        previous_words = ",".join(previous_words.split(",")[-chain_length:])
        # print(next_word_frequencies)
        # print(words)
        # print(weights)
        if chosen_word == "NEWSONG":
            break

    return song
