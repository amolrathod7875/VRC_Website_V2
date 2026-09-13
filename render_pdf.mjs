import fs from "fs";
import { createCanvas, Canvas } from "canvas";

class OffscreenCanvasPolyfill extends Canvas {
  constructor(width, height) {
    super(width, height);
    this.width = width;
    this.height = height;
  }
  getContext(type) {
    if (type === "2d") return super.getContext(type);
    return null;
  }
  transferToImageBitmap() { return this; }
  convertToBlob() { return Promise.resolve(new Blob([this.toBuffer("image/png")], { type: "image/png" })); }
  toDataURL() { return this.toDataURL("image/png"); }
  toBlob() { return Promise.resolve(this.toBuffer("image/png")); }
}
globalThis.OffscreenCanvas = OffscreenCanvasPolyfill;

function makeCanvasFactory() {
  return {
    create(width, height) {
      const canvas = createCanvas(width, height);
      return { canvas, context: canvas.getContext("2d") };
    },
    reset(entry, width, height) {
      const canvas = createCanvas(width, height);
      entry.canvas = canvas;
      entry.context = canvas.getContext("2d");
    },
    destroy() {},
  };
}

const data = new Uint8Array(fs.readFileSync("D:\\Office_Working\\website\\public\\Catalogue\\TUBE VARNISH COATING SYSTEM.pdf"));
const pdfjs = await import("pdfjs-dist/legacy/build/pdf.mjs");
const doc = await pdfjs.getDocument({
  data,
  disableFontFace: true,
  canvasFactory: makeCanvasFactory(),
}).promise;
const page = await doc.getPage(1);
const viewport = page.getViewport({ scale: 2 });
const canvas = createCanvas(viewport.width, viewport.height);
const ctx = canvas.getContext("2d");
const origDraw = ctx.drawImage.bind(ctx);
ctx.drawImage = function (img, ...rest) {
  if (rest.length >= 4 && img && img.constructor && img.constructor.name === "CanvasElement") {
    const inner = img.ctx && img.ctx.canvas;
    console.log("inner canvas:", inner && inner.constructor && inner.constructor.name, "isCanvas:", inner instanceof Canvas);
    if (inner instanceof Canvas) {
      return origDraw(inner, ...rest);
    }
  }
  return origDraw(img, ...rest);
};
try {
  await page.render({ canvasContext: ctx, viewport, canvas }).promise;
  const out = `C:\\Users\\shiva\\AppData\\Local\\Temp\\kilo\\tubepage1.png`;
  fs.writeFileSync(out, canvas.toBuffer("image/png"));
  console.log("RENDER OK ->", out);
} catch (e) {
  console.log("RENDER FAIL:", e.message);
}
await doc.destroy();