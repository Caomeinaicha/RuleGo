import os
import sys

# ===== 基础配置 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "Module")
OUTPUT_DIR = os.path.join(BASE_DIR, "Rewrite")

VALID_EXT = (".list", ".conf", ".sgmodule", ".txt", ".ruleset")

# ===== 行处理 =====
def process_line(line):
    line = line.strip()
    if not line or line[0] in "#;[/":
        return None, False

    is_reject = "- reject" in line

    if "%APPEND% " in line:
        line = line.replace("%APPEND% ", "")

    if is_reject:
        line = line.replace("- reject", "url reject")

    return line, is_reject

def count_hostname(line):
    line_lower = line.lower()

    if "hostname" not in line_lower:
        return 0

    pos = line_lower.find("hostname")
    eq_pos = line.find("=", pos)

    if eq_pos == -1:
        return 0

    try:
        content = line[eq_pos + 1:]
        return sum(1 for h in content.split(",") if h.strip())
    except:
        return 0


# ===== 文件处理 =====
def process_file(file_name):
    src_path = os.path.join(SOURCE_DIR, file_name)
    dst_path = os.path.join(OUTPUT_DIR, file_name)

    total_reject = 0
    total_host = 0
    has_output = False

    results = []

    with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            result, is_reject = process_line(raw_line)

            if result:
                results.append(result)
                has_output = True

                if "hostname" in result.lower():
                    total_host += count_hostname(result)

                if is_reject:
                    total_reject += 1

    with open(dst_path, "w", encoding="utf-8") as out:
        for i, item in enumerate(results):
            if i == len(results) - 1:
                out.write(item)
            else:
                out.write(item + "\n")

    return has_output, total_reject, total_host


# ===== 主流程 =====
def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(SOURCE_DIR):
        print(f"错误：找不到目录 {SOURCE_DIR}")
        return

    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(VALID_EXT)]

    if not files:
        print("未找到规则文件")
        return

    print(">>> 处理 Rewrite 规则...\n")

    for name in files:
        try:
            ok, reject, host = process_file(name)
            if ok:
                print(f"[完成] {name}")
                print(f"       └─ reject: {reject} | hostname: {host}")
            else:
                print(f"[跳过] {name}")
        except Exception as e:
            print(f"[错误] {name}: {e}")


if __name__ == "__main__":
    run()
    if len(sys.argv) == 1:
        print("\n--- 完成 ---")
        input("回车退出...")