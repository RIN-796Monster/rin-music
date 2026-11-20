# -*- coding: utf-8 -*-
import qrcode, os

# --- QR target URLs ---
urls = {
    "hp": "https://rin-music.vercel.app/",
    "sp": "https://open.spotify.com/intl-ja/artist/47PIO5ogSohxvdA96vMnmz?si=KeWZNXi-Qda-noKsMoOXTA",
    "am": "https://music.apple.com/jp/artist/rin/6771279389",
    "tt": "https://www.tiktok.com/@rin_796monster",
    "x":  "https://x.com/RIN_796",
}
# display order left -> right with tile x and label
slots = [
    ("hp", 112, "公式HP"),
    ("sp", 212, "Spotify"),
    ("am", 312, "Apple Music"),
    ("tt", 412, "TikTok"),
    ("x",  512, "X"),
]
TILE = 56
TY = 832

def qr_rects(key, x0):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=2, box_size=10)
    q.add_data(urls[key]); q.make(fit=True)
    m = q.get_matrix(); n = len(m); px = TILE / n
    out = []
    for r in range(n):
        run = None
        for c in range(n):
            dark = m[r][c]
            if dark and run is None:
                run = c
            if (not dark or c == n-1) and run is not None:
                end = c if not dark else c+1
                out.append(f'<rect x="{x0+run*px:.2f}" y="{TY+r*px:.2f}" width="{(end-run)*px:.2f}" height="{px:.2f}" fill="#0b0a09"/>')
                run = None
    return "".join(out)

qr_svg = "\n".join(qr_rects(k, x) for (k, x, _) in slots)
tiles_svg = "\n".join(f'<rect x="{x}" y="{TY}" width="56" height="56" rx="4" fill="#ffffff"/>' for (_, x, _) in slots)
qr_labels = "\n".join(
    f'<text x="{x+28}" y="902" text-anchor="middle" fill="#9b9486" style="font-family:sans-serif;font-size:10px;letter-spacing:1px;">{lbl}</text>'
    for (_, x, lbl) in slots
)

mincho = "'Yu Mincho','Hiragino Mincho ProN','Noto Serif JP',serif"

