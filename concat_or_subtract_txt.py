from os import PathLike
from pathlib import Path
import fire
import shutil


def main(
    file_1: PathLike,
    file_2: PathLike,
    file_output: PathLike,
    concat=False,
    sub=False

):
    """
        Args:
            file_1 (PathLike): path to txt
            file_2 (PathLike): path to txt
            file_output (PathLike): path to txt
            concat (bool): if you want to concatenate file_1 with file_2
            sub (bool): if you want to subtract file_2 from file_1 (len(file_1) > len(file_2))
    """
    if concat is True:
        files = [file_1, file_2]
        with open(file_output, 'w') as new_file:
            for file in files:
                with open(file) as f:
                    for line in f:
                        new_file.write(line)
                new_file.write('\n')

    elif sub is True:
        with open(file_1, "r") as file_1_input:
            a = set(file_1_input.readlines())

        with open(file_2, "r") as file_2_input:
            b = set(file_2_input.readlines())

        with open(file_output, 'w') as new_file:
            for line in (a - b):
                new_file.write(line)


if __name__ == "__main__":
    fire.Fire(main)
