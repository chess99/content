import sharp from 'file:///C:/Users/zcs/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/lib/index.js';
import fs from 'node:fs/promises';
import path from 'node:path';

const outputDir = path.resolve('D:/code/content/topics/20260812-vercel-vs-cloudflare/image-post/images');
const sourceDir = path.resolve('D:/code/content/topics/20260812-vercel-vs-cloudflare/image-post/source');
await fs.mkdir(outputDir, { recursive: true });

const palette = {
  paper: '#F7F3EA',
  ink: '#17191C',
  muted: '#5F6671',
  line: '#CBD0D6',
  blue: '#315CFF',
  blueSoft: '#E8EDFF',
  white: '#FFFDF8',
};

function escapeXml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function t(x, y, value, size, weight = 500, fill = palette.ink, anchor = 'start') {
  return `<text x="${x}" y="${y}" font-family="Noto Sans SC, Microsoft YaHei, sans-serif" font-size="${size}" font-weight="${weight}" fill="${fill}" text-anchor="${anchor}">${escapeXml(value)}</text>`;
}

function pill(x, y, width, label) {
  return `<rect x="${x}" y="${y}" width="${width}" height="52" rx="26" fill="${palette.blueSoft}"/>${t(x + width / 2, y + 36, label, 25, 650, palette.blue, 'middle')}`;
}

function baseSvg(content) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440">
    <rect width="1080" height="1440" fill="${palette.paper}"/>
    <circle cx="982" cy="88" r="145" fill="${palette.blueSoft}"/>
    <circle cx="102" cy="1352" r="102" fill="#EEF0F2"/>
    ${content}
  </svg>`;
}

const card1 = baseSvg(`
  ${pill(72, 72, 216, '部署平台选择')}
  ${t(72, 190, 'Vercel 还是 Cloudflare？', 60, 760)}
  ${t(72, 258, '先看项目需要什么', 42, 650, palette.blue)}
  <line x1="72" y1="310" x2="1008" y2="310" stroke="${palette.line}" stroke-width="2"/>

  <rect x="72" y="358" width="452" height="828" rx="28" fill="${palette.white}" stroke="${palette.line}" stroke-width="2"/>
  <rect x="556" y="358" width="452" height="828" rx="28" fill="${palette.white}" stroke="${palette.line}" stroke-width="2"/>
  <rect x="72" y="358" width="452" height="12" rx="6" fill="${palette.ink}"/>
  <rect x="556" y="358" width="452" height="12" rx="6" fill="${palette.blue}"/>

  ${t(112, 450, 'Vercel', 47, 760)}
  ${t(596, 450, 'Cloudflare', 47, 760, palette.blue)}

  ${t(112, 540, 'Next.js 原生平台', 31, 650)}
  ${t(112, 600, '完整 Node.js 支持更直接', 28, 500, palette.muted)}
  ${t(112, 650, '更高的函数内存上限', 28, 500, palette.muted)}

  ${t(596, 540, 'Workers 边缘运行环境', 31, 650)}
  ${t(596, 600, '静态资源请求免费且不限量', 28, 500, palette.muted)}
  ${t(596, 650, 'R2 免互联网出口流量费', 28, 500, palette.muted)}

  <line x1="112" y1="730" x2="484" y2="730" stroke="${palette.line}" stroke-width="2"/>
  <line x1="596" y1="730" x2="968" y2="730" stroke="${palette.line}" stroke-width="2"/>
  ${t(112, 800, '常见场景', 25, 650, palette.blue)}
  ${t(112, 865, '标准 Next.js', 32, 650)}
  ${t(112, 920, '依赖完整 Node.js', 32, 650)}
  ${t(112, 975, '服务端计算较重', 32, 650)}

  ${t(596, 800, '常见场景', 25, 650, palette.blue)}
  ${t(596, 865, '静态资源较多', 32, 650)}
  ${t(596, 920, '文件流量较多', 32, 650)}
  ${t(596, 975, '维护多个小站', 32, 650)}

  <rect x="72" y="1232" width="936" height="126" rx="28" fill="${palette.ink}"/>
  ${t(540, 1312, '两家都能上站，项目条件决定选择', 34, 650, palette.white, 'middle')}
`);

const rows = [
  ['依赖 Workers 尚不支持的 Node.js API', '先看 Vercel'],
  ['静态资源多 / 动态逻辑轻', '先看 Static Assets'],
  ['图片 / PDF / 下载文件多', '先看 R2，应用平台另选'],
  ['本地重计算 / 高内存', 'Vercel 或独立后端'],
  ['主要调用数据库、支付、外部 AI API', '两边都可以'],
];

let rowSvg = '';
rows.forEach(([condition, answer], index) => {
  const y = 322 + index * 174;
  rowSvg += `<rect x="72" y="${y}" width="936" height="142" rx="24" fill="${index % 2 ? palette.white : palette.blueSoft}" stroke="${index % 2 ? palette.line : palette.blueSoft}" stroke-width="2"/>`;
  rowSvg += `<circle cx="122" cy="${y + 71}" r="25" fill="${palette.blue}"/>`;
  rowSvg += t(122, y + 80, String(index + 1), 24, 760, palette.white, 'middle');
  rowSvg += t(166, y + 58, condition, 29, 560, palette.ink);
  rowSvg += t(166, y + 105, `→ ${answer}`, 30, 700, palette.blue);
});

const card2 = baseSvg(`
  ${pill(72, 72, 176, '决策卡')}
  ${t(72, 195, '按这 5 个条件选', 64, 760)}
  ${t(72, 260, '只保留真正会改变答案的条件', 30, 500, palette.muted)}
  ${rowSvg}
  <rect x="72" y="1240" width="936" height="118" rx="26" fill="${palette.ink}"/>
  ${t(540, 1313, '没有明显偏向：选与现有代码更匹配的', 32, 650, palette.white, 'middle')}
`);

for (const [name, svg] of [['01-key-differences', card1], ['02-decision-card', card2]]) {
  await fs.writeFile(path.join(sourceDir, `${name}.svg`), svg, 'utf8');
  await sharp(Buffer.from(svg)).png({ compressionLevel: 9 }).toFile(path.join(outputDir, `${name}.png`));
}
