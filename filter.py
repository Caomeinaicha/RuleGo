
import os
import sys
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCE_DIR = os.path.join(BASE_DIR, "Surge", "Ruleset")
OUTPUT_DIR = os.path.join(BASE_DIR, "Quantumult", "Filter")

VALID_EXT = (".list", ".conf", ".txt", ".ruleset")


def process_line(line, tag):
    stripped = line.strip()

    if not stripped or stripped.startswith(("#", ";", "[")):
        return line.rstrip("\r\n"), False

    line = line.split("//", 1)[0]
    parts = [part.strip() for part in line.split(",", 2)]

    if len(parts) < 2:
        return line.rstrip("\r\n"), False

    if parts[0].upper() == "IP-CIDR6":
        parts[0] = "IP6-CIDR"

    return f"{parts[0]},{parts[1]},{tag}", True


def convert_file(src_path, dst_path, tag):
    count = 0

    with open(src_path, "r", encoding="utf-8", errors="ignore") as f, \
         open(dst_path, "w", encoding="utf-8", newline="\n") as out:

        first_line = True

        for raw_line in f:
            result, is_rule = process_line(raw_line, tag)

            if not first_line:
                out.write("\n")

            out.write(result)

            if is_rule:
                count += 1

            first_line = False

    return count


def clean_output():
    cleaned = 0

    if not os.path.isdir(OUTPUT_DIR):
        return cleaned

    for entry in os.listdir(OUTPUT_DIR):
        full = os.path.join(OUTPUT_DIR, entry)

        if os.path.isfile(full):
            os.remove(full)
            cleaned += 1
            print(f"[清理] 删除旧文件 {entry}")

        elif os.path.isdir(full):
            shutil.rmtree(full)
            cleaned += 1
            print(f"[清理] 删除旧子目录 {entry}/")

    return cleaned


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.isdir(SOURCE_DIR):
        print(f"找不到源目录：{SOURCE_DIR}")
        cleaned = clean_output()
        print(f"[完成] 清理旧输出 {cleaned} 项")
        return 0

    total_files = 0
    total_rules = 0
    has_error = False
    produced = set()
    seen_sources = {}

    for root, dirs, files in os.walk(SOURCE_DIR):
        dirs.sort()

        for name in sorted(files):
            if not name.lower().endswith(VALID_EXT):
                continue

            src_path = os.path.join(root, name)
            rel_path = os.path.relpath(src_path, SOURCE_DIR)

            dst_name = name
            dst_path = os.path.join(OUTPUT_DIR, dst_name)
            tag = os.path.splitext(name)[0]

            if dst_name in seen_sources:
                print(
                    f"[警告] 文件名冲突: {rel_path} 与 "
                    f"{seen_sources[dst_name]} 都输出为 {dst_name}，后者将覆盖前者"
                )

            seen_sources[dst_name] = rel_path

            try:
                count = convert_file(src_path, dst_path, tag)

                if count:
                    total_files += 1
                    total_rules += count
                    produced.add(dst_name)

                    print(f"[完成] {rel_path} -> {dst_name} (提取 {count} 条)")

                else:
                    if os.path.exists(dst_path):
                        os.remove(dst_path)

                    print(f"[跳过] {rel_path} (无匹配规则)")

            except Exception as e:
                print(f"[错误] {rel_path}: {e}")
                has_error = True

    cleaned = 0

    for entry in os.listdir(OUTPUT_DIR):
        full = os.path.join(OUTPUT_DIR, entry)

        if os.path.isfile(full):
            if entry not in produced:
                os.remove(full)
                cleaned += 1
                print(f"[清理] 删除旧文件 {entry}")

        elif os.path.isdir(full):
            shutil.rmtree(full)
            cleaned += 1
            print(f"[清理] 删除旧子目录 {entry}/")

    print(f"\n共处理 {total_files} 个文件，生成 {total_rules} 条规则")

    if cleaned:
        print(f"清理旧输出 {cleaned} 项")

    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
