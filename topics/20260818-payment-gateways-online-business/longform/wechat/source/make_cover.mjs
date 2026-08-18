import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "file:///C:/Users/zcs/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const logosDir = path.join(here, "logos");
const outPath = path.resolve(here, "..", "cover.jpg");

const stripeSvg = fs.readFileSync(path.join(logosDir, "stripe-wordmark-white.svg"));
const razorpaySvg = fs.readFileSync(path.join(logosDir, "razorpay-logo.svg"));
const stripeData = stripeSvg.toString("base64");
const razorpayData = razorpaySvg.toString("base64");

const svg = `
<svg width="900" height="383" viewBox="0 0 900 383" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#08101f"/>
      <stop offset="0.58" stop-color="#10172b"/>
      <stop offset="1" stop-color="#182043"/>
    </linearGradient>
    <linearGradient id="rail" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#635BFF" stop-opacity="0.22"/>
      <stop offset="0.55" stop-color="#635BFF" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#2F87FF" stop-opacity="0.55"/>
    </linearGradient>
    <linearGradient id="glow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#9A93FF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#9A93FF" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#2F87FF" stop-opacity="0"/>
    </linearGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000814" flood-opacity="0.45"/>
    </filter>
    <clipPath id="frame">
      <rect width="900" height="383" rx="0"/>
    </clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="900" height="383" fill="url(#bg)"/>
    <circle cx="715" cy="78" r="172" fill="#635BFF" opacity="0.18" filter="url(#blur)"/>
    <circle cx="812" cy="323" r="144" fill="#2F87FF" opacity="0.15" filter="url(#blur)"/>

    <g opacity="0.12" stroke="#C7D2FF" stroke-width="1">
      <path d="M0 64 H900"/>
      <path d="M0 128 H900"/>
      <path d="M0 192 H900"/>
      <path d="M0 256 H900"/>
      <path d="M0 320 H900"/>
      <path d="M90 0 V383"/>
      <path d="M180 0 V383"/>
      <path d="M270 0 V383"/>
      <path d="M360 0 V383"/>
      <path d="M450 0 V383"/>
      <path d="M540 0 V383"/>
      <path d="M630 0 V383"/>
      <path d="M720 0 V383"/>
      <path d="M810 0 V383"/>
    </g>

    <path d="M485 -38 C555 32 561 86 633 133 C706 181 731 250 920 326 L920 421 L626 421 C649 333 576 289 522 237 C459 177 429 99 410 8 Z" fill="url(#rail)"/>
    <path d="M462 1 C522 74 551 115 621 158 C697 206 743 264 904 320" fill="none" stroke="url(#glow)" stroke-width="4"/>
    <path d="M503 -5 C552 54 584 94 647 131 C718 173 768 218 890 260" fill="none" stroke="#A4A0FF" stroke-opacity="0.38" stroke-width="1.5" stroke-dasharray="6 10"/>

    <g font-family="Microsoft YaHei, PingFang SC, sans-serif">
      <text x="52" y="52" fill="#9CA9C3" font-size="18" font-weight="600" letter-spacing="1">沿着支付入口往回看</text>
      <text x="50" y="126" fill="#FFFFFF" font-size="47" font-weight="800">网上的人</text>
      <text x="50" y="184" fill="#FFFFFF" font-size="47" font-weight="800">究竟在卖什么</text>
      <rect x="52" y="229" width="228" height="38" rx="19" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.12"/>
      <text x="73" y="254" fill="#CBD4E9" font-size="17" font-weight="600">11 个入口 · 963 条来源</text>
    </g>

    <g filter="url(#shadow)">
      <rect x="440" y="63" width="258" height="112" rx="22" fill="#635BFF"/>
      <rect x="440.75" y="63.75" width="256.5" height="110.5" rx="21.25" fill="none" stroke="#B9B5FF" stroke-opacity="0.52" stroke-width="1.5"/>
      <image href="data:image/svg+xml;base64,${stripeData}" x="495" y="94" width="148" height="48" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <g filter="url(#shadow)">
      <rect x="635" y="226" width="220" height="88" rx="18" fill="#FFFFFF"/>
      <rect x="635.75" y="226.75" width="218.5" height="86.5" rx="17.25" fill="none" stroke="#C8D9FF" stroke-width="1.5"/>
      <image href="data:image/svg+xml;base64,${razorpayData}" x="670" y="249" width="150" height="42" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <g font-family="Microsoft YaHei, PingFang SC, sans-serif" font-size="14" font-weight="600">
      <g transform="translate(451 184)">
        <rect width="82" height="31" rx="15.5" fill="#111A2E" stroke="#8E88FF" stroke-opacity="0.58"/>
        <text x="41" y="21" text-anchor="middle" fill="#DAD8FF">AI 产品</text>
      </g>
      <g transform="translate(471 274)">
        <rect width="112" height="31" rx="15.5" fill="#111A2E" stroke="#62A4FF" stroke-opacity="0.58"/>
        <text x="56" y="21" text-anchor="middle" fill="#D7E8FF">专业软件</text>
      </g>
      <g transform="translate(523 334)">
        <rect width="76" height="31" rx="15.5" fill="#111A2E" stroke="#62A4FF" stroke-opacity="0.46"/>
        <text x="38" y="21" text-anchor="middle" fill="#D7E8FF">课程</text>
      </g>
      <g transform="translate(822 153)">
        <rect width="72" height="31" rx="15.5" fill="#111A2E" stroke="#8E88FF" stroke-opacity="0.46"/>
        <text x="36" y="21" text-anchor="middle" fill="#DAD8FF">SaaS</text>
      </g>
    </g>

    <g fill="#D6D9FF">
      <circle cx="535" cy="137" r="4"/>
      <circle cx="600" cy="196" r="4"/>
      <circle cx="700" cy="209" r="4"/>
      <circle cx="821" cy="329" r="4"/>
    </g>
  </g>
</svg>`;

await sharp(Buffer.from(svg))
  .flatten({ background: "#08101f" })
  .jpeg({ quality: 94, chromaSubsampling: "4:4:4" })
  .toFile(outPath);

const meta = await sharp(outPath).metadata();
if (meta.format !== "jpeg" || meta.width !== 900 || meta.height !== 383) {
  throw new Error(`Unexpected cover output ${meta.format} ${meta.width}x${meta.height}`);
}

process.stdout.write(JSON.stringify({ output: outPath, width: meta.width, height: meta.height, format: meta.format }));
