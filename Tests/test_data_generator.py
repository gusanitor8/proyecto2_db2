from model.data_generator import DataGenerator
def test_data_generator():
    dg = DataGenerator(10000, 3000, 1000, 1000)
    dg.run()
