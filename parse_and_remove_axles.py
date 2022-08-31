from pathlib import Path

def parse_and_remove_axles(txt_list):
    for txt_file in txt_list:

        width = 960
        height  = 540

        with open(txt_file, "r") as f:
            lines = f.readlines()

        with open(txt_file, "w") as f:
            for line in lines:
                l = list(line.split())
                if (l[0] == '12') & ((float(l[3]) * width) < 16) | ((float(l[4]) * height) < 16):
                    print(l, (float(l[3]) * width), (float(l[4]) * height))
                    continue
                else:
                    f.write(line)

def main():
    root = Path("/home/alexsh/temp/rv_yolo_16cl/234/")
    txt_list = list(root.glob('**/*.txt')) 

    parse_and_remove_axles(txt_list)


if __name__ == "__main__":
    main()