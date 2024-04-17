from model.data_generator import DataGenerator
def test_data_generator():
    dg = DataGenerator(10000, 30, 10, 10)
    dg.run()
