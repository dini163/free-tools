#!/usr/bin/env python3
"""
为所有 HTML 文件添加 manifest.json 引用和移动端优化标签
"""
from pathlib import Path

BASE_DIR = "/Users/richard/workspace/free-tools"

def add_pwa_tags(html_content, is_index=False, is_tool_page=False):
    """添加 PWA 和移动端优化标签"""
    
    # 1. 添加 manifest.json 引用（如果还没有）
    if 'rel="manifest"' not in html_content:
        manifest_tag = '<link rel="manifest" href="manifest.json">'
        if is_tool_page:
            manifest_tag = '<link rel="manifest" href="../manifest.json">'
        
        # 在 </head> 前插入
        html_content = html_content.replace('</head>', f'    {manifest_tag}\n</head>')
    
    # 2. 添加 theme-color（如果还没有）
    if 'name="theme-color"' not in html_content:
        theme_color = '<meta name="theme-color" content="#667eea">'
        html_content = html_content.replace('</head>', f'    {theme_color}\n</head>')
    
    # 3. 添加 mobile-web-app-capable（如果还没有）
    if 'name="mobile-web-app-capable"' not in html_content:
        mobile_capable = '<meta name="mobile-web-app-capable" content="yes">'
        html_content = html_content.replace('</head>', f'    {mobile_capable}\n</head>')
    
    # 4. 添加 apple-mobile-web-app-capable（如果还没有）
    if 'name="apple-mobile-web-app-capable"' not in html_content:
        apple_capable = '<meta name="apple-mobile-web-app-capable" content="yes">'
        html_content = html_content.replace('</head>', f'    {apple_capable}\n</head>')
    
    # 5. 添加 apple-mobile-web-app-status-bar-style（如果还没有）
    if 'name="apple-mobile-web-app-status-bar-style"' not in html_content:
        apple_status = '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
        html_content = html_content.replace('</head>', f'    {apple_status}\n</head>')
    
    return html_content

def main():
    base_dir = Path(BASE_DIR)
    updated_count = 0
    
    print("🚀 开始添加 PWA 和移动端优化标签...\n")
    
    # 更新 index.html
    index_file = base_dir / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding='utf-8')
        updated = add_pwa_tags(content, is_index=True)
        
        if content != updated:
            index_file.write_text(updated, encoding='utf-8')
            updated_count += 1
            print(f"✅ 已更新 index.html")
    
    # 更新所有工具页面
    tools_dir = base_dir / "tools"
    for html_file in tools_dir.glob("*.html"):
        try:
            content = html_file.read_text(encoding='utf-8')
            updated = add_pwa_tags(content, is_tool_page=True)
            
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
