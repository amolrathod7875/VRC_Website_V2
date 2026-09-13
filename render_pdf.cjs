class DOMMatrix {
  constructor(transform = []) {
    if (typeof transform === "string") {
      const m = transform.match(/matrix\(([^)]+)\)/);
      if (m) {
        const v = m[1].split(/,\s*/).map(Number);
        [this.a, this.b, this.c, this.d, this.e, this.f] = v;
      } else {
        [this.a, this.b, this.c, this.d, this.e, this.f] = [1, 0, 0, 1, 0, 0];
      }
    } else if (Array.isArray(transform)) {
      [this.a, this.b, this.c, this.d, this.e, this.f] = transform;
    } else {
      [this.a, this.b, this.c, this.d, this.e, this.f] = [1, 0, 0, 1, 0, 0];
    }
  }
  multiply(other) {
    const { a: a1, b: b1, c: c1, d: d1, e: e1, f: f1 } = this;
    const { a: a2, b: b2, c: c2, d: d2, e: e2, f: f2 } = other;
    return new DOMMatrix([
      a1 * a2 + c1 * b2, a1 * b2 + c1 * d2,
      b1 * a2 + d1 * c2, b1 * b2 + d1 * d2,
      e1 * a2 + c1 * e2 + f1 * a2, e1 * b2 + d1 * e2 + f1 * b2,
    ]);
  }
  translate(x = 0, y = 0) {
    return new DOMMatrix([this.a, this.b, this.c, this.d, this.e + x, this.f + y]);
  }
  scale(s) {
    return new DOMMatrix([this.a * s, this.b * s, this.c * s, this.d * s, this.e, this.f]);
  }
  inverse() {
    const det = this.a * this.d - this.b * this.c;
    if (!det) return new DOMMatrix();
    const inv = 1 / det;
    return new DOMMatrix([
      this.d * inv, -this.b * inv, -this.c * inv, this.a * inv,
      (this.c * this.f - this.d * this.e) * inv,
      (this.b * this.e - this.a * this.f) * inv,
    ]);
  }
  transformPoint(p) {
    return { x: this.a * p.x + this.c * p.y + this.e, y: this.b * p.x + this.d * p.y + this.f };
  }
  static fromMatrix(m) { return new DOMMatrix([m.a, m.b, m.c, m.d, m.e, m.f]); }
}
globalThis.DOMMatrix = DOMMatrix;
globalThis.DOMPoint = class DOMPoint {
  constructor(x = 0, y = 0, z = 0, w = 1) { this.x = x; this.y = y; this.z = z; this.w = w; }
};

const fs = require("fs");
const pdfjs = require("pdfjs-dist/legacy/build/pdf.mjs");
const { createCanvas } = require("canvas");

(async () => {
  const data = new Uint8Array(fs.readFileSync("D:\\Office_Working\\website\\public\\Catalogue\\TUBE VARNISH COATING SYSTEM.pdf"));
  const doc = await pdfjs.getDocument({ data, disableFontFace: true }).promise;
  console.log("numPages:", doc.numPages);
  for (let p = 1; p <= doc.numPages; p++) {
    const page = await doc.getPage(p);
    const viewport = page.getViewport({ scale: 2 });
    const canvas = createCanvas(viewport.width, viewport.height);
    const ctx = canvas.getContext("2d");
    await page.render({ canvasContext: ctx, viewport, canvas }).promise;
    const out = `C:\\Users\\shiva\\AppData\\Local\\Temp\\kilo\\tubepage${p}.png`;
    fs.writeFileSync(out, canvas.toBuffer("image/png"));
    console.log(`page ${p} -> ${out} (${viewport.width}x${viewport.height})`);
  }
  await doc.destroy();
})();