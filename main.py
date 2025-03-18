from model.data_handler import DataHandler
from model.utils import Utils
from view.gui import GUI


def main(
    file_in: str,
    title_label: str,
    frames_per_timestamp: int,
    num_visible: int,
    prod: bool,
    file_out: str,
):
    data_handler = DataHandler(filename=file_in, num_visible=num_visible)

    gui = GUI(
        data_handler=data_handler,
        title_label=title_label,
        frames_per_entry=frames_per_timestamp,
        num_visible=num_visible,
        prod=prod,
        file_out=file_out,
    )

    gui.run()


if __name__ == "__main__":
    args = Utils.parse_args()

    main(*args)
