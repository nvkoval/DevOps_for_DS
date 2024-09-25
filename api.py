from pins import board_folder
from vetiver import VetiverModel, prepare_docker


# Save to Board
model_board = board_folder(
    "./data/model",
    allow_pickle_read=True
)

vetiver_model = VetiverModel.from_pin(model_board, 'penguin_model',
                                      version='20240923T232941Z-bdd5f')

prepare_docker(model_board, 'penguin_model')
