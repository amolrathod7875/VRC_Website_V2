import { createCanvas } from "canvas";

const a = createCanvas(10, 10);
const b = createCanvas(20, 20);
const ctx = b.getContext("2d");
try {
  ctx.drawImage(a, 0, 0, 10, 10, 0, 0, 20, 20);
  console.log("drawImage Canvas OK");
} catch (e) {
  console.log("drawImage Canvas FAIL:", e.message);
}