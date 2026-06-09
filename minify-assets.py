#!/usr/bin/env python3
"""
压缩 CSS 和 JS 文件以优化性能
"""
import re
import os
from pathlib import Path

def minify_css(css_content):
    """压缩 CSS：移除注释、空格、换行"""
    # 移除多行注释
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # 移除多余空格
    css_content = re.sub(r'\s+', ' ', css_content)
    # 移除特定位置的空格
    css_content = re.sub(r'\s*{\s*', '{', css_content)
    css_content = re.sub(r'\s*}\s*', '}', css_content)
    css_content = re.sub(r'\s*;\s*', ';', css_content)
    css_content = re.sub(r'\s*:\s*', ':', css_content)
    css_content = re.sub(r'\s*,\s*', ',', css_content)
    # 移除首尾空格
    css_content = css_content.strip()
    return css_content

def minify_js(js_content):
    """简单的 JS 压缩：移除注释、多余空格"""
    # 移除单行注释
    js_content = re.sub(r'//.*$', '', js_content, flags=re.MULTILINE)
    # 移除多行注释
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    # 移除多余空格和换行
    js_content = re.sub(r'\s+', ' ', js_content)
    # 移除特定位置的空格
    js_content = re.sub(r'\s*{\s*', '{', js_content)
    js_content = re.sub(r'\s*}\s*', '}', js_content)
    js_content = re.sub(r'\s*;\s*', ';', js_content)
    js_content = re.sub(r'\s*:\s*', ':', js_content)
    js_content = re.sub(r'\s*=\s*', '=', js_content)
    js_content = re.sub(r'\s*==\s*', '==', js_content)
    js_content = re.sub(r'\s*!=\s*', '!=', js_content)
    js_content = re.sub(r'\s*&&\s*', '&&', js_content)
    js_content = re.sub(r'\s*\|\|\s*', '||', js_content)
    # 移除首尾空格
    js_content = js_content.strip()
    return js_content

def main():
    base_dir = Path(__file__).resolve().parent
    
    print("🚀 开始压缩 CSS 和 JS 文件...\n")
    
    # 压缩 CSS
    css_file = base_dir / "css/style.css"
    if css_file.exists():
        original_size = css_file.stat().st_size
        content = css_file.read_text(encoding='utf-8')
        minified = minify_css(content)
        
        min_file = base_dir / "css/style.min.css"
        min_file.write_text(minified, encoding='utf-8')
        
        minified_size = min_file.stat().st_size
        savings = original_size - minified_size
        percent = (savings / original_size) * 100
        
        print(f"✅ CSS 压缩完成:")
        print(f"   - 原始: {original_size:,} bytes")
        print(f"   - 压缩后: {minified_size:,} bytes")
        print(f"   - 节省: {savings:,} bytes ({percent:.1f}%)\n")
    
    # 压缩 JS - theme.js
    js_files = [
        ("js/theme.js", "js/theme.min.js"),
        ("js/i18n.js", "js/i18n.min.js")
    ]
    
    for src, dst in js_files:
        src_file = base_dir / src
        if src_file.exists():
            original_size = src_file.stat().st_size
            content = src_file.read_text(encoding='utf-8')
            minified = minify_js(content)
            
            min_file = base_dir / dst
            min_file.write_text(minified, encoding='utf-8')
            
            minified_size = min_file.stat().st_size
            savings = original_size - minified_size
            percent = (savings / original_size) * 100
            
            print(f"✅ JS 压缩完成 ({src}):")
            print(f"   - 原始: {original_size:,} bytes")
            print(f"   - 压缩后: {minified_size:,} bytes")
            print(f"   - 节省: {savings:,} bytes ({percent:.1f}%)\n")
    
    print("📊 总节省:")
    total_original = 24020 + 5514 + 81750  # 从之前的输出
    total_minified = 0
    
    for f in ["css/style.min.css", "js/theme.min.js", "js/i18n.min.js"]:
        f_path = base_dir / f
        if f_path.exists():
            total_minified += f_path.stat().st_size
    
    total_savings = total_original - total_minified
    print(f"   - 原始总大小: {total_original:,} bytes ({total_original/1024:.1f} KB)")
    print(f"   - 压缩后总大小: {total_minified:,} bytes ({total_minified/1024:.1f} KB)")
    print(f"   - 总节省: {total_savings:,} bytes ({total_savings/1024:.1f} KB, {total_savings/total_original*100:.1f}%)")

if __name__ == "__main__":
    main()
