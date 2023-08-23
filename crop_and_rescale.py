import cv2
import yaml
from os import PathLike
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fire
from tqdm import tqdm


def make_imgs_list(dataset_path: PathLike):
    result = []
    types = ["*.jp*g", "*.png"]

    for t in types:
        try:
            for img in Path(dataset_path).glob(t):
                result.append(str(img))
        except ValueError:
            print("Dataset is Empty!")
        
    return result


def to_cv_coords(img, 
                 rect, 
                 scale_ratio_h, 
                 scale_ratio_w, 
                 crop_x1, 
                 crop_y1, 
                 crop_x2, 
                 crop_y2):
    
    height, width, _ = img.shape
    x = float(rect[1]) * width
    y = float(rect[2]) * height
    w = float(rect[3]) * width
    h = float(rect[4]) * height
    
    x1 = (x - w/2) * scale_ratio_w - crop_x1
    y1 = (y - h/2) * scale_ratio_h - crop_y1
    x2 = (x + w/2) * scale_ratio_w - crop_x1
    y2 = (y + h/2) * scale_ratio_h - crop_y1
    
    return max(0,int(x1)), max(0,int(y1)), max(0,int(x2)), max(0,int(y2))


def to_darknet_coords(img, rect):
    height, width, _ = img.shape
    x1, y1, x2, y2 = rect
    
    x = ((x2 + x1)/2)/width
    y = ((y2 + y1)/2)/height
    w = (x2 - x1)/width
    h = (y2 - y1)/height
    
    return float(x), float(y), float(w), float(h)


def plot_img(img_path,
             crop_x1: int = 0,
             crop_y1: int = 0,
             crop_x2: int = 0,
             crop_y2: int = 0
            ):
    
    input_img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    height, width, channels = input_img.shape
    
    # input_img[y:y+h, x:x+w] -> input_img[y1:y2, x1:x2]
    cropped_image = input_img[crop_y1:(height-crop_y2), crop_x1:(width-crop_x2)]
    c_height, c_width, c_channels = cropped_image.shape
    
    print(f"original img = {height}:{width}:{channels}")
    print(f"cropped img = {c_height}:{c_width}:{c_channels}")
    
    scale_ratio_w = width/c_width
    scale_ratio_h = height/c_height
    
    txt_path = Path(img_path).with_suffix(".txt")
    
    with open(str(txt_path), "r") as f:
        lines = f.read().splitlines()

    dn_coords = [line.split() for line in lines]
    
    for i in range(len(dn_coords)):
        x1, y1, x2, y2 = to_cv_coords(cropped_image, 
                                      dn_coords[i], 
                                      scale_ratio_h, 
                                      scale_ratio_w, 
                                      crop_x1, 
                                      crop_y1, 
                                      crop_x2, 
                                      crop_y2)
        print(x1, y1, x2, y2)
        cv2.rectangle(cropped_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    plt.imshow(cropped_image)
    plt.show()
    #return encoded_image.tobytes()
    
    
def rescale(img_path: PathLike,
            new_path: PathLike,
            crop_x1: int,
            crop_y1: int,
            crop_x2: int,
            crop_y2: int,
            limiter: int
           ):
    
    new_path.mkdir(parents=True, exist_ok=True)
    input_img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    height, width, channels = input_img.shape
    
    # input_img[y:y+h, x:x+w] -> input_img[y1:y2, x1:x2]
    cropped_image = input_img[crop_y1:(height-crop_y2), crop_x1:(width-crop_x2)]
    c_height, c_width, _ = cropped_image.shape
    
    scale_ratio_w = width/c_width
    scale_ratio_h = height/c_height
    
    txt_path = Path(img_path).with_suffix(".txt")
    new_txt_path = Path(new_path / img_path.name).with_suffix(".txt")
    
    with open(str(txt_path), "r") as f:
        lines = f.read().splitlines()

    dn_coords = [line.split() for line in lines]
    
    with open(new_txt_path, "w") as f:
        for i in range(len(dn_coords)):
            label = dn_coords[i][0] # the first element of the array is the class label
            x1, y1, x2, y2 = to_cv_coords(cropped_image, 
                                          dn_coords[i], 
                                          scale_ratio_h, 
                                          scale_ratio_w, 
                                          crop_x1, 
                                          crop_y1, 
                                          crop_x2, 
                                          crop_y2)
            
            x, y, w, h = to_darknet_coords(cropped_image, [x1, y1, x2, y2])
            if ((c_width - x1) > limiter) & ((c_height - y1) > limiter) & (x2 > limiter) & (y2 > limiter) & ([x1, y1, x2, y2].count(0) <= 2):
                f.write(label +" "+str(x)+" "+str(y)+" "+str(w)+" "+str(h))
                f.write("\n")
            
    cv2.imwrite(str(new_path / img_path.name), cropped_image)


def main(cvat_task: str,
         conf_path: PathLike,
         data_dir: PathLike
         ):
    """
        Args:
            cvat_task (str): path to configure file
            conf_path (PathLike): 
            data_dir (PathLike): 
    """
    # cvat_task = "twinforks"
    # conf_path = Path("D:/projects/cut_by_roi/datasets.yaml")
    # data_dir = Path("/home/alexsh/inex_datasets/data_darknet")

    crop_x1 = 400 # crop left pixel
    crop_y1 = 200 # crop top pixel
    crop_x2 = 0 # crop right pixel
    crop_y2 = 0 # crop bottom pixel
    limiter = 50 # 50 pixel limit for each side of the image

    params = yaml.safe_load(open(Path(conf_path)))["cvat_tasks"]
    data = params[cvat_task]
    task_id = [str(task["id"]) for task in data]

    for task_name in tqdm(task_id):
        proj_path = Path(data_dir) / task_name
        img_list = make_imgs_list(proj_path)
        
        if img_list:
            for img in img_list:
                img_path = Path(img)
                new_path = img_path.parents[1] / f"cropped_{img_path.parents[0].name}"
                rescale(img_path, new_path, crop_x1, crop_y1, crop_x2, crop_y2, limiter)


if __name__ == "__main__":
    fire.Fire(main)