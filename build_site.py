# -*- coding: utf-8 -*-
"""组件武器库 V3 - 生成脚本（59 分类全量）"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
final = json.load(open('/tmp/21st_final_v3.json'))
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
    ('glassmorphism', '玻璃拟态'), ('liquid-glass', '液态玻璃'), ('bento', 'Bento 网格'),
    ('text', '文字特效'), ('animation', '动效'), ('carousel', '轮播'), ('card', '卡片'),
    ('dashboard', '仪表盘'), ('navbar', '导航栏'), ('button', '按钮'),
    ('loader', '加载动画'), ('footer', '页脚'), ('toggle', '开关'),
    ('tag', '标签徽章'), ('input', '输入控件'), ('table', '表格'), ('calendar', '日历'),
    # 新增分类
    ('coming-soon', '上线倒计时页'), ('404', '404 页面'), ('login', '登录页'),
    ('sign-up', '注册页'), ('faq', 'FAQ 问答'), ('stats', '数据统计'),
    ('timeline', '时间线'), ('roadmap', '路线图'), ('logo-cloud', 'Logo 墙'),
    ('logo-marquee', 'Logo 跑马灯'), ('marquee', '跑马灯'), ('countdown', '倒计时'),
    ('waitlist', 'Waitlist'), ('comparison-slider', '对比滑块'), ('video-background', '视频背景'),
    ('sidebar', '侧边栏'), ('tabs', '选项卡'), ('accordion', '手风琴'),
    ('modal', '弹窗'), ('dropdown', '下拉菜单'), ('tooltip', '气泡提示'),
    ('mega-menu', '超级菜单'), ('portfolio', '作品集'), ('profile-card', '个人卡片'),
    ('empty-state', '空状态'), ('parallax', '视差'), ('particle', '粒子'),
    ('cursor-trail', '光标拖尾'), ('sphere', '球体'), ('globe', '3D 地球'),
    ('holographic', '全息'), ('glitch', '故障风'), ('neon', '霓虹'),
    ('dock', 'Dock 栏'),
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

# ---- Codrops 教程库 ----
cd_raw = []
try:
    cd_raw = json.load(open('/tmp/codrops_tuts_full.json'))
    cd_raw += json.load(open('/tmp/codrops_extra.json'))
except FileNotFoundError:
    pass

def cd_date(s):
    # 'Sep 24, 2026' -> '2026.09.24'
    import re
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    m = re.match(r'([A-Z][a-z]{2})\s+(\d{1,2}),\s+(\d{4})', s or '')
    if m:
        return f'{m.group(3)}.{months.get(m.group(1),"??")}.{int(m.group(2)):02d}'
    return (s or '')[:10]

cd = []
for x in cd_raw:
    if x.get('cat') and x.get('cat') != 'tutorials':
        c = x['cat']
    else:
        c = 'tutorials'
    cd.append({
        'c': c,
        'ti': clean(x.get('title')),
        'u': x['url'],
        'i': x.get('img'),
        'd': clean(x.get('desc'))[:160],
        'dt': cd_date(x.get('date', '')),
        't': [clean(t) for t in (x.get('tags') or [])[:6]],
    })
# 去重
seen = set(); cd = [x for x in cd if not (x['u'] in seen or seen.add(x['u']))]
print('codrops items:', len(cd))

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
    .replace('__CD_JSON__', js_json(cd))
    .replace('__GS_JSON__', js_json(json.load(open('/tmp/gsap_skills_data.json'))))
    .replace('__CAT_JSON__', js_json([{'k': k, 'n': n} for k, n in cat_meta])))

path = os.path.join(BASE, 'index.html')
open(path, 'w', encoding='utf-8').write(out)
print('written:', path, '%.0f KB' % (os.path.getsize(path) / 1024))
print('items:', len(data), '| cats:', len(cat_meta) - 1)
