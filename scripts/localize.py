#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ts-cms-ep-sfx 汉化脚本（无界面版，供 GitHub Actions 使用）

用法: python3 localize.py <输入encrypt.html> <输出文件.html>
"""

import re, base64, hashlib, sys, os
from urllib.parse import unquote

TRANSLATIONS = [
    ('"Advanced options"', '"高级选项"'),
    ('"Advanced password options"', '"高级密码选项"'),
    ('"An error occurred"', '"发生错误"'),
    ('"Approximate file size"', '"大约文件大小"'),
    ('"Archive name"', '"压缩包名称"'),
    ('"Cancel"', '"取消"'),
    ('"Close"', '"关闭"'),
    ('"Confirm password"', '"确认密码"'),
    ('"Decrypt a file"', '"解密文件"'),
    ('"Drop your file here"', '"将文件拖放到此处"'),
    ('"Drop your files here"', '"将文件拖放到此处"'),
    ('"Encrypt a file"', '"加密文件"'),
    ('"File configuration"', '"文件配置"'),
    ('"File name"', '"文件名"'),
    ('"File selected"', '"已选择文件"'),
    ('"File selection"', '"文件选择"'),
    ('"File size"', '"文件大小"'),
    ('"File"', '"文件"'),
    ('"Form actions"', '"表单操作"'),
    ('"Getting things ready"', '"正在准备..."'),
    ('"HTML\\u2010based file encryption and decryption utility"',
     '"基于HTML的文件加密解密工具"'),
    ('"Hint"', '"提示"'),
    ('"Message"', '"消息"'),
    ('"Name"', '"名称"'),
    ('"Next \\u2192"', '"下一步 \\u2192"'),
    ('"No file name"', '"无文件名"'),
    ('"No file name provided"', '"未提供文件名"'),
    ('"Other options"', '"其他选项"'),
    ('"Override file name"', '"覆盖文件名"'),
    ('"Password"', '"密码"'),
    ('"Password configuration"', '"密码配置"'),
    ("\"Passwords don't match\"", '"两次密码不一致"'),
    ('"Processing data\\u2026"', '"正在处理数据\\u2026"'),
    ('"Provided information"', '"提供的信息"'),
    ('"Reset"', '"重置"'),
    ('"Review file information"', '"查看文件信息"'),
    ('"Skip to main content"', '"跳转到主要内容"'),
    ('"Source"', '"源代码"'),
    ('"Stack"', '"堆栈"'),
    ('"Testing mode banner"', '"测试模式横幅"'),
    ('"\\u26a0\\ufe0f Testing mode \\u26a0\\ufe0f"',
     '"\\u26a0\\ufe0f 测试模式 \\u26a0\\ufe0f"'),
    ('"\\u2705\\ufe0f File successfully decrypted!"',
     '"\\u2705\\ufe0f 文件解密成功！"'),
    ('"\\u2b07\\ufe0e Download for offline use"',
     '"\\u2b07\\ufe0e 下载离线使用"'),
    ('"\\ud83d\\udcbe\\ufe0e Download"', '"\\ud83d\\udcbe\\ufe0e 下载"'),
    ('"\\ud83d\\udcbe\\ufe0e Save"', '"\\ud83d\\udcbe\\ufe0e 保存"'),
    ('"attribution"', '"署名"'),
    ('" iteration count"', '" 迭代次数"'),
    ('"More options\\u2026"', '"更多选项\\u2026"'),
    ('"Invalid or missing password"', '"密码无效或缺失"'),
    ('"Missing password"', '"缺少密码"'),
    ('"Missing or invalid file"', '"文件缺失或无效"'),
    ('"Unable to read file contents"', '"无法读取文件内容"'),
    ('"Unsupported browser"', '"浏览器不受支持"'),
    ('"Warranty disclaimer"', '"免责声明"'),
    ('"Made with \\u2764\\ufe0f by "', '"用 \\u2764\\ufe0f 制作，"'),
    ('" Apeleg Limited. All rights reserved."', '" Apeleg 版权所有。"'),
    ('"Build information: "', '"构建信息："'),
]

DISCLAIMER_OLD = (
    '"To the extent permissible by applicable law, the Software is provided '
    '\\u201cas is\\u201d, without warranty of any kind, express or implied, '
    'including but not limited to the warranties of merchantability, fitness '
    'for a particular purpose and noninfringement. Except as required by '
    'applicable law, in no event shall the authors or copyright holders be '
    'liable for any claim, damages or other liability, whether in an action '
    'of contract, tort or otherwise, arising from, out of or in connection '
    'with the Software or the use or other dealings in the Software."'
)
DISCLAIMER_NEW = (
    '"在适用法律允许的最大范围内，本软件按\\u201c现状\\u201d提供，'
    '不提供任何明示或暗示的保证，包括但不限于对适销性、特定用途适用性和不侵权的保证。'
    '在任何情况下，除非适用法律要求，作者或版权人均不对因本软件或使用本软件而产生的'
    '任何索赔、损害或其他责任承担责任，无论是合同、侵权或其他诉讼行为。"'
)

BROWSER_UNSUPPORTED_OLD = (
    '"Your browser is unsupported and some functionality might not work as intended."'
)
BROWSER_UNSUPPORTED_NEW = '"您的浏览器不受支持，部分功能可能无法正常使用。"'

TITLE_OLD = '<title>HTML CMS Tool</title>'
TITLE_NEW = '<title>文件加密解密工具</title>'


def js_escape(s):
    out = []
    for ch in s:
        if ord(ch) > 127:
            out.append('\\u%04x' % ord(ch))
        else:
            out.append(ch)
    return ''.join(out)


def sha384_b64(data):
    return 'sha384-' + base64.b64encode(hashlib.sha384(data).digest()).decode()


def do_localize(html, log=print):
    si = html.find('id="i15">')
    if si < 0:
        raise ValueError('找不到 id="i15"，上游文件结构可能已变化。')
    text = html[si + len('id="i15">'):]
    ei = text.find(']]></script>')
    i15_text = text[:ei]
    pat = re.compile(r'^\s*(?:<!\[CDATA\[)?>\x3c!--([\S\s]*):--\x3e<!(?:]]\x3e)?\s*$')
    m = pat.match(i15_text)
    if not m:
        raise ValueError('无法从 i15 提取 base64 数据，上游文件结构可能已变化。')
    cleaned = re.sub(r'[^a-zA-Z0-9+/=]', '', m.group(1).strip())
    main_js = base64.b64decode(cleaned).decode('utf-8')
    log('解码主 JS: %d 字符' % len(main_js))

    total = 0
    for old, new in list(TRANSLATIONS) + [(DISCLAIMER_OLD, DISCLAIMER_NEW)]:
        new_escaped = '"' + js_escape(new[1:-1]) + '"'
        if old in main_js:
            n = main_js.count(old)
            main_js = main_js.replace(old, new_escaped)
            total += n
        else:
            log('[跳过] 未找到: %s' % old[:60])
    log('主 JS 共替换 %d 处' % total)

    new_b64 = base64.b64encode(main_js.encode('utf-8')).decode('ascii')
    lines = [new_b64[i:i+76] for i in range(0, len(new_b64), 76)]
    new_b64_formatted = '\n'.join(lines)
    new_hash = sha384_b64(main_js.encode('utf-8'))

    new_i15_full = '<![CDATA[><!--\n' + new_b64_formatted + '\n:--><!'
    html = html[:si+len('id="i15">')] + new_i15_full + html[si+len('id="i15">')+len(i15_text):]

    old_di = re.search(r'data-integrity="(sha384-[^"]+)"', html).group(1)
    html = html.replace(f'data-integrity="{old_di}"', f'data-integrity="{new_hash}"', 1)
    html = html.replace(f"'{old_di}'", f"'{new_hash}'", 1)

    parts = html.split('data:text/javascript;base64,', 2)
    if len(parts) >= 2:
        err_raw = parts[1].split('"')[0]
        err_js = base64.b64decode(unquote(err_raw)).decode('utf-8')
        new_err_escaped = '"' + js_escape(BROWSER_UNSUPPORTED_NEW[1:-1]) + '"'
        if BROWSER_UNSUPPORTED_OLD in err_js:
            err_js = err_js.replace(BROWSER_UNSUPPORTED_OLD, new_err_escaped)
            log('浏览器提示已翻译')
        new_err_bytes = err_js.encode('utf-8')
        new_err_b64 = base64.b64encode(new_err_bytes).decode('ascii')
        new_err_url = new_err_b64.replace('=', '%3D')
        new_err_hash = sha384_b64(new_err_bytes)
        html = html.replace('data:text/javascript;base64,' + err_raw,
                            'data:text/javascript;base64,' + new_err_url, 1)
        old_eh = re.search(r'integrity="(sha384-[^"]+)"', html)
        if old_eh:
            html = html.replace(f'integrity="{old_eh.group(1)}"',
                                f'integrity="{new_err_hash}"', 1)
            html = html.replace(f"'{old_eh.group(1)}'",
                                f"'{new_err_hash}'", 1)

    if TITLE_OLD in html:
        html = html.replace(TITLE_OLD, TITLE_NEW, 1)
        log('页面标题已替换')
    return html


def main():
    if len(sys.argv) < 3:
        print('用法: python3 localize.py <输入.html> <输出.html>')
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    result = do_localize(html)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(result)
    print('输出: %s (%d 字节)' % (dst, len(result)))


if __name__ == '__main__':
    main()
