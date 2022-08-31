from pathlib import Path


def main():
    proj_names = ['80', '81', '82', '115', '116',
                  '118', '123', '146', '149', '234', '242', '95', '147']
    proj_path = '/home/alexsh/temp/rv_yolo_roi_test/'
    counter = 0
    sums = []
    for proj in range(len(proj_names)):
        # print(proj_names[proj])
        #print(Path(proj_path) / proj_names[proj])
        for txt in (Path(proj_path) / proj_names[proj]).glob("*.txt"):
            with open(txt, "r") as txt_file:
                lines = txt_file.readlines()
                for line in lines:
                    l = line.split()
                    # print(l)
                    counter += 1

        sums.append(counter)
        counter = 0
    print(sums)
    print(f'total = {sum(sums)}')


if __name__ == "__main__":
    main()
