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
    "IP-CIDR6": "ip6-cidr",
    "IP-CIDR": "ip-cidr",
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

    raw_type = line[:pos].strip().upper()
    if raw_type not in rule_map:
        return None

    content = line[pos + 1:].strip()
    
    comma_pos = content.find(",")
    comment_pos = content.find("//")
    
    cut = -1
    if comma_pos != -1 and comment_pos != -1:
        cut = min(comma_pos, comment_pos)
    elif comma_pos != -1:
        cut = comma_pos
    elif comment_pos != -1:
        cut = comment_pos

    if cut != -1:
        content = content[:cut].strip()

    if not content:
        return None

    return f"{rule_map[raw_type]},{content},{tag}"


# ===== 文件处理 =====
def process_file(file_name, rule_map):
    tag = os.path.splitext(file_name)[0]
    src_path = os.path.join(SOURCE_DIR, file_name)
    dst_path = os.path.join(OUTPUT_DIR, file_name)

    count = 0
    has_content = False

    try:
        with open(src_path, "r", encoding="utf-8", errors="ignore") as f, \
             open(dst_path, "w", encoding="utf-8") as out:
            
            first_entry = True
            for raw_line in f:
                result = process_line(raw_line, tag, rule_map)
                
                if result:
                    if not first_entry:
                        out.write("\n")
                    out.write(result)
                    
                    count += 1
                    first_entry = False
                    has_content = True
        
        if not has_content and os.path.exists(dst_path):
            os.remove(dst_path)
            
        return count
    except Exception:
        raise


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

    print(">>> 正在转换 Ruleset 规则 ...\n")

    for name in files:
        try:
            count = process_file(name, RULE_MAP)
            if count:
                print(f"[完成] {name} -> 提取 {count} 条")
            else:
                print(f"[跳过] {name} (无匹配规则)")
        except Exception as e:
            print(f"[错误] {name}: {e}")


if __name__ == "__main__":
    run()
    if len(sys.argv) == 1:
        print("\n--- 任务全部完成 ---")
        input("按回车键退出...")