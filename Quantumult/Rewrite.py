import os
import sys

# ===== 基础配置 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "Module")
OUTPUT_DIR = os.path.join(BASE_DIR, "Rewrite")

VALID_EXT = (".list", ".conf", ".sgmodule", ".txt", ".ruleset")

def process_line(line):

    line = line.strip()

    if not line or line[0] in "#;[/":
        return None, False

    is_reject = False
    
    if "- reject" in line:
        line = line.replace("- reject", "url reject")
        is_reject = True
    
    if "%APPEND% " in line:
        line = line.replace("%APPEND% ", "")

    return line, is_reject

def get_hostname_count(line):

    line_lower = line.lower()
    if "hostname" not in line_lower:
        return 0
    eq_pos = line.find("=")
    if eq_pos == -1:
        return 0

    content = line[eq_pos + 1:].strip()
    if not content:
        return 0
    return sum(1 for h in content.split(",") if h.strip())

def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(SOURCE_DIR):
        print(f"错误：找不到目录 {SOURCE_DIR}")
        return

    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(VALID_EXT)]
    if not files:
        print("未找到规则文件")
        return

    print(f">>> 开始处理 {len(files)} 个文件...\n")

    for name in files:
        src_path = os.path.join(SOURCE_DIR, name)
        dst_name = os.path.splitext(name)[0] + ".snippet"
        dst_path = os.path.join(OUTPUT_DIR, dst_name)

        total_reject = 0
        total_host = 0
        has_content = False

        try:
            with open(src_path, "r", encoding="utf-8", errors="ignore") as f, \
                 open(dst_path, "w", encoding="utf-8") as out:
                
                first_line = True
                for raw_line in f:
                    processed, is_reject = process_line(raw_line)
                    
                    if processed:

                        if is_reject:
                            total_reject += 1
                        if "hostname" in processed.lower():
                            total_host += get_hostname_count(processed)
                        
                        if not first_line:
                            out.write("\n")
                        out.write(processed)
                        
                        first_line = False
                        has_content = True

            if has_content:
                print(f"[完成] {name} -> {dst_name}")
                print(f"      └─ reject: {total_reject} | hostname: {total_host}")
            else:
                print(f"[跳过] {name} (无有效内容)")
                if os.path.exists(dst_path):
                    os.remove(dst_path)

        except Exception as e:
            print(f"[错误] {name}: {e}")

if __name__ == "__main__":
    run()
    if len(sys.argv) == 1:
        print("\n--- 全部处理完成 ---")
        input("按回车退出...")