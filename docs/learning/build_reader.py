"""Build the offline learning reader and a source-symbol inventory.

Uses markdown-it-py already present in StayCode's virtual environment.
Only writes inside docs/learning and reads product source/test files.
"""
from __future__ import annotations

import ast
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
MAIN = HERE / "Agent开发学习手册.md"

MODULES = {
    "staycode": "装配、运行时、消息、协议和界面",
    "staycode/agents": "子 Agent 的定义、工具过滤、任务与轨迹",
    "staycode/commands": "用户斜杠命令与参数解析",
    "staycode/commands/handlers": "命令与应用状态的连接",
    "staycode/context": "工具结果预算、压缩和恢复附件",
    "staycode/filehistory": "文件编辑备份与回退快照",
    "staycode/hooks": "生命周期事件、条件和执行器",
    "staycode/mcp": "MCP 连接、包装与加载策略",
    "staycode/memory": "指令、会话日志、自动记忆、召回和整理",
    "staycode/permissions": "权限模式、规则、危险命令与路径检查",
    "staycode/sandbox": "操作系统命令隔离后端",
    "staycode/skills": "技能定义、发现、执行与安装",
    "staycode/teams": "团队成员、共享任务、消息和启动后端",
    "staycode/tools": "模型可调用工具与注册表",
    "staycode/tools/impl": "工具发现实现",
    "staycode/worktree": "Git 工作目录创建、状态和清理",
    "tests": "现有测试：阅读对象，不代表全部已经执行",
}


