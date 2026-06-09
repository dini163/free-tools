#!/usr/bin/env python3
"""
为所有工具页面添加 Open Graph 和 Twitter Card 标签以优化 SEO
"""
import re
import os
from pathlib import Path

TOOLS_DIR = "/Users/richard/workspace/free-tools/tools"
BASE_URL = "https://dini163.github.io/free-tools"

def extract_meta_info(html_content):
    """从 HTML 内容中提取 title 和 description"""
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    desc_match = re.search(r'<meta name="description" content="(.*?)"', html_content, re.IGNORECASE)
    
    title = title_match.group(1) if title_match else ""
    description = desc_match.group(1) if desc_match else ""
    
    return title, description

def has_og_tags(html_content):
    """检查是否已有 Open Graph 标签"""
    return 'og:' in html_content or 'property="og:' in html_content

def has_twitter_tags(html_content):
    """检查是否已有 Twitter Card 标签"""
    return 'twitter:' in html_content or 'name="twitter:' in html_content

def add_social_meta_tags(html_content, title, description, canonical_url):
    """添加 Open Graph 和 Twitter Card 标签"""
    
    # 构建 Open Graph 标签
    og_tags = f"""
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="{BASE_URL}/assets/og-image.png">
    <meta property="og:site_name" content="FreeDevTools">"""
    
    # 构建 Twitter Card 标签
    twitter_tags = f"""
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{BASE_URL}/assets/og-image.png">"""
    
    # 在 </head> 前插入标签
    if not has_og_tags(html_content):
        html_content = html_content.replace('</head>', og_tags + '\n</head>')
    
    if not has_twitter_tags(html_content):
        html_content = html_content.replace('</head>', twitter_tags + '\n</head>')
    
    return html_content

def main():
    tools_dir = Path(TOOLS_DIR)
    updated_count = 0
    skipped_count = 0
    
    print("🚀 开始为工具页面添加社交媒体标签...\n")
    
    for html_file in tools_dir.glob("*.html"):
        try:
            content = html_file.read_text(encoding='utf-8')
            
            # 提取已有信息
            title, description = extract_meta_info(content)
            
            if not title or not description:
                print(f"⚠️  跳过 {html_file.name} (缺少 title 或 description)")
                skipped_count += 1
                continue
            
            # 获取 canonical URL
            canonical_match = re.search(r'<link rel="canonical" href="(.*?)"', content)
            if canonical_match:
                canonical_url = canonical_match.group(1)
            else:
                # 如果没有 canonical，使用默认 URL
                relative_path = html_file.relative_to(tools_dir.parent)
                canonical_url = f"{BASE_URL}/{relative_path}"
            
            # 检查是否已有标签
            has_og = has_og_tags(content)
            has_twitter = has_twitter_tags(content)
            
            if has_og and has_twitter:
                print(f"✅ 跳过 {html_file.name} (已有标签)")
                skipped_count += 1
                continue
            
            # 添加标签
            updated_content = add_social_meta_tags(content, title, description, canonical_url)
            
            # 写回文件
            html_file.write_text(updated_content, encoding='utf-8')
            updated_count += 1
            print(f"✅ 已更新 {html_file.name}")
            
        except Exception as e:
            print(f"❌ 错误 {html_file.name}: {e}")
    
    print(f"\n📊 完成统计:")
    print(f"   - 已更新: {updated_count} 个文件")
    print(f"   - 已跳过: {skipped_count} 个文件")
    print(f"   - 总计: {updated_count + skipped_count} 个文件")

if __name__ == "__main__":
    main()
