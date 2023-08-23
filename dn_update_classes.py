import inexlib.object_detection.darknet as dn
from pathlib import Path
import sys


def main():
    # cfg_file_path: Path, n_classes: int, new_cfg_file_path: Path
    try:
        cfg_file_path, n_classes, new_cfg_file_path = sys.argv[1:]
        cfg_file_path = Path(cfg_file_path)
        n_classes = int(n_classes)
    except:  # noqa: E722
        print("Usage: cfg_file_path n_classes new_cfg_file_path")
        exit(0)
    assert cfg_file_path.is_file()
    assert n_classes >= 1
    print(f"Reading from {cfg_file_path}...")
    net = dn.from_darknet_config_file(cfg_file_path)
    print("...done")
    print(f"Writing to {new_cfg_file_path}...")
    dn.to_darknet_config_file(dn.set_classes(net, n_classes), new_cfg_file_path)
    print("...done")

if __name__ == "__main__":
    main()