# inner design uses original A4 coords (680x962). It is wrapped in a translate(10,10)
# group so a 3mm (10px) bleed surrounds it on all sides -> full canvas 700x982.
inner = f'''<g transform="translate(10,10)">
<rect x="40" y="40" width="600" height="882" fill="none" stroke="#3a342a" stroke-width="0.75"/>

<text x="90" y="92" fill="#b9956a" style="font-family:sans-serif;font-size:13px;letter-spacing:7px;">A  MUSIC  PROJECT</text>
<text x="590" y="92" text-anchor="end" fill="#6b6356" style="font-family:sans-serif;font-size:11px;letter-spacing:2px;">rin-music.vercel.app</text>

<text x="340" y="232" text-anchor="middle" fill="#ede6d6" style="font-family:Georgia,'Times New Roman',serif;font-size:112px;letter-spacing:2px;">RIN.</text>
<line x1="300" y1="296" x2="380" y2="296" stroke="#b9956a" stroke-width="1"/>

<text x="340" y="368" text-anchor="middle" fill="#d8b988" style="font-family:{mincho};font-size:31px;letter-spacing:2px;">62歳、AIと音楽を始めました。</text>

<text x="340" y="438" text-anchor="middle" fill="#c8c1b3" style="font-family:{mincho};font-size:14.5px;letter-spacing:1.5px;">生成AIは、特別な才能を持つ人だけのものではなく、</text>
<text x="340" y="468" text-anchor="middle" fill="#c8c1b3" style="font-family:{mincho};font-size:14.5px;letter-spacing:1.5px;">誰かの中にある「表現したい」という気持ちを、広げられるのか。</text>
<text x="340" y="510" text-anchor="middle" fill="#9b9486" style="font-family:{mincho};font-size:14.5px;letter-spacing:1.5px;">RIN.は、その問いを、自分自身で試しています。</text>

<line x1="90" y1="548" x2="590" y2="548" stroke="#3a342a" stroke-width="0.75"/>
<text x="90" y="574" fill="#b9956a" style="font-family:sans-serif;font-size:11px;letter-spacing:4px;">SONGS</text>
<text x="90" y="598" fill="#d8d2c5" style="font-family:{mincho};font-size:14px;">私はここにいる / I Am Here</text>
<text x="90" y="621" fill="#d8d2c5" style="font-family:{mincho};font-size:14px;">消えないで All Night / Don't Disappear, All Night</text>
<text x="90" y="644" fill="#d8d2c5" style="font-family:{mincho};font-size:14px;">Weekend Lonely</text>
<text x="90" y="667" fill="#d8d2c5" style="font-family:{mincho};font-size:14px;">オルタナティブラブ / Alternative Love</text>
<text x="90" y="690" fill="#d8d2c5" style="font-family:{mincho};font-size:14px;">Look Up, Me</text>
<text x="90" y="713" fill="#8a8174" style="font-family:{mincho};font-size:12.5px;">Coming Soon — 僕がオバさんになっても（配信準備中）</text>

<line x1="90" y1="734" x2="590" y2="734" stroke="#3a342a" stroke-width="0.75"/>
<text x="90" y="757" fill="#8a8174" style="font-family:{mincho};font-size:11.5px;">RIN.（岡部鈴）— トランスジェンダー女性。広告会社の管理部門等を経て、</text>
<text x="90" y="775" fill="#8a8174" style="font-family:{mincho};font-size:11.5px;">62歳から音楽制作を開始。生成AIで世界配信に挑戦中。</text>
<text x="90" y="793" fill="#8a8174" style="font-family:{mincho};font-size:11.5px;">日本語歌詞、英語歌詞で全曲リリース。</text>

<text x="90" y="822" fill="#b9956a" style="font-family:sans-serif;font-size:11px;letter-spacing:4px;">LISTEN &amp; FOLLOW</text>
{tiles_svg}
{qr_svg}
{qr_labels}
</g>'''

defs_bg = '''<defs>
<radialGradient id="spot2" cx="50%" cy="30%" r="48%">
<stop offset="0%" stop-color="#2a2620"/>
<stop offset="55%" stop-color="#141210"/>
<stop offset="100%" stop-color="#0b0a09"/>
</radialGradient>
</defs>
<rect x="0" y="0" width="700" height="982" fill="#0b0a09"/>
<rect x="0" y="0" width="700" height="982" fill="url(#spot2)"/>'''

title = '<title>RIN. 音楽プロジェクト フライヤー</title><desc>62歳、AIと音楽を始めました。A4＋塗り足し3mm。</desc>'

# 1) Print SVG sized in mm (216 x 303 = A4 + 3mm bleed all sides)
svg_mm = f'<svg width="216mm" height="303mm" viewBox="0 0 700 982" xmlns="http://www.w3.org/2000/svg" role="img">{title}{defs_bg}{inner}</svg>'
# 2) Pixel SVG for raster preview
svg_px = f'<svg width="700" height="982" viewBox="0 0 700 982" xmlns="http://www.w3.org/2000/svg" role="img">{title}{defs_bg}{inner}</svg>'
# 3) HTML wrapper for borderless PDF print at exact 216x303mm
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: 216mm 303mm; margin: 0; }}
html,body {{ margin:0; padding:0; background:#0b0a09; }}
svg {{ display:block; width:216mm; height:303mm; }}
</style></head><body>{svg_mm}</body></html>'''

base = os.path.dirname(os.path.abspath(__file__))
for name, content in [("RIN_flyer.svg", svg_mm), ("RIN_flyer_px.svg", svg_px), ("RIN_flyer_print.html", html)]:
    with open(os.path.join(base, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("WROTE:", os.path.join(base, name))
