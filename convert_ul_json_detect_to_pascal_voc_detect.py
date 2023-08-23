from pathlib import Path
from tqdm import tqdm
import cv2
import glob
from os import PathLike
import fire
import json
import yaml


def parse_ul_yolo_json(batch, obj_names, save_path):
    image_path = batch["filename"]  # don't forget to iterate over data

    new_txt = Path(save_path) / (f'{Path(image_path)}.txt')

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


def main():
    config_path = Path('/home/alexsh/yolov3/data/configs/yolov3-tiny_20cls.yaml')
    labels_path = Path('/home/alexsh/yolov3/data/val/labels')
    result_path = Path('/home/alexsh/yolov3/runs/val/exp2/best_predictions.json')

    save_path = Path(f'{labels_path.parent}/pascal_voc_ul_det')
    save_path.mkdir(parents=True, exist_ok=True)

    obj_names = yaml.safe_load(open(Path.cwd() / Path(config_path)))["names"]

    with open(result_path, "r") as f:
        data = json.load(f)
        for batch in tqdm(data):
            parse_ul_yolo_json(batch, obj_names, save_path)


if __name__ == "__main__":
    fire.Fire(main)
