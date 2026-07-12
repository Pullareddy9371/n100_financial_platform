from src.etl.loader import load_all_excels
from src.etl.validator import validate_dataset


def main():

    datasets = load_all_excels()

    for name, df in datasets.items():
        validate_dataset(name, df)


if __name__ == "__main__":
    main()