def inventory():
    lines = [
        "# StayCode 源码导航", "",
        "生成日期：2026-09-24。以当前 Python AST 提取符号和行号，覆盖 staycode/ 与 tests/。",
        "只列定义，不代表相应功能已验证；空初始化文件也保留，便于确认包边界。",
        "源码链接为本机绝对路径。浏览器对源码文件可能显示原文或下载，精确行号请在编辑器中定位。", "",
        "[返回学习手册](E:/AIAgentK开发/StayCode/docs/learning/Agent开发学习手册.md)", "",
    ]
    manifest = []
    source_files = sorted((PROJECT / "staycode").rglob("*.py"))
    test_files = sorted((PROJECT / "tests").glob("*.py"))
    files = source_files + test_files
    lines.extend([f"产品 Python 文件：{len(source_files)}；测试相关 Python 文件：{len(test_files)}。", ""])
    groups = {}
    for path in files:
        groups.setdefault(path.parent.relative_to(PROJECT).as_posix(), []).append(path)
    for group, members in sorted(groups.items()):
        lines.extend([f"## {group}", "", MODULES.get(group, "包资源与初始化"), ""])
        for path in members:
            text = path.read_text(encoding="utf-8-sig")
            tree = ast.parse(text)
            symbols = []
            for node in tree.body:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols.append((node.name, node.lineno))
                    if isinstance(node, ast.ClassDef):
                        for child in node.body:
                            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                symbols.append((f"{node.name}.{child.name}", child.lineno))
            rel = path.relative_to(PROJECT).as_posix()
            lines.extend([f"### {path.name}", "", f"[打开源码]({path.as_posix()}) · {len(text.splitlines())} 行", ""])
            if symbols:
                lines.append(" · ".join(f"[{name}]({path.as_posix()}:{line})" for name, line in symbols))
            else:
                lines.append("无顶层类/函数定义；查看常量、导入或资源声明。")
            lines.append("")
            manifest.append({"path": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                             "lines": len(text.splitlines()), "symbols": symbols})
    lines.extend(["## 非 Python 阅读入口", ""])
    assets = [PROJECT / "pyproject.toml", PROJECT / "staycode/styles.tcss"]
    assets += sorted((PROJECT / "staycode/agents/builtins").glob("*.md"))
    for path in assets:
        lines.append(f"- [{path.relative_to(PROJECT).as_posix()}]({path.as_posix()})")
    (HERE / "源码导航.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (HERE / "evidence").mkdir(exist_ok=True)
    (HERE / "evidence/source-index.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def architecture_svg():
    nodes = [
        ("用户任务", 335, 10, 230, 48),
        ("__main__.py · 入口装配", 285, 92, 330, 52),
        ("TUI · app.py", 35, 188, 240, 54),
        ("CLI · _run_prompt", 330, 188, 240, 54),
        ("Remote · remote.py", 625, 188, 240, 54),
        ("Agent · 执行循环", 295, 290, 310, 62),
        ("消息历史 / 上下文 / 记忆", 20, 404, 250, 68),
        ("LLMClient + 序列化", 325, 404, 250, 68),
        ("注册表 / 权限 / 工具调度", 630, 404, 250, 68),
        ("模型服务", 325, 525, 250, 62),
        ("文件 / Bash / MCP / Agents", 590, 525, 305, 62),
    ]
    paths = ["M450 58V92", "M450 144V165H155V188", "M450 144V188", "M450 165H745V188",
             "M155 242V265H355V290", "M450 242V290", "M745 242V265H545V290",
             "M365 352V380H145V404", "M450 352V404", "M535 352V380H755V404",
             "M450 472V525", "M755 472V525"]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 915 622" role="img" aria-labelledby="arch-title arch-desc">',
             '<title id="arch-title">StayCode 架构职责图</title>',
             '<desc id="arch-desc">用户通过 TUI、CLI 或 Remote 进入 Agent 循环；循环连接消息上下文、模型客户端与工具调度。入口具体接线存在差异。</desc>',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#78928e"/></marker></defs>']
    for d in paths:
        parts.append(f'<path d="{d}" fill="none" stroke="#78928e" stroke-width="2" marker-end="url(#arrow)"/>')
    for label, x, y, w, h in nodes:
        primary = label.startswith("Agent ·")
        fill, color = ("#175b50", "#ffffff") if primary else ("#f0f4ee", "#1e3834")
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#b9ccc1"/>')
        parts.append(f'<text x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle" fill="{color}" font-size="17" font-family="Segoe UI,Microsoft YaHei,sans-serif">{html.escape(label)}</text>')
    parts.append('<text x="457" y="614" text-anchor="middle" font-size="13" fill="#66746d" font-family="Microsoft YaHei,sans-serif">实线展示主要职责连接；工具结果回到历史，驱动下一轮模型请求。</text></svg>')
    return "".join(parts)


CSS = r"""
:root{color-scheme:light;--ink:#24342f;--muted:#64726b;--accent:#175b50;--paper:#faf9f5;--line:#dce2d9}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:32px}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.85 'Segoe UI','Microsoft YaHei',sans-serif}
a{color:var(--accent);text-underline-offset:4px}a:hover{color:#b05e27}button,input{font:inherit}button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #d78b37;outline-offset:3px}
.rail{position:fixed;inset:0 auto 0 0;width:288px;background:#183f37;color:#e2eee4;padding:30px 23px;overflow:auto}.eyebrow{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase}.brand{font-size:27px;font-weight:750;margin:8px 0 3px;letter-spacing:-1px}.rail small{color:#b4cfc1}.rail a{color:#dceae0;text-decoration:none}.rail a:hover,.rail a.active{color:#fff;background:#2d584a}.nav-list{list-style:none;margin:20px 0;padding:0}.nav-list a{display:block;padding:7px 8px;border-radius:5px;line-height:1.5;font-size:13px}.nav-list .done::after{content:' ✓';color:#9ee0ac}.search{width:100%;margin-top:22px;padding:9px 11px;border:1px solid #537467;background:#234d41;color:white;border-radius:6px}.search::placeholder{color:#bed0c5}.progress-track{height:5px;background:#426355;border-radius:8px;margin:13px 0 5px}.progress-fill{height:100%;width:0;background:#a5dba7;border-radius:8px}.progress-text{font-size:12px;color:#c4d9cc}.rail-bottom{border-top:1px solid #426355;padding-top:18px;display:flex;gap:12px;flex-wrap:wrap;font-size:12px}.rail button{border:0;background:none;color:#c4d9cc;padding:0;font-size:12px}
main{margin-left:288px;padding:56px 6vw 100px;max-width:1460px}.topline{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:36px;gap:20px}.topline span{font-size:12px;letter-spacing:1px;color:var(--muted)}.print{background:transparent;border:1px solid var(--line);border-radius:5px;padding:5px 12px;font-size:12px;color:var(--ink)}article{max-width:1020px}h1{font-size:clamp(31px,3.2vw,47px);letter-spacing:-1px;line-height:1.35;max-width:900px;margin:0 0 24px;font-weight:760}h2{font-size:28px;line-height:1.5;margin:0 0 26px;letter-spacing:-.4px}h3{font-size:21px;margin-top:33px;line-height:1.5}p{margin:16px 0}strong{font-weight:700}section{padding-top:54px;margin-top:52px;border-top:1px solid var(--line)}section .chapter-head{display:flex;align-items:flex-start;gap:20px;justify-content:space-between}.complete{white-space:nowrap;font-size:12px;display:flex;gap:6px;align-items:center;color:var(--muted);padding-top:8px}.complete input{accent-color:var(--accent);width:17px;height:17px}li{margin:7px 0}.table-wrap{overflow-x:auto;margin:25px 0}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.7;background:#fff}th{text-align:left;background:#eaf0e7;font-size:13px;color:#234739}th,td{padding:13px 15px;border:1px solid var(--line);vertical-align:top}tbody tr:nth-child(even){background:#f8faf6}code{font:13px/1.7 Consolas,'Cascadia Code',monospace;overflow-wrap:anywhere;background:#eaf0e7;padding:2px 5px;border-radius:3px}pre{background:#203c34;color:#e3eee5;padding:23px 24px;overflow:auto;border-radius:8px;margin:25px 0;position:relative;line-height:1.7}pre code{background:none;padding:0;color:inherit;overflow-wrap:normal;font-size:13px}.copy{position:absolute;right:9px;top:7px;font-size:11px;background:#365448;color:#e3eee5;border:1px solid #61786b;border-radius:4px;padding:2px 8px}.diagram{background:#fff;border:1px solid var(--line);padding:20px;border-radius:9px;margin:25px 0}.diagram svg{display:block;width:100%;height:auto;min-width:450px}.diagram{overflow:auto}.note{padding:14px 18px;background:#eff2e7;border-left:3px solid #8ca565;font-size:14px}footer{margin-top:60px;font-size:12px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px}.mobile-toggle{display:none}.empty-search{display:none;font-size:12px;color:#d6e3d8}.source-note{font-size:12px;color:var(--muted)}
@media(min-width:1500px){main{padding-left:95px;padding-right:80px}}@media(max-width:960px){.rail{width:240px;padding:25px 16px}main{margin-left:240px;padding:38px 28px}.chapter-head{flex-wrap:wrap;gap:0!important}}@media(max-width:700px){.rail{position:relative;width:auto;max-height:none;padding:18px 23px}.brand{font-size:23px}.rail small,.rail .progress-track,.rail .progress-text{display:none}.mobile-toggle{display:inline-block;position:absolute;right:22px;top:27px;padding:5px 10px!important;border:1px solid #789589!important;border-radius:4px}.nav-content{display:none}.rail.open .nav-content{display:block}.rail-bottom{margin-top:15px}main{margin:0;padding:30px 20px 70px}h1{font-size:30px}h2{font-size:24px}body{font-size:15px}th,td{padding:10px;min-width:125px}pre{padding:30px 15px 18px}section{margin-top:35px;padding-top:35px}.topline{margin-bottom:27px}.diagram{padding:8px}}
@media print{.rail,.topline,.complete,.copy,footer{display:none!important}main{margin:0;padding:0;max-width:none}body{font-size:10pt;background:white;color:black}h1{font-size:24pt}h2{font-size:19pt}section{break-before:page;border:0;margin:0;padding:10px 0}h2,h3{break-after:avoid}pre,table,.diagram{break-inside:avoid}pre{white-space:pre-wrap;background:#f4f4f4;color:black;border:1px solid #ccc}a{color:black;text-decoration:none}.table-wrap{overflow:visible}table{font-size:9pt}.diagram svg{min-width:0}}
"""

JS = r"""
const storageKey='staycode-learning-20260924';
let completed=new Set();
try{completed=new Set(JSON.parse(localStorage.getItem(storageKey)||'[]'));}catch(e){}
const boxes=[...document.querySelectorAll('[data-chapter]')];
function refresh(){
  boxes.forEach(b=>{b.checked=completed.has(b.dataset.chapter);const n=document.querySelector('.nav-list a[href="#'+b.dataset.chapter+'"]');if(n)n.classList.toggle('done',b.checked);});
  const count=boxes.filter(b=>b.checked).length;
  document.querySelector('.progress-text').textContent=count+' / '+boxes.length+' 章已完成 · 进度保存在当前浏览器';
  document.querySelector('.progress-fill').style.width=(boxes.length?count/boxes.length*100:0)+'%';
}
boxes.forEach(b=>b.addEventListener('change',()=>{if(b.checked)completed.add(b.dataset.chapter);else completed.delete(b.dataset.chapter);try{localStorage.setItem(storageKey,JSON.stringify([...completed]));}catch(e){}refresh();}));
refresh();
document.querySelector('.reset').addEventListener('click',()=>{completed.clear();try{localStorage.removeItem(storageKey);}catch(e){}refresh();});
document.querySelector('.print').addEventListener('click',()=>window.print());
document.querySelector('.mobile-toggle').addEventListener('click',e=>{const open=document.querySelector('.rail').classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',String(open));});
document.querySelector('.search').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();let visible=0;document.querySelectorAll('.nav-list li').forEach(li=>{const id=li.querySelector('a').getAttribute('href').slice(1);const s=document.getElementById(id);const ok=!q||(s?s.textContent:li.textContent).toLowerCase().includes(q);li.hidden=!ok;if(ok)visible++;});document.querySelector('.empty-search').style.display=visible?'none':'block';});
document.querySelectorAll('pre').forEach(pre=>{const button=document.createElement('button');button.className='copy';button.type='button';button.textContent='复制';button.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(pre.querySelector('code').textContent);button.textContent='已复制';setTimeout(()=>button.textContent='复制',1400);}catch(e){button.textContent='请选中复制';}});pre.appendChild(button);});
const sections=[...document.querySelectorAll('section[id]')];
const observer=new IntersectionObserver(entries=>{const first=entries.find(e=>e.isIntersecting);if(first){document.querySelectorAll('.nav-list a').forEach(a=>a.classList.toggle('active',a.hash==='#'+first.target.id));}},{rootMargin:'0px 0px -65% 0px',threshold:0});
sections.forEach(s=>observer.observe(s));
"""


def render(path: Path, is_main=False):
    source = path.read_text(encoding="utf-8")
    anchor_map = {title: anchor for anchor, title in re.findall(r'<a id="([^"]+)"></a>\s*\n## ([^\n]+)', source)}
    source = re.sub(r'^<a id="[^"]+"></a>\s*$', '', source, flags=re.M)
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    tokens = md.parse(source)
    nav = []
    last_id = None
    for i, token in enumerate(tokens):
        if token.type == "html_block":
            match = re.search(r'<a id="([^"]+)"></a>', token.content)
            if match:
                last_id = match.group(1)
                token.content = ""
        if token.type == "heading_open" and token.tag == "h2":
            title = tokens[i + 1].content
            anchor = anchor_map.get(title) or last_id or f"section-{len(nav)+1}"
            last_id = None
            token.attrSet("id", anchor)
            nav.append((anchor, title))
    body = md.renderer.render(tokens, md.options, {})
    body = re.sub(r'<pre><code class="language-mermaid">.*?</code></pre>',
                  lambda _: '<div class="diagram">'+architecture_svg()+'</div>', body, flags=re.S)
    # Group content into sections so chapter search and progress reflect the same text.
    body = re.sub(r'<h2 id="([^"]+)">', r'</section><section id="\1"><div class="chapter-head"><h2>', body)
    body = body.replace('</h2>', '</h2></div>')
    body = '<section class="intro" style="border:0;margin:0;padding:0">' + body + '</section>'
    for anchor, title in nav:
        if re.fullmatch(r'ch\d\d', anchor):
            needle = f'<section id="{anchor}"><div class="chapter-head"><h2>{html.escape(title)}</h2>'
            body = body.replace(needle, needle+f'<label class="complete"><input type="checkbox" data-chapter="{anchor}">已完成本章</label>')
    body = re.sub(r'<table>', '<div class="table-wrap"><table>', body).replace('</table>', '</table></div>')
    def convert_link(match):
        target = unquote(html.unescape(match.group(1)))
        if re.match(r'^[A-Za-z]:/', target):
            line = None
            suffix = re.search(r':(\d+)$', target)
            if suffix:
                line = suffix.group(1)
                target = target[:suffix.start()]
            p = Path(target)
            if p.parent == HERE and p.suffix == '.md':
                return f'href="{html.escape(p.with_suffix(".html").name, quote=True)}"'
            title = f' title="源码第 {line} 行；请在编辑器中定位"' if line else ''
            return f'href="{html.escape(p.as_uri(), quote=True)}"{title}'
        return match.group(0)
    body = re.sub(r'href="([^"]+)"', convert_link, body)
    nav_html = ''.join(f'<li><a href="#{a}">{html.escape(t)}</a></li>' for a,t in nav)
    title = 'Agent 架构与源码学习手册' if is_main else path.stem
    page = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="基于 StayCode 真实源码的 18 章 Agent 开发课程，含架构、调用链、离线实验与验收标准。"><title>{title} · StayCode</title><style>{CSS}</style></head>
<body><aside class="rail"><div class="eyebrow">SOURCE CODE STUDY / 2026</div><div class="brand">StayCode 学习笔记</div><small>从 LLM 应用走进 Agent 内核</small><button class="mobile-toggle" aria-expanded="false" aria-controls="nav-content">章节目录</button><div class="nav-content" id="nav-content"><input class="search" type="search" aria-label="搜索章节内容" placeholder="搜索章节内容…"><div class="progress-track"><div class="progress-fill"></div></div><div class="progress-text"></div><nav aria-label="章节目录"><ul class="nav-list">{nav_html}</ul><p class="empty-search">没有匹配章节，请换个关键词。</p></nav><div class="rail-bottom"><a href="Agent开发学习手册.html">学习手册</a><a href="源码导航.html">源码导航</a><a href="验证记录.html">验证记录</a><button class="reset">重置进度</button></div></div></aside>
<main><div class="topline"><span>架构 · 源码 · 实验 · 验证</span><button class="print">打印 / 保存 PDF</button></div><article>{body}</article><footer>源码快照日期 2026-09-24 · 离线阅读，无外部脚本依赖。进度保存在当前浏览器；不支持本地存储时仍可正常阅读。源码链接的行号请在编辑器中定位。</footer></main><script>{JS}</script></body></html>'''
    path.with_suffix('.html').write_text(page, encoding='utf-8')


def validate():
    errors = []
    source = MAIN.read_text(encoding='utf-8')
    anchors = set(re.findall(r'<a id="([^"]+)"', source))
    if len(re.findall(r'^## 第 \d+ 章', source, re.M)) != 18:
        errors.append('Expected exactly 18 chapters')
    for target in re.findall(r'\]\(([^)]+)\)', source):
        if target.startswith('#'):
            if target[1:] not in anchors:
                errors.append('Missing anchor '+target)
        elif re.match(r'^[A-Za-z]:/', target):
            location = re.sub(r':\d+$', '', target)
            if not Path(location).exists():
                errors.append('Missing file '+target)
            elif re.search(r':\d+$', target):
                n = int(target.rsplit(':', 1)[1])
                if n > len(Path(location).read_text(encoding='utf-8-sig').splitlines()):
                    errors.append('Line out of range '+target)
    if source.count('```') % 2:
        errors.append('Unbalanced code fences')
    page_report = {}
    for page in HERE.glob('*.html'):
        rendered = page.read_text(encoding='utf-8')
        hrefs = re.findall(r'href="([^"]+)"', rendered)
        resources = re.findall(r'<(?:script|img|link|iframe)[^>]+(?:src|href)="(https?://[^"]+)"', rendered)
        for target in hrefs:
            target = html.unescape(target)
            if target.startswith('file:///'):
                local = Path(unquote(urlparse(target).path).lstrip('/'))
                if not local.exists():
                    errors.append('Missing HTML source link '+str(local))
            elif not urlparse(target).scheme and not target.startswith('#'):
                if not (page.parent / unquote(target.split('#')[0])).exists():
                    errors.append('Missing HTML relative link '+target)
        page_report[page.name] = {'links':len(hrefs),'external_resource_dependencies':resources}
        if resources:
            errors.append('Unexpected external resource dependency '+page.name)
    (HERE / 'evidence/html-links.json').write_text(json.dumps(page_report,ensure_ascii=False,indent=2),encoding='utf-8')
    report = {'chapters':18, 'local_links_and_anchors':'passed' if not errors else 'failed',
              'errors':errors, 'markdown_characters':len(source),
              'html_bytes':MAIN.with_suffix('.html').stat().st_size}
    (HERE / 'evidence/document-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    inventory()
    for filename in ('Agent开发学习手册.md','源码导航.md','验证记录.md'):
        path = HERE / filename
        if path.exists():
            render(path, path == MAIN)
    validate()
