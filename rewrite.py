
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCE_FILE = os.path.join(
    BASE_DIR, "Surge", "Module", "Block", "Advertising.sgmodule"
)

OUTPUT_DIR = os.path.join(BASE_DIR, "Quantumult", "Rewrite")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Advertising.snippet")


def process_line(line):
    if line == "" or line.lstrip().startswith("#"):
        return line

    if line.startswith("["):
        return "#" + line

    line = line.replace("%APPEND% ", "")
    line = line.replace(" - reject", " url reject")

    return line


def convert_file():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.isfile(SOURCE_FILE):
        print(f"找不到源文件：{SOURCE_FILE}")

        if os.path.isfile(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
            print("[清理] 删除旧文件 Advertising.snippet")

        return 0

    with open(SOURCE_FILE, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    result = [process_line(line) for line in lines]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        if result:
            f.write("\n".join(result) + "\n")

    print("[完成] Advertising.sgmodule -> Advertising.snippet")

    return 0


def main():
    try:
        return convert_file()

    except Exception as e:
        print(f"[错误] Advertising.sgmodule: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
