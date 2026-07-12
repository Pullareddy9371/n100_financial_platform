from src.etl.loader import load_all_excels


def test_load_all_excels():

    datasets = load_all_excels()

    assert len(datasets) == 12