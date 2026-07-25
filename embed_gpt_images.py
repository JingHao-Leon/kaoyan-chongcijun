import re, os

WEBSITE_DIR = "/Users/ahs/Documents/kimi/workspace/考研冲刺君/website"

# 定义每个文件的章节→新配图映射
CHAPTER_IMAGES = {
    "ds.html": [
        ("绪论", ["ds_ch1_intro.png"]),
        ("线性表", ["ds_ch2_linked_list.png"]),
        ("栈、队列和数组", ["ds_ch3_stack_queue.png"]),
        ("树与二叉树", ["ds_ch4_tree.png"]),
        ("图", ["ds_ch5_graph.png"]),
        ("查找", ["ds_ch6_search.png"]),
        ("排序", ["ds_ch7_sort.png"]),
    ],
    "co.html": [
        ("计算机系统概述", ["co_ch1_overview.png"]),
        ("数据的表示和运算", ["co_ch2_data_representation.png"]),
        ("存储系统", ["co_ch3_memory.png"]),
        ("指令系统", ["co_ch4_instruction.png"]),
        ("中央处理器", ["co_ch5_cpu.png"]),
        ("总线", ["co_ch6_bus.png"]),
    ],
    "os.html": [
        ("操作系统概述", ["os_ch1_overview.png"]),
        ("进程管理", ["os_ch2_process.png"]),
        ("内存管理", ["os_ch3_memory.png"]),
        ("文件管理", ["os_ch4_file.png"]),
        ("输入输出系统", ["os_ch5_io.png"]),
    ],
    "cn.html": [
        ("计算机网络体系结构", ["cn_ch1_architecture.png"]),
        ("物理层", ["cn_ch2_physical.png"]),
        ("数据链路层", ["cn_ch3_datalink.png"]),
        ("网络层", ["cn_ch4_network.png"]),
        ("传输层", ["cn_ch5_transport.png"]),
        ("应用层", ["cn_ch6_application.png"]),
    ],
}

def img_tag(filename, alt):
    return f'<div style="text-align:center;margin:20px 0;"><img src="images/{filename}" style="max-width:100%;border-radius:8px;border:1px solid #e3e2e0;" alt="{alt}"></div>'

def embed_images(html_path, mappings):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    inserted = 0
    for keyword, img_list in mappings:
        # 找到包含关键词的<h2>标签
        pattern = rf'(<h2[^>]*>[^<]*{re.escape(keyword)}[^<]*</h2>)'
        match = re.search(pattern, content)
        if match:
            h2_tag = match.group(1)
            # 检查这些图片是否已经被插入
            imgs_html = ""
            for img in img_list:
                if img not in content:
                    imgs_html += img_tag(img, img.replace(".png", ""))
            if imgs_html:
                # 在h2标签后插入图片
                content = content.replace(h2_tag, h2_tag + "\n" + imgs_html, 1)
                inserted += len(img_list)
                print(f"  ✓ {os.path.basename(html_path)}: 在'{keyword}'后插入 {len(img_list)} 张新图")
            else:
                print(f"  - {os.path.basename(html_path)}: '{keyword}' 的新图已存在")
        else:
            print(f"  ✗ {os.path.basename(html_path)}: 未找到章节'{keyword}'")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    return inserted

# 处理所有文件
total_inserted = 0
for filename, mappings in CHAPTER_IMAGES.items():
    html_path = os.path.join(WEBSITE_DIR, filename)
    print(f"\n处理: {filename}")
    count = embed_images(html_path, mappings)
    total_inserted += count

print(f"\n{'='*50}")
print(f"总共新插入了 {total_inserted} 张 GPT Image 2 配图")
