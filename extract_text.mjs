import fs from "fs";

const pdfjs = await import("pdfjs-dist/legacy/build/pdf.mjs");

const data = new Uint8Array(fs.readFileSync("D:\\Office_Working\\website\\public\\Catalogue\\TUBE VARNISH COATING SYSTEM.pdf"));
const doc = await pdfjs.getDocument({ data, disableFontFace: true }).promise;
console.log("numPages:", doc.numPages);
for (let p = 1; p <= doc.numPages; p++) {
  const page = await doc.getPage(p);
  const content = await page.getTextContent();
  const items = content.items.map((it) => it.str);
  const text = items.join("");
  console.log(`\n===== PAGE ${p} =====`);
  console.log(text);
}
await doc.destroy();