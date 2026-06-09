#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

const toolsDir = './tools';
const issues = [];

// 检查每个工具文件
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

console.log(`\n🔍 Checking ${files.length} tool files...\n`);

files.forEach(file => {
    const filePath = path.join(toolsDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    const fileIssues = [];

    // 1. 检查必需的结构
    if (!content.includes('<header class="header">')) {
        fileIssues.push('Missing header');
    }
    if (!content.includes('<main')) {
        fileIssues.push('Missing main content');
    }
    if (!content.includes('<footer class="footer">')) {
        fileIssues.push('Missing footer');
    }

    // 2. 检查多主题支持
    if (!content.includes('theme.js') && !content.includes('theme.min.js')) {
        fileIssues.push('Missing theme.js');
    }
    if (!content.includes('themeToggleBtn')) {
        fileIssues.push('Missing theme toggle button');
    }
    if (!content.includes('setTheme')) {
        fileIssues.push('Missing setTheme function calls');
    }

    // 3. 检查多语言支持
    if (!content.includes('i18n.js') && !content.includes('i18n.min.js')) {
        fileIssues.push('Missing i18n.js');
    }
    if (!content.includes('langToggleBtn')) {
        fileIssues.push('Missing language toggle button');
    }
    if (!content.includes('changeLanguage')) {
        fileIssues.push('Missing changeLanguage function calls');
    }

    // 4. 检查 Google Ads
    if (!content.includes('adsbygoogle')) {
        fileIssues.push('Missing Google Ads script');
    }

    // 5. 检查 canonical URL
    const canonicalMatch = content.match(/<link rel="canonical" href="([^"]+)"/);
    if (canonicalMatch) {
        const expectedCanonical = `https://dini163.github.io/free-tools/tools/${file}`;
        if (canonicalMatch[1] !== expectedCanonical) {
            fileIssues.push(`Canonical URL mismatch: ${canonicalMatch[1]}`);
        }
    } else {
        fileIssues.push('Missing canonical URL');
    }

    // 6. 检查 JS 语法（基本检查）
    const scriptMatch = content.match(/<script>([\s\S]*?)<\/script>/g);
    if (scriptMatch) {
        scriptMatch.forEach(script => {
            // 检查常见语法错误
            if (script.includes('navigator.javaEnabled') && !script.includes('navigator.javaEnabled()')) {
                fileIssues.push('Possible javaEnabled() syntax error');
            }
        });
    }

    if (fileIssues.length > 0) {
        issues.push({ file, issues: fileIssues });
    }
});

// 输出结果
if (issues.length === 0) {
    console.log('✅ All tool files passed basic checks!\n');
} else {
    console.log('❌ Found issues in the following files:\n');
    issues.forEach(({ file, issues }) => {
        console.log(`📄 ${file}:`);
        issues.forEach(issue => console.log(`   - ${issue}`));
        console.log('');
    });
}

// 检查 index.html 中的链接
console.log('\n🔗 Checking index.html links...\n');

const indexContent = fs.readFileSync('./index.html', 'utf-8');
const linkPattern = /href="tools\/([^"]+)"/g;
const links = [];
let match;

while ((match = linkPattern.exec(indexContent)) !== null) {
    links.push(match[1]);
}

console.log(`Found ${links.length} tool links in index.html`);

const missingFiles = [];
links.forEach(link => {
    const filePath = path.join(toolsDir, link);
    if (!fs.existsSync(filePath)) {
        missingFiles.push(link);
    }
});

if (missingFiles.length > 0) {
    console.log('\n❌ Missing files:');
    missingFiles.forEach(file => console.log(`   - ${file}`));
} else {
    console.log('✅ All linked files exist!\n');
}

// 检查未被链接的文件
const linkedFiles = new Set(links);
const unlinkedFiles = files.filter(file => !linkedFiles.has(file));

if (unlinkedFiles.length > 0) {
    console.log('\n⚠️  Files not linked in index.html:');
    unlinkedFiles.forEach(file => console.log(`   - ${file}`));
} else {
    console.log('✅ All files are linked in index.html!\n');
}

console.log('\n📊 Summary:');
console.log(`   - Total tool files: ${files.length}`);
console.log(`   - Total links in index.html: ${links.length}`);
console.log(`   - Files with issues: ${issues.length}`);
console.log(`   - Missing files: ${missingFiles.length}`);
console.log(`   - Unlinked files: ${unlinkedFiles.length}`);
