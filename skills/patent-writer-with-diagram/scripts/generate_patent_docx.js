#!/usr/bin/env node
/**
 * generate_patent_docx.js
 * Usage: NODE_PATH=/usr/local/lib/node_modules node generate_patent_docx.js --input data.json --output out.docx
 */
const { Document, Packer, Paragraph, TextRun, ImageRun,
        AlignmentType, LevelFormat, BorderStyle, WidthType, ShadingType,
        Table, TableRow, TableCell } = require('docx');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ── args ──────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i >= 0 ? args[i + 1] : null; };
const inputFile = get('--input');
const outputFile = get('--output');
if (!inputFile || !outputFile) {
  console.error('Usage: node generate_patent_docx.js --input data.json --output out.docx');
  process.exit(1);
}
const data = JSON.parse(fs.readFileSync(inputFile, 'utf8'));

// ── helpers ───────────────────────────────────────────────────────────────────
const FONT = 'Microsoft YaHei';
const S = 24;
const border = { style: BorderStyle.SINGLE, size: 4, color: '000000' };
const cellBorders = { top: border, bottom: border, left: border, right: border };
const WHITE = 'FFFFFF';

const p = (children, opts = {}) => new Paragraph({ children, ...opts });
const t = (text, opts = {}) => new TextRun({ text, size: S, font: FONT, ...opts });
const tGray = (text) => new TextRun({ text, size: 20, color: '808080', font: FONT });
const tBold = (text) => new TextRun({ text, size: S, bold: true, font: FONT });

const labelCell = (text, w) => new TableCell({
  width: { size: w, type: WidthType.DXA }, borders: cellBorders,
  shading: { fill: WHITE, type: ShadingType.CLEAR },
  children: [p([tBold(text)])]
});
const valueCell = (text, w, span) => {
  const opts = {
    width: { size: w, type: WidthType.DXA }, borders: cellBorders,
    shading: { fill: WHITE, type: ShadingType.CLEAR },
    children: [p([t(text)])]
  };
  if (span) opts.columnSpan = span;
  return new TableCell(opts);
};

// ── info table ────────────────────────────────────────────────────────────────
function buildInfoTable(d) {
  const inventors = Array.isArray(d.inventors) ? d.inventors.join(' ') : (d.inventors || '');
  const c = d.contact || {};
  return new Table({
    width: { size: 10111, type: WidthType.DXA },
    columnWidths: [1360, 3348, 1752, 3651],
    rows: [
      new TableRow({ children: [labelCell('专利名称', 1360), valueCell(d.patent_name || '', 8751, 3)] }),
      new TableRow({ children: [labelCell('专利类型', 1360), valueCell(d.patent_type || '', 3348), labelCell('发明人', 1752), valueCell(inventors, 3651)] }),
      new TableRow({ children: [
        labelCell('联系人', 1360), valueCell(c.name || '', 3348),
        new TableCell({
          width: { size: 5403, type: WidthType.DXA }, columnSpan: 2, borders: cellBorders,
          shading: { fill: WHITE, type: ShadingType.CLEAR },
          children: [
            p([tBold('联系电话'), t('  ' + (c.phone || ''))]),
            p([tBold('e-mail：'), t('  ' + (c.email || ''))]),
          ]
        }),
      ]}),
    ]
  });
}

