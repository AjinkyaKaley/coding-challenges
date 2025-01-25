
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ccwc",description="program that emulates word count")
    parser.add_argument("file_name", type=str)
    parser.add_argument("-c", "--count", action="store_true", default=True)
    parser.add_argument("-l", "--lines",action="store_true", default=True)
    parser.add_argument("-w", "--words", action="store_true", default=True)
    parser.add_argument("-m", "--chars", action="store_true", default=True)

    args = parser.parse_args()
    file_name = args.file_name
    bytes = 0
    line_num = 0
    word_count = 0
    _chars = 0
    if args.count:
        bytes = os.path.getsize(file_name)
    if args.lines:
        with open(file_name, "r") as f:
            line_num = 0
            while f.readline():
                line_num+=1
    if args.words:
        with open(file_name, "r") as f:
            word_count = 0
            lines = f.readlines()
            for line in lines:
                words = line.split()
                word_count += len(words)
    if args.chars:
        with open(file_name, "r") as f:
            lines = f.readlines()
            _chars = set()
            for line in lines:
                words = line.split()
                for word in words:
                    for c in word:
                        _chars.add(c)
    print(f"{bytes} {line_num} {word_count} {len(_chars)} {file_name}")