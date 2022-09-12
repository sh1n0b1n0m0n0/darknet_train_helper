from pathlib import Path
from tqdm import tqdm
import cv2
import glob
from os import PathLike
import fire
import json


def parse_ul_yolo_json(file_path, batch, obj_names):
    image_path = batch["filename"]  # don't forget to iterate over data

    new_txt = Path(file_path).parent / 'pascal_voc_ul_detect' / (
        f'{Path(image_path)}.txt')

    with open(new_txt, "a") as f:
        label = batch["class_id"]
        conf = batch["confidence"]
        bbox = batch["bbox"]
        id = int(label)
        label = obj_names[id]
        string_list = list(map(str, bbox))
        string_line = str(label) + ' ' + str(conf) + \
            ' ' + ' '.join(string_list)
        f.write(string_line)
        f.write('\n')


def main(
    file_path: PathLike,
    names: PathLike
):
    """
        Args:
            file_path (PathLike): path result.json
            names (PathLike): path to obj.names
    """
    Path(f'{Path(file_path).parent}/pascal_voc_ul_detect').mkdir(parents=True, exist_ok=True)
    with open(names, "r") as f:
        obj_names = f.read().splitlines()
        # print(obj_names)

    with open(file_path, "r") as f:
        data = json.load(f)
        for batch in tqdm(data):
            parse_ul_yolo_json(file_path, batch, obj_names)


if __name__ == "__main__":
    fire.Fire(main)
