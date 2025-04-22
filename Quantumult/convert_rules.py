import os
import re

def convert_surge_to_qx(surge_rules, filename):
    qx_rules = []

    # 提取文件名（不含扩展名）作为分流策略
    policy_name = os.path.splitext(filename)[0]

    for rule in surge_rules:
        # 保留原始的注释行和空行
        original_rule = rule.strip()
        if not original_rule:
            qx_rules.append(original_rule)
            continue

        # 删除包含//的内容
        rule = re.sub(r'//.*', '', rule).strip()

        # 移除no-resolve
        rule = re.sub(r',\s*no-resolve', '', rule, flags=re.IGNORECASE)

        # 判断是否为注释行，如果是注释行，也进行转换
        if original_rule.startswith("#"):
            rule = original_rule.lstrip("#").strip()
            if rule:
                rule = re.sub(r',\s*no-resolve', '', rule, flags=re.IGNORECASE)
                try:
                    if rule.startswith("DOMAIN-SUFFIX"):
                        parts = rule.split(",")
                        qx_rules.append(f"# host-suffix,{parts[1]},{policy_name}")
                    elif rule.startswith("DOMAIN-WILDCARD"):
                        parts = rule.split(",")
                        qx_rules.append(f"# host-wildcard,{parts[1]},{policy_name}")
                    elif rule.startswith("DOMAIN-KEYWORD"):
                        parts = rule.split(",")
                        qx_rules.append(f"# host-keyword,{parts[1]},{policy_name}")
                    elif rule.startswith("DOMAIN"):
                        parts = rule.split(",")
                        qx_rules.append(f"# host,{parts[1]},{policy_name}")
                    elif rule.startswith("USER-AGENT"):
                        parts = rule.split(",")
                        qx_rules.append(f"# user-agent,{parts[1]},{policy_name}")
                    elif rule.startswith("IP-CIDR6"):
                        parts = rule.split(",")
                        qx_rules.append(f"# ip6-cidr,{parts[1]},{policy_name}")
                    elif rule.startswith("IP-CIDR"):
                        parts = rule.split(",")
                        qx_rules.append(f"# ip-cidr,{parts[1]},{policy_name}")
                    elif rule.startswith("GEOIP"):
                        parts = rule.split(",")
                        qx_rules.append(f"# geoip,{parts[1]},{policy_name}")
                    elif rule.startswith("IP-ASN"):
                        parts = rule.split(",")
                        qx_rules.append(f"# ip-asn,{parts[1]},{policy_name}")
                    else:
                        qx_rules.append(original_rule)
                except IndexError as e:
                    print(f"错误: 无法解析规则 '{rule}' - {e}")  # 输出解析错误
                    qx_rules.append(f"# 无法解析的规则: {rule}")
            else:
                qx_rules.append(original_rule)
            continue

        # 判断规则类型并转换
        try:
            if rule.startswith("DOMAIN-SUFFIX"):
                parts = rule.split(",")
                qx_rules.append(f"host-suffix,{parts[1]},{policy_name}")
            elif rule.startswith("DOMAIN-WILDCARD"):
                parts = rule.split(",")
                qx_rules.append(f"host-wildcard,{parts[1]},{policy_name}")
            elif rule.startswith("DOMAIN-KEYWORD"):
                parts = rule.split(",")
                qx_rules.append(f"host-keyword,{parts[1]},{policy_name}")
            elif rule.startswith("DOMAIN"):
                parts = rule.split(",")
                qx_rules.append(f"host,{parts[1]},{policy_name}")
            elif rule.startswith("USER-AGENT"):
                parts = rule.split(",")
                qx_rules.append(f"user-agent,{parts[1]},{policy_name}")
            elif rule.startswith("IP-CIDR6"):
                parts = rule.split(",")
                qx_rules.append(f"ip6-cidr,{parts[1]},{policy_name}")
            elif rule.startswith("IP-CIDR"):
                parts = rule.split(",")
                qx_rules.append(f"ip-cidr,{parts[1]},{policy_name}")
            elif rule.startswith("GEOIP"):
                parts = rule.split(",")
                qx_rules.append(f"geoip,{parts[1]},{policy_name}")
            elif rule.startswith("IP-ASN"):
                parts = rule.split(",")
                qx_rules.append(f"ip-asn,{parts[1]},{policy_name}")
            else:
                print(f"未识别的规则: {rule}")  # 输出未识别的规则
                qx_rules.append(f"# 未识别的规则: {rule}")
        except IndexError as e:
            print(f"错误: 无法解析规则 '{rule}' - {e}")  # 输出解析错误
            qx_rules.append(f"# 无法解析的规则: {rule}")

    return qx_rules

def convert_files_in_directory(surge_dir, qx_dir):
    for root, _, files in os.walk(surge_dir):
        for filename in files:
            if filename.endswith(".list"):
                surge_file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(surge_file_path, surge_dir)
                qx_file_path = os.path.join(qx_dir, relative_path)

                os.makedirs(os.path.dirname(qx_file_path), exist_ok=True)

                with open(surge_file_path, 'r', encoding='utf-8') as f:
                    surge_rules = f.readlines()

                qx_rules = convert_surge_to_qx(surge_rules, filename)

                with open(qx_file_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(qx_rules))

                print(f"转换完成，规则已保存到 {qx_file_path}")

def main():
    surge_dir = "Ruleset"
    qx_dir = "Filter"

    # 确保目标目录存在
    if not os.path.exists(qx_dir):
        os.makedirs(qx_dir)

    convert_files_in_directory(surge_dir, qx_dir)

if __name__ == "__main__":
    main()
