from pathlib import Path
from tqdm import tqdm
from os import PathLike
import fire


def rename_classes(project_path: PathLike, to_rename, rename):
    txt_file = Path(project_path).with_suffix('.txt')

    for txt_file in tqdm(Path(project_path).glob('*.txt')):
        with open(txt_file, "r") as f:
            line = f.read()
            # print(line)

        line = line.replace(str(to_rename), str(rename))
        with open(txt_file, "w") as f:
            f.write(line)

    print("Complete.\n")


def main(
    folder_path: PathLike,
    to_rename: str,
    rename: str
):
    """
        Args:
            folder_path (PathLike): path to folder with txts
            to_rename (String): class name you want to rename
            rename (String): new class name
    """

    rename_classes(folder_path, to_rename, rename)


if __name__ == "__main__":
    fire.Fire(main)
