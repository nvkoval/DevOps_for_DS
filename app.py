from vetiver import VetiverModel, VetiverAPI
from pins import board_folder


b = board_folder('./data/model', allow_pickle_read=True)
v = VetiverModel.from_pin(b, 'penguin_model',
                          version='20240923T232941Z-bdd5f')

vetiver_api = VetiverAPI(v)
api = vetiver_api.app
