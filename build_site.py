# -*- coding: utf-8 -*-
"""组件武器库 V2 - 生成脚本"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
final = json.load(open('/tmp/21st_final.json'))
aceternity = json.load(open('/tmp/aceternity.json'))

magicui = ['android','animated-beam','animated-circular-progress-bar','animated-gradient-text',
'animated-grid-pattern','animated-list','animated-shiny-text','animated-theme-toggler','aurora-text',
'avatar-circles','backlight','bento-grid','blur-fade','border-beam','code-comparison','comic-text',
'confetti','cool-mode','dia-text-reveal','dock','dot-pattern','dotted-map','file-tree','flickering-grid',
'floating-3d-particles','glare-hover','globe','glyph-matrix','grid-pattern','hero-video-dialog',
'hexagon-pattern','highlighter','hyper-text','icon-cloud','interactive-grid-pattern',
'interactive-hover-button','iphone','kinetic-text','lens','light-rays','line-shadow-text','magic-card',
'marquee','meteors','morphing-text','neon-gradient-card','noise-texture','number-ticker',
'orbiting-circles','particles','pixel-image','pointer','progressive-blur','pulsating-button',
'rainbow-button','retro-grid','ripple','ripple-button','safari','scroll-based-velocity',
'scroll-progress','shimmer-button','shine-border','shiny-button','smooth-cursor','sparkles-text',
'spinning-text','striped-pattern','terminal','text-3d-flip','text-animate','text-reveal','tweet-card',
'typing-animation','video-text','warp-background','word-rotate']

cat_meta = [
    ('all', '全部'), ('hero', '首屏 Hero'), ('pricing-section', '定价区'),
    ('testimonials', '客户评价'), ('ai-chat', 'AI 对话'), ('features', '特性展示'),
    ('cta', '行动号召'), ('shader', '着色器背景'), ('3d', '3D 立体'),
    ('glassmorphism', '玻璃拟态'), ('bento', 'Bento 网格'), ('text', '文字特效'),
    ('animation', '动效'), ('carousel', '轮播'), ('card', '卡片'),
    ('dashboard', '仪表盘'), ('navbar', '导航栏'), ('button', '按钮'),
    ('loader', '加载动画'), ('footer', '页脚'), ('toggle', '开关'),
    ('tag', '标签徽章'), ('input', '输入控件'), ('table', '表格'), ('calendar', '日历'),
]

def clean(s):
    return (s or '').replace('\n', ' ').strip()

data = []
for s in final:
    data.append({
        'name': clean(s['name']) or s['cname'],
        'cname': s['cname'], 'author': s['author'],
        'desc': clean(s['desc'])[:200],
        'cat': s['cat'], 'bm': s['bm'],
        'views': s.get('views') or 0, 'dl': s.get('dl') or 0,
        'preview': s['preview'], 'video': s['video'], 'demo': s['demo'],
        'url': s['url'], 'install': s['install'],
        'tags': [clean(t) for t in (s.get('tags') or [])[:3] if clean(t)],
    })

ace = [{'t': a['title'], 'u': 'https://ui.aceternity.com/components/' + a['slug']} for a in aceternity]
mag = [{'t': m.replace('-', ' ').title(),
        'u': 'https://magicui.design/docs/components/' + m,
        'i': 'npx shadcn@latest add "https://magicui.design/r/%s.json"' % m} for m in magicui]

def js_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

tpl = open(os.path.join(BASE, 'template.html'), encoding='utf-8').read()
out = (tpl
    .replace('__TOTAL__', str(len(data)))
    .replace('__VIDS__', str(sum(1 for d in data if d['video'])))
    .replace('__CATS_N__', str(len([c for c in cat_meta if c[0] != 'all'])))
    .replace('__DATA_JSON__', js_json(data))
    .replace('__ACE_JSON__', js_json(ace))
    .replace('__MAG_JSON__', js_json(mag))
    .replace('__CAT_JSON__', js_json([{'k': k, 'n': n} for k, n in cat_meta])))

path = os.path.join(BASE, 'index.html')
open(path, 'w', encoding='utf-8').write(out)
print('written:', path, '%.0f KB' % (os.path.getsize(path) / 1024))
