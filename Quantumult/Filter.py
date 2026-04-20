import os
import sys

# ===== 基础配置 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "Ruleset")
OUTPUT_DIR = os.path.join(BASE_DIR, "Filter")

VALID_EXT = (".list", ".conf", ".txt", ".ruleset")

RULE_MAP = {
    "DOMAIN-SUFFIX": "host-suffix",
    "DOMAIN-KEYWORD": "host-keyword",
    "DOMAIN-WILDCARD": "host-wildcard",
    "DOMAIN": "host",
    "IP-CIDR": "ip-cidr",
    "IP-CIDR6": "ip6-cidr",
    "IP-ASN": "ip-asn",
    "GEOIP": "geoip",
    "USER-AGENT": "user-agent"
}


# ===== 行处理 =====
def process_line(line, tag, rule_map):
    line = line.strip()
    if not line or line[0] in "#;[/":
        return None

    pos = line.find(",")
    if pos == -1:
        return None

    raw_type = line[:pos].strip()
    key = raw_type.upper()

    if key not in rule_map:
        return None

    content = line[pos + 1:].strip()

    comma_pos = content.find(",")
    comment_pos = content.find("//")

    cut = len(content)
    if comma_pos != -1:
        cut = min(cut, comma_pos)
    if comment_pos != -1:
        cut = min(cut, comment_pos)

    content = content[:cut].strip()

    if not content:
        return None

    return f"{rule_map[key]},{content},{tag}"


# ===== 文件处理 =====
def process_file(file_name, rule_map):
    tag = os.path.splitext(file_name)[0]

    src_path = os.path.join(SOURCE_DIR, file_name)
    dst_path = os.path.join(OUTPUT_DIR, file_name)

    count = 0
    results = []

    with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            result = process_line(line, tag, rule_map)
            if result:
                results.append(result)
                count += 1

    with open(dst_path, "w", encoding="utf-8") as out:
        for i, item in enumerate(results):
            if i == len(results) - 1:
                out.write(item)
            else:
                out.write(item + "\n")

    return count


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

    print(">>> 处理 Ruleset 规则...\n")

    rule_map = RULE_MAP

    for name in files:
        try:
            count = process_file(name, rule_map)
            if count:
                print(f"[完成] {name} -> {count} 条")
            else:
                print(f"[跳过] {name}")
        except Exception as e:
            print(f"[错误] {name}: {e}")


if __name__ == "__main__":
    run()
    if len(sys.argv) == 1:
        print("\n--- 完成 ---")
        input("回车退出...")