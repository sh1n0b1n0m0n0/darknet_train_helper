from pathlib import Path
from tqdm import tqdm
import cv2
from os import PathLike
import fire
import yaml


def remove_small_boxes(dataset_path: PathLike, number_of_classes: int, resize: int):
    list_of_images = []
    types = ["*.jp*g", "*.png"]
    for t in types:
        try:
            for img in Path(dataset_path).glob(t):
                list_of_images.append(str(img))
        except ValueError:
            print("Dataset is Empty!")

    list_of_images.sort()
    image = cv2.imread(list_of_images[0], cv2.IMREAD_UNCHANGED)
    height, width, _ = image.shape
    # print(image.shape)
    list_of_classes = [str(n) for n in range(number_of_classes)]
    for txt_file in tqdm(Path(dataset_path).glob('*.txt')):
        with open(txt_file, "r") as f:
            lines = f.readlines()

        with open(txt_file, "w") as f:
            for line in lines:
                dn_coords = list(line.split())
                if (dn_coords[0] in list_of_classes) & \
                   (((round(float(dn_coords[3]) * width) * resize / width)) < (resize * 0.02)) | \
                   (((round(float(dn_coords[4]) * height) * resize / height)) < (resize * 0.02)):
                    # print("before resize =", round(
                    #    float(dn_coords[3]) * width), round(float(dn_coords[4]) * height))
                    # print("after resize =", round((float(dn_coords[3]) * width) * resize / width), round(
                    #     (float(dn_coords[4]) * height) * resize / height))
                    print(line)
                    continue
                else:
                    f.write(line)
    print("Complete.\n")


def main():
    classes = 18
    resize = 416
    params = yaml.safe_load(open(Path.cwd() / Path("params.yaml")))["prepare"]
    paths = yaml.safe_load(open(Path.cwd() / Path("paths.yaml")))["train"]
    datasets = params["datasets"]
    data_root = paths["datasets_root"]
    
    if params["remove_small_boxes"]:
        print("Small boxes removed!\n")
        for dataset in datasets:
            remove_small_boxes(Path(data_root) / str(dataset), classes, resize)
    else:
        print("Small boxes are not removed!\n")


if __name__ == "__main__":
    fire.Fire(main)
