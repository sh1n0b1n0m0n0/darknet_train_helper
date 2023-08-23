from cProfile import label
from pathlib import Path
from typing import List
from tqdm import tqdm
import cv2
import glob
from os import PathLike
import fire
import yaml


def convert_darknet_to_pascal_voc(bbox, w, h):
    # bbox = center_x, center_y, width, heigth
    w_half_len = (float(bbox[2]) * w) / 2
    h_half_len = (float(bbox[3]) * h) / 2
    xmin = int((float(bbox[0]) * w) - w_half_len)
    ymin = int((float(bbox[1]) * h) - h_half_len)
    xmax = int((float(bbox[0]) * w) + w_half_len)
    ymax = int((float(bbox[1]) * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


def parse_darknet_txt(image_path: PathLike, txt_path: PathLike, obj_names, save_path):
    new_txt = Path(save_path) / (Path(txt_path).name)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width = image.shape[0], image.shape[1]

    with open(txt_path, "r") as f:
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


def main():
    labels_path = Path('/home/alexsh/yolov3/data/val/labels')
    images_path = Path('/home/alexsh/yolov3/data/val/images')
    config_path = Path('/home/alexsh/yolov3/data/configs/yolov3-tiny_20cls.yaml')

    save_path = Path(f'{labels_path.parent}/pascal_voc_ul_gt')
    save_path.mkdir(parents=True, exist_ok=True)

    obj_names = yaml.safe_load(open(Path.cwd() / Path(config_path)))["names"]
    imgs_list = []
    txts_list = []
    
    try:
        for txt in labels_path.glob('*.txt'):
            txts_list.append(str(txt))
    except ValueError:
            print("Dataset is Empty!")
    
    types = ["*.jp*g", "*.png"]
    for t in types:
        try:
            for img in images_path.glob(t):
                imgs_list.append(str(img))
        except ValueError:
            print("Dataset is Empty!")

    imgs_list.sort()
    txts_list.sort()
    print(len(imgs_list), len(txts_list))
    # for img, txt in tqdm(zip(imgs_list, txts_list), total=len(imgs_list)):
    #     parse_darknet_txt(img, txt, obj_names, save_path)


if __name__ == "__main__":
    fire.Fire(main)
