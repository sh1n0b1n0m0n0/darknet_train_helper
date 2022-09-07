from cProfile import label
from pathlib import Path
from typing import List
from tqdm import tqdm
import cv2
import glob
from os import PathLike
import fire


def convert_darknet_to_pascal_voc(bbox, w, h):
    # bbox = center_x, center_y, width, heigth
    w_half_len = (float(bbox[2]) * w) / 2
    h_half_len = (float(bbox[3]) * h) / 2
    xmin = int((float(bbox[0]) * w) - w_half_len)
    ymin = int((float(bbox[1]) * h) - h_half_len)
    xmax = int((float(bbox[0]) * w) + w_half_len)
    ymax = int((float(bbox[1]) * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


def parse_darknet_txt(image_path: PathLike, obj_names):
    txt_file = Path(image_path).with_suffix('.txt')
    new_txt = Path(image_path).parents[1] / 'pascal_voc_gt' / (
        f'{Path(image_path).parents[0].name}.' + Path(txt_file).name)
    # print(txt_file)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width = image.shape[0], image.shape[1]
    # print(height, width)
    # print(f'{Path(image_path).parents[0].name}.' + Path(txt_file).name)
    # print(Path(image_path).parents[1]/'pascal_voc_gt' /
    #       (f'{Path(image_path).parents[0].name}.' + Path(txt_file).name))
    with open(txt_file, "r") as f:
        lines = f.readlines()

    with open(new_txt, "w") as f:
        for line in lines:
            dn_coords = list(line.split())
            id = int(dn_coords[0])
            label = obj_names[id]
            res = convert_darknet_to_pascal_voc(dn_coords[1:], width, height)
            string_list = list(map(str, res))
            string_line = label + ' ' + ' '.join(string_list)
            f.write(string_line)
            f.write('\n')


def main(
    file_path: PathLike,
    names: PathLike
):
    """
        Args:
            file_path (PathLike): path to valid.txt
            names (PathLike): path to obj.names
    """

    Path(f'{Path(file_path).parent}/pascal_voc_gt').mkdir(parents=True, exist_ok=True)
    with open(names, "r") as f:
        obj_names = f.read().splitlines()
        # print(obj_names)

    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        for line in tqdm(lines):
            parse_darknet_txt(line, obj_names)


if __name__ == "__main__":
    fire.Fire(main)
