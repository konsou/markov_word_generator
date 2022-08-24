import random
from random import choice

from analyzers import get_analysis_data
from words import generate_word


def generate_finnish_first_name(gender: str, chain_length: int, analysis_data=None) -> str:
    tag = 'finnish_names_female' if gender == 'female' else 'finnish_names_male'
    if analysis_data is None:
        analysis_data = get_analysis_data(chain_length=chain_length, tag=tag)
    return generate_word(analysis_data=analysis_data, chain_length=chain_length).capitalize()


def generate_finnish_surname(chain_length: int, analysis_data=None) -> str:
    tag = 'finnish_names_surnames'
    if analysis_data is None:
        analysis_data = get_analysis_data(chain_length=chain_length, tag=tag)
    return generate_word(analysis_data=analysis_data, chain_length=chain_length).capitalize()


if __name__ == '__main__':
    chain_length = 2
    names_to_generate = 20
    male_analysis_data = get_analysis_data(chain_length=chain_length, tag='finnish_names_male')
    female_analysis_data = get_analysis_data(chain_length=chain_length, tag='finnish_names_female')
    surname_analysis_data = get_analysis_data(chain_length=chain_length + 1, tag='finnish_names_surnames')

    analysis_data_for_gender = {
        'male': male_analysis_data,
        'female': female_analysis_data,
    }

    names = []

    for _ in range(names_to_generate):
        gender = random.choice(['male', 'female'])
        first_name = generate_finnish_first_name(gender=gender,
                                                 chain_length=chain_length,
                                                 analysis_data=analysis_data_for_gender[gender])
        surname = generate_finnish_surname(chain_length=chain_length + 1, analysis_data=surname_analysis_data)

        names.append(f"{first_name} {surname}")

    print(", ".join(names))


