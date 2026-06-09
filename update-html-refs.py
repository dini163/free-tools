#!/usr/bin/env python3
"""
更新所有 HTML 文件以引用压缩后的 CSS/JS 资源
"""
import re
from pathlib import Path

BASE_DIR = "/Users/richard/workspace/free-tools"

def update_html_references(html_content):
    """更新 HTML 中的 CSS/JS 引用"""
    
    # 替换 CSS 引用
    html_content = html_content.replace(
        'href="css/style.css"',
        'href="css/style.min.css"'
    )
    
    # 替换 JS 引用 (theme.js)
    html_content = html_content.replace(
        'src="js/theme.js"',
        'src="js/theme.min.js" defer'
    )
    
    # 替换 JS 引用 (i18n.js) - 添加 defer
    html_content = html_content.replace(
        'src="js/i18n.js"',
        'src="js/i18n.min.js" defer'
    )
    
    # 替换 tools/ 目录中的 JS 引用
    html_content = html_content.replace(
        'src="../js/theme.js"',
        'src="../js/theme.min.js" defer'
    )
    html_content = html_content.replace(
        'src="../js/i18n.js"',
        'src="../js/i18n.min.js" defer'
    )
    
    # 替换 CDN 引用 - 添加 defer (如果还没有)
    html_content = html_content.replace(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>',
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js" defer></script>'
    )
    html_content = html_content.replace(
        '<script src="../js/js-yaml.min.js"></script>',
        '<script src="../js/js-yaml.min.js" defer></script>'
    )
    
    return html_content

def add_preload_tags(html_content, is_index=False):
    """添加资源预加载标签"""
    
    preload_tags = """
    <!-- Preload critical resources -->
    <link rel="preload" href="css/style.min.css" as="style">
    <link rel="preload" href="js/theme.min.js" as="script">
    <link rel="preload" href="js/i18n.min.js" as="script">"""
    
    if is_index:
        preload_tags += """
    <link rel="preload" href="css/style.min.css" as="style">"""
    
    # 在 </head> 前插入预加载标签
    if '</head>' in html_content and 'rel="preload"' not in html_content:
        html_content = html_content.replace('</head>', preload_tags + '\n</head>')
    
    return html_content

def main():
    base_dir = Path(BASE_DIR)
    updated_count = 0
    
    print("🚀 开始更新 HTML 文件引用...\n")
    
    # 更新 index.html
    index_file = base_dir / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding='utf-8')
        updated = update_html_references(content)
        updated = add_preload_tags(updated, is_index=True)
        
        if content != updated:
            index_file.write_text(updated, encoding='utf-8')
            updated_count += 1
            print(f"✅ 已更新 index.html")
    
    # 更新所有工具页面
    tools_dir = base_dir / "tools"
    for html_file in tools_dir.glob("*.html"):
        try:
            content = html_file.read_text(encoding='utf-8')
            updated = update_html_references(content)
            updated = add_preload_tags(updated, is_index=False)
            
            if content != updated:
                html_file.write_text(updated, encoding='utf-8')
                updated_count += 1
                print(f"✅ 已更新 {html_file.name}")
        
        except Exception as e:
            print(f"❌ 错误 {html_file.name}: {e}")
    
    print(f"\n📊 完成统计:")
    print(f"   - 已更新: {updated_count} 个文件")
    print(f"   - 总计: {updated_count} 个文件")

if __name__ == "__main__":
    main()
