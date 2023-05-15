from model.data_handler import DataHandler
from model.utils import Utils
from view.gui import GUI

def main():
    (
        FILE_IN,
        TITLE_LABEL,
        FRAMES_PER_ENTRY,
        NUM_VISIBLE,
        PROD,
        FILE_OUT,
    ) = Utils.parse_args()

    data_handler = DataHandler(FILE_IN, NUM_VISIBLE)

    gui = GUI(data_handler, TITLE_LABEL, FRAMES_PER_ENTRY, NUM_VISIBLE, PROD, FILE_OUT)
    gui.run()

if __name__=="__main__":
    main()
