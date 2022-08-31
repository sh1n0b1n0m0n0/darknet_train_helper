from pathlib import Path
from tqdm import tqdm
import cv2
from inexlib.utils.file_system import list_folder_files_with_extension
from os import PathLike
import fire


def remove_small_boxes(project_path: PathLike, number_of_classes: int, resize: int):
    list_of_images = list_folder_files_with_extension(
        project_path, ["*.jp*g", "*.png"])
    image = cv2.imread(list_of_images[0].as_posix(), cv2.IMREAD_UNCHANGED)
    height, width, _ = image.shape
    # print(image.shape)
    list_of_classes = [str(n) for n in range(number_of_classes)]
    for txt_file in tqdm(Path(project_path).glob('*.txt')):
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


def main(
    folder_path: PathLike
):
    """
        Args:
            folder_path (PathLike): path to train data.
    """
    # root = "/home/alexsh/temp/rv_yolo_18cl/291/"

    classes = 18
    resize = 416
    remove_small_boxes(folder_path, classes, resize)


if __name__ == "__main__":
    fire.Fire(main)
