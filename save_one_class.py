from pathlib import Path
from tqdm import tqdm
import random
from os import PathLike
import fire
import shutil


def make_obj_data_file(new_project_folder):
    '''
        train = /<new_project_folder>/train.txt
        names = /<new_project_folder>/obj.names
        backup = /<new_project_folder>/backup
        classes = 1
    '''
    obj_data_path = Path(new_project_folder) / "obj.data"
    with open(obj_data_path, "w") as f:
        data = f"train = {new_project_folder}/train.txt\nnames = {new_project_folder}/obj.names\nbackup = {new_project_folder}/backup\nclasses = 1"
        f.write(data)


def make_obj_names_file(new_project_folder, class_name):
    '''
        class name
    '''
    obj_names_path = Path(new_project_folder) / "obj.names"
    with open(obj_names_path, "w") as f:
        f.write(class_name)


def class_remover(train_txt_path, obj_names, label):
    counter = 0
    empty_counter = 0
    new_images_list = []
    empty_list = []

    with open(obj_names, "r") as f:
        labels = f.read().splitlines()

    new_project_folder = Path(train_txt_path).parents[1]/f"rv_yolo_1cl_{labels[int(label)]}"
    new_project_folder.mkdir(parents=True, exist_ok=True)
    Path(new_project_folder / "backup").mkdir(parents=True, exist_ok=True)
    
    make_obj_names_file(new_project_folder, labels[int(label)])
    make_obj_data_file(new_project_folder)
    with open(train_txt_path, "r") as f:
        imgs = f.read().splitlines()

    txts = [Path(img).with_suffix('.txt') for img in imgs]

    for img, txt in tqdm(zip(imgs, txts), total=len(imgs)):
        new_txt_path = new_project_folder / Path(txt).parent.name / Path(txt).name
        new_image_path = new_project_folder / Path(img).parent.name / Path(img).name
        Path(new_txt_path.parent).mkdir(parents=True, exist_ok=True)
        # print(new_txt_path)
        with open(txt, "r") as f:
            txt_guts = f.read().splitlines()
            splited_txt = [item.split() for item in txt_guts]
        
        if len(splited_txt) == 0:
            empty_counter += 1

            shutil.copyfile(img, new_image_path)
            empty_list.append(new_image_path)

            with open(Path(new_image_path).with_suffix('.txt'), "w") as f:
                f.write("")
        else:
            for i in splited_txt:
                if int(i[0]) == int(label):
                    counter += 1
                    # print(txt_guts[splited_txt.index(i)], new_txt_path)

                    line = txt_guts[splited_txt.index(i)]
                    line = line.replace(str(label), str("0"), 1)

                    new_images_list.append(new_image_path)
                    shutil.copyfile(img, new_image_path)

                    with open(new_txt_path, "a") as ff:
                        ff.write(line)
                        ff.write('\n')

                    
    print(f"class {labels[int(label)]} - {int(label)}: {counter}")
    print(f"empty images: {empty_counter}")
    make_train_set_txt(new_images_list, empty_list, new_project_folder)


def make_train_set_txt(images, empty_images, new_project_folder):
    full_set = list(set(images + empty_images[:int(len(images)/2)]))
    random.shuffle(full_set)
    train_txt_dir = Path(new_project_folder) / "train.txt"

    with open(str(train_txt_dir), "w") as f:
        for img in full_set:
            f.write(str(img))
            f.write("\n")

    print(f"Number of not empty images: {len(images)}, number of empty images: {len(empty_images)}, batch of empty images for training: {len(empty_images[:int(len(images)/2)])}")


def main(
    txt_path: PathLike,
    obj_names: PathLike,
    label: str
):
    """
        Args:
            txt_path (PathLike): path to train.txt.
            obj_names (PathLike): path to obj.names
            label (string): 
    """

    if Path(txt_path).is_file() and Path(obj_names).is_file():
        class_remover(txt_path, obj_names, label)
    else:
        print(f"{txt_path} doesn't exist.")


if __name__ == "__main__":
    fire.Fire(main)