// ── flow chart image (optional, 发明专利专用) ─────────────────────────────────
function buildFlowChart(scenes) {
  if (!scenes || scenes.length === 0) return null;
  const tmpPng = '/tmp/_patent_flow_chart.png';
  const pyScript = '/tmp/_patent_flow_gen.py';
  const py = `
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import os, json

scenes = ${JSON.stringify(scenes)}

# 找中文字体
font_paths = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode MS.ttf",
]
font_prop = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_prop = fm.FontProperties(fname=fp, size=10)
            break
        except: pass

n_scenes = len(scenes)
fig_h = 2.8 * n_scenes
fig, axes = plt.subplots(n_scenes, 1, figsize=(11, fig_h))
if n_scenes == 1:
    axes = [axes]

BLUE      = '#3B6FD4'
LIGHT_BG  = '#EEF3FC'
ARROW_CLR = '#7A9ED4'
TITLE_CLR = '#FFFFFF'
TEXT_CLR  = '#1A1A2E'
BORDER    = '#3B6FD4'

for ax, scene in zip(axes, scenes):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # 标题栏
    title_box = FancyBboxPatch((0.01, 0.72), 0.98, 0.24,
        boxstyle="round,pad=0.01", linewidth=0,
        facecolor=BLUE, zorder=2)
    ax.add_patch(title_box)
    kw = dict(fontproperties=font_prop) if font_prop else {}
    ax.text(0.5, 0.84, scene['title'], ha='center', va='center',
            color=TITLE_CLR, fontsize=11, fontweight='bold', **kw)

    steps = scene['steps']
    n = len(steps)
    margin = 0.03
    arrow_w = 0.045
    total_arrow = arrow_w * (n - 1)
    box_w = (1 - 2 * margin - total_arrow) / n
    box_h = 0.52
    box_y = 0.08

    for i, step in enumerate(steps):
        x0 = margin + i * (box_w + arrow_w)
        # 步骤框
        box = FancyBboxPatch((x0, box_y), box_w, box_h,
            boxstyle="round,pad=0.015", linewidth=1.2,
            edgecolor=BORDER, facecolor=LIGHT_BG, zorder=2)
        ax.add_patch(box)

        # 步骤编号圆形背景（用 scatter 画点，自动保持正圆）
        cx = x0 + box_w / 2
        dot_y = box_y + box_h - 0.1
        ax.scatter([cx], [dot_y], s=700, color=BLUE, zorder=3, clip_on=False)
        ax.text(cx, dot_y, str(i + 1),
                ha='center', va='center', color='white',
                fontsize=8, fontweight='bold', zorder=4)

        # 步骤文字（最多2行，自动换行）
        words = list(step)
        mid = len(words) // 2
        if len(words) <= 8:
            lines = [step]
        else:
            lines = [''.join(words[:mid]), ''.join(words[mid:])]
        text_y = box_y + box_h * 0.38
        line_gap = 0.13
        for li, line in enumerate(lines):
            ax.text(cx, text_y - li * line_gap, line,
                    ha='center', va='center', color=TEXT_CLR,
                    fontsize=9, **kw)

        # 箭头
        if i < n - 1:
            ax_start = x0 + box_w + 0.004
            ax_end   = x0 + box_w + arrow_w - 0.004
            ay = box_y + box_h / 2
            ax.annotate('', xy=(ax_end, ay), xytext=(ax_start, ay),
                arrowprops=dict(arrowstyle='->', color=ARROW_CLR,
                                lw=1.8, mutation_scale=14))

plt.tight_layout(pad=0.4)
plt.savefig("${tmpPng}", dpi=180, bbox_inches='tight',
            facecolor='white', format='PNG')
plt.close()
`;
  fs.writeFileSync(pyScript, py);
  try {
    execSync(`python3 ${pyScript}`, { stdio: 'pipe' });
    return fs.readFileSync(tmpPng);
  } catch (e) {
    console.warn('Flow chart generation failed:', e.message);
    return null;
  }
}

