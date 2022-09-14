from pathlib import Path
from tqdm import tqdm
import random
from os import PathLike
import fire
import shutil
import pandas as pd


def class_remover(train_txt_path, obj_names):
    empty_counter = 0
    temp_dict = {}
    classes_list = []

    with open(obj_names, "r") as f:
        labels = f.read().splitlines()
    labels_dict = dict(enumerate(labels))

    print(labels_dict)

    with open(train_txt_path, "r") as f:
        imgs = f.read().splitlines()
    
    temp_dict.update({"all_images": len(imgs)})

    txts = [Path(img).with_suffix('.txt') for img in imgs]

    for img, txt in zip(imgs, txts):
        with open(txt, "r") as f:
            txt_guts = f.read().splitlines()
            splited_txt = [item.split() for item in txt_guts]

        if len(splited_txt) == 0:
            empty_counter+=1
            temp_dict.update({"empty_images": empty_counter})
        else:
            for i in splited_txt:
                if i[0] != "\n":
                    classes_list.append(int(i[0]))
    
    classes_list.sort()
    counted_classes = {labels_dict[elem]: classes_list.count(elem) for elem in tqdm(classes_list)}
    df_classes = pd.DataFrame({"class": list(counted_classes.keys()), "amount": list(counted_classes.values())})

    print("\n")
    for key, value in temp_dict.items():
        print(key, value)

    print(df_classes)
    print("\nMax values: ")
    print(df_classes.nlargest(18, "amount"))



def main(
    txt_path: PathLike,
    obj_names: PathLike,
):
    """
        Args:
            txt_path (PathLike): path to train.txt.
            obj_names (PathLike): path to obj.names
    """

    if Path(txt_path).is_file() and Path(obj_names).is_file():
        class_remover(txt_path, obj_names)
    else:
        print(f"{txt_path} doesn't exist.")


if __name__ == "__main__":
    fire.Fire(main)
