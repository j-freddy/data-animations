import numpy as np

from model.const import FILEPATH
from model.data_handler import DataHandler
from view.gui import GUI

def main():
    data_handler = DataHandler(FILEPATH)

    gui = GUI(data_handler)
    gui.run()

if __name__=="__main__":
    main()