// ── document body ─────────────────────────────────────────────────────────────
function buildDoc(d) {
  const numConfig = [
    { reference: 'num1', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'num2', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'bullet1', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ];

  const drawbacks = Array.isArray(d.drawbacks) ? d.drawbacks : [];
  const advantages = Array.isArray(d.advantages) ? d.advantages : [];
  // 兼容新格式 description_scenes 和旧格式 description（平铺段落）
  const scenes = Array.isArray(d.description_scenes) ? d.description_scenes
    : Array.isArray(d.description) ? [{ title: null, items: d.description }]
    : [];
  const flowChartBuf = buildFlowChart(d.flow_chart_scenes);

  const children = [
    p([new TextRun({ text: '专利申请技术交底书', bold: true, size: 32, font: FONT })], { alignment: AlignmentType.CENTER, spacing: { after: 300 } }),
    buildInfoTable(d),
    p([t('针对上次评审意见的补充材料:')], { spacing: { before: 200, after: 300 } }),

    // §1
    p([tGray('1 Background: What is the problem solved by your invention? Describe known solutions to this problem (if any). What are the drawbacks of such known solutions, or why is an additional solution required? Cite any relevant technical documents or references.')], { spacing: { after: 60 } }),
    p([tGray('1 背景: 你的方案要解决什么问题？ 描述一下针对该问题的现有解决方案(如果有找到的话)。现有解决方案的缺点在哪里，或者为什么需要其他的解决方案？列出检索到的对比文件并进行分析比较。')], { spacing: { after: 200 } }),
    p([tBold('问题的描述:')], { spacing: { after: 100 } }),
    p([t(d.background || '')], { spacing: { after: 200 } }),
    p([tBold('现存问题的缺点：')], { spacing: { after: 100 } }),
    ...drawbacks.map(item => p([t(item)], { numbering: { reference: 'num1', level: 0 }, spacing: { after: 60 } })),
    p([], { spacing: { after: 200 } }),

    // §2
    p([tGray('2,Summary of Invention: Briefly describe the core idea of your invention(saving the details for question #3 below). Describe the advantage(s) of using your invention instead of the known solutions described above.')], { spacing: { after: 60 } }),
    p([tGray('2，发明要点：简要地描述你的方案的核心要点（略去一些细节），描述一下采用你的方案来替代现有方案后获得的优势')], { spacing: { after: 200 } }),
    p([tBold('针对上述问题和现有解决方案的缺陷,本方案提出:')], { spacing: { after: 100 } }),
    p([t(d.summary || '')], { spacing: { after: 200 } }),
    p([tBold('采用本方案的优势：')], { spacing: { after: 100 } }),
    ...advantages.map(item => p([t(item)], { numbering: { reference: 'num2', level: 0 }, spacing: { after: 60 } })),
    p([], { spacing: { after: 200 } }),

    // §3
    p([tGray('3,Description: Describe how your invention works, and how it could be implemented, using text, diagrams and flow charts as appropriate.')], { spacing: { after: 60 } }),
    p([tGray('3，描述：采用适当的文字，框图，流程图来描述你的方案是如何工作的，该方案要怎么做就可以获得实施,如何实现的。')], { spacing: { after: 200 } }),
    p([tBold('交互行为描述：')], { spacing: { after: 100 } }),
  ];

  // ── §3 description scenes：每个场景文字 + 紧跟对应图片（图文交织）──────────
  const figmaImages = Array.isArray(d.figma_images) ? d.figma_images : [];

  // 构建 sceneIndex → images[] 映射
  const sceneImgMap = {};
  let autoIdx = 0;
  for (const entry of figmaImages) {
    const imgPath = typeof entry === 'string' ? entry : entry.path;
    const caption = typeof entry === 'object' ? (entry.caption || '') : '';
    const annotations = typeof entry === 'object' && Array.isArray(entry.annotations) ? entry.annotations : [];
    const sceneIdx = (typeof entry === 'object' && entry.scene_index != null)
      ? entry.scene_index : autoIdx++;
    if (!sceneImgMap[sceneIdx]) sceneImgMap[sceneIdx] = [];
    sceneImgMap[sceneIdx].push({ imgPath, caption, annotations });
  }

  // 渲染图片块的辅助函数
  function renderImage(imgPath, caption, annotations) {
    try {
      const imgBuf = fs.readFileSync(imgPath);
      const sizeOf = (() => {
        if (imgBuf[0] === 0x89 && imgBuf[1] === 0x50 && imgBuf[2] === 0x4E && imgBuf[3] === 0x47) {
          return { width: imgBuf.readUInt32BE(16), height: imgBuf.readUInt32BE(20) };
        }
        return { width: 1200, height: 800 };
      })();
      const maxW = 595, maxH = 421;
      const scale = Math.min(1, maxW / sizeOf.width, maxH / sizeOf.height);
      const blocks = [];
      blocks.push(new Paragraph({
        children: [new ImageRun({ data: imgBuf, transformation: { width: Math.round(sizeOf.width * scale), height: Math.round(sizeOf.height * scale) } })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 60 }
      }));
      if (caption) {
        blocks.push(p([new TextRun({ text: caption, size: 20, color: '555555', font: FONT, italics: true })], { alignment: AlignmentType.CENTER, spacing: { after: 80 } }));
      }
      if (annotations.length > 0) {
        annotations.forEach((note, i) => {
          const text = annotations.length === 1 ? note : `${i + 1}. ${note}`;
          blocks.push(p([t(text)], { spacing: { after: 60 }, indent: { left: 360 } }));
        });
      }
      blocks.push(p([], { spacing: { after: 160 } }));
      return blocks;
    } catch (e) {
      console.warn(`Skipping image ${imgPath}:`, e.message);
      return [];
    }
  }

  // 逐场景渲染：文字 → 图片
  for (let si = 0; si < scenes.length; si++) {
    const scene = scenes[si];
    if (scene.title) children.push(p([tBold(scene.title)], { spacing: { after: 100 } }));
    for (const item of (scene.items || [])) {
      children.push(p([t(item)], { numbering: { reference: 'bullet1', level: 0 }, spacing: { after: 60 } }));
    }
    const imgs = sceneImgMap[si] || [];
    for (const { imgPath, caption, annotations } of imgs) {
      children.push(...renderImage(imgPath, caption, annotations));
    }
    if (imgs.length === 0) children.push(p([], { spacing: { after: 140 } }));
  }

  // scene 数量之外剩余的图片追加在末尾
  const extraKeys = Object.keys(sceneImgMap).map(Number).filter(k => k >= scenes.length);
  for (const k of extraKeys.sort((a, b) => a - b)) {
    for (const { imgPath, caption, annotations } of sceneImgMap[k]) {
      children.push(...renderImage(imgPath, caption, annotations));
    }
  }

  // ── §4 技术实现（发明专利，图文交织）────────────────────────────────────────
  const techScenes = Array.isArray(d.tech_scenes) ? d.tech_scenes : [];
  const archImages = Array.isArray(d.arch_images) ? d.arch_images : [];

  if (techScenes.length > 0 || flowChartBuf || archImages.length > 0) {
    children.push(p([tGray('4,Technical Implementation: Describe the technical implementation details.')], { spacing: { after: 60 } }));
    children.push(p([tGray('4，技术实现：描述方案的技术实现细节。')], { spacing: { after: 200 } }));

    if (techScenes.length > 0) {
      const archImgMap = {};
      let archAutoIdx = 0;
      for (const entry of archImages) {
        const imgPath = typeof entry === 'string' ? entry : entry.path;
        const caption = typeof entry === 'object' ? (entry.caption || '') : '';
        const annotations = typeof entry === 'object' && Array.isArray(entry.annotations) ? entry.annotations : [];
        const sceneIdx = (typeof entry === 'object' && entry.scene_index != null)
          ? entry.scene_index : archAutoIdx++;
        if (!archImgMap[sceneIdx]) archImgMap[sceneIdx] = [];
        archImgMap[sceneIdx].push({ imgPath, caption, annotations });
      }

      for (let ti = 0; ti < techScenes.length; ti++) {
        const ts = techScenes[ti];
        if (ts.title) children.push(p([tBold(ts.title)], { spacing: { after: 100 } }));
        for (const item of (ts.items || [])) {
          children.push(p([t(item)], { numbering: { reference: 'bullet1', level: 0 }, spacing: { after: 60 } }));
        }
        const archImgs = archImgMap[ti] || [];
        for (const { imgPath, caption, annotations } of archImgs) {
          children.push(...renderImage(imgPath, caption, annotations));
        }
        if (archImgs.length === 0) children.push(p([], { spacing: { after: 140 } }));
      }
    }

    // flow chart
    if (flowChartBuf) {
      const fcW = flowChartBuf.readUInt32BE(16);
      const fcH = flowChartBuf.readUInt32BE(20);
      const fcScale = Math.min(1, 595 / fcW);
      children.push(p([tBold('关键交互流程草图：')], { spacing: { after: 120 } }));
      children.push(new Paragraph({
        children: [new ImageRun({ data: flowChartBuf, transformation: { width: Math.round(fcW * fcScale), height: Math.round(fcH * fcScale) } })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 }
      }));
    }
  }

  return new Document({
    numbering: { config: numConfig },
    styles: { default: { document: { run: { font: FONT, size: S } } } },
    sections: [{
      properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      children
    }]
  });
}

// ── run ───────────────────────────────────────────────────────────────────────
Packer.toBuffer(buildDoc(data)).then(buf => {
  fs.mkdirSync(path.dirname(path.resolve(outputFile)), { recursive: true });
  fs.writeFileSync(outputFile, buf);
  console.log('done:', outputFile);
});
