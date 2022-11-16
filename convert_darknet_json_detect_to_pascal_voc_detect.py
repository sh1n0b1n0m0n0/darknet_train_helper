from pathlib import Path
from tqdm import tqdm
import cv2
import glob
from os import PathLike
import fire
import json


def convert_darknet_to_pascal_voc(bbox, w, h):
    # bbox = center_x, center_y, width, heigth
    w_half_len = (float(bbox[2]) * w) / 2
    h_half_len = (float(bbox[3]) * h) / 2
    xmin = int((float(bbox[0]) * w) - w_half_len)
    ymin = int((float(bbox[1]) * h) - h_half_len)
    xmax = int((float(bbox[0]) * w) + w_half_len)
    ymax = int((float(bbox[1]) * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


def parse_darknet_json(batch, save_path):
    image_path = batch["filename"]  # don't forget to iterate over data
    events = batch["objects"]

    txt_file = Path(image_path).with_suffix('.txt')
    new_txt = Path(save_path) / (
        f'{Path(image_path).parents[0].name}_' + Path(txt_file).name)

    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width = image.shape[0], image.shape[1]

    # print(image_path)
    # print(txt_file)
    # print(new_txt)
    with open(new_txt, "w") as f:
        if events != []:
            for event in events:
                # label = event["class_id"]
                label = event["name"]
                conf = event["confidence"]
                bbox = [event["relative_coordinates"]["center_x"],
                        event["relative_coordinates"]["center_y"],
                        event["relative_coordinates"]["width"],
                        event["relative_coordinates"]["height"]]

                # print(label, conf, bbox)

                res = convert_darknet_to_pascal_voc(bbox, width, height)
                string_list = list(map(str, res))
                string_line = str(label) + ' ' + str(conf) + \
                    ' ' + ' '.join(string_list)
                f.write(string_line)
                f.write('\n')


def main(
    file_path: PathLike,
    save_path: PathLike
):
    """
        Args:
            file_path (PathLike): path result.json
            save_path (PathLike): path to save
    """
    Path(save_path).mkdir(parents=True, exist_ok=True)

    with open(file_path, 'r') as f:
        data = json.load(f)
        for batch in tqdm(data):
            parse_darknet_json(batch, save_path)


if __name__ == "__main__":
    fire.Fire(main)
