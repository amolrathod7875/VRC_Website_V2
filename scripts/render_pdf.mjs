import fs from "fs";
import { createCanvas, Canvas, Image } from "canvas";

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
console.log("numPages:", doc.numPages);
for (let p = 1; p <= doc.numPages; p++) {
  const page = await doc.getPage(p);
  const viewport = page.getViewport({ scale: 2 });
  const canvas = createCanvas(viewport.width, viewport.height);
  const ctx = canvas.getContext("2d");
  const origDraw = ctx.drawImage.bind(ctx);
  ctx.drawImage = function (img, ...rest) {
    if (rest.length >= 4 && img && img.constructor && img.constructor.name === "CanvasElement") {
      const url = img.toDataURL();
      const real = new Image();
      real.src = url;
      return origDraw(real, ...rest);
    }
    return origDraw(img, ...rest);
  };
  await page.render({ canvasContext: ctx, viewport, canvas }).promise;
  const out = `C:\\Users\\shiva\\AppData\\Local\\Temp\\kilo\\tubepage${p}.png`;
  fs.writeFileSync(out, canvas.toBuffer("image/png"));
  console.log(`page ${p} -> ${out} (${viewport.width}x${viewport.height})`);
}