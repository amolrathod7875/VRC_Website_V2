import { createCanvas, Canvas } from "canvas";

class Sub extends Canvas {
  constructor(w, h) { super(w, h); this.width = w; this.height = h; }
  getContext(t) { return super.getContext(t); }
}

const a = new Sub(10, 10);
const b = createCanvas(20, 20);
const ctx = b.getContext("2d");
console.log("a instanceof Canvas:", a instanceof Canvas);
console.log("a instanceof OffscreenCanvas:", typeof OffscreenCanvas !== "undefined" && a instanceof OffscreenCanvas);
try {
  ctx.drawImage(a, 0, 0, 10, 10, 0, 0, 20, 20);
  console.log("drawImage Sub OK");
} catch (e) {
  console.log("FAIL:", e.message);
}