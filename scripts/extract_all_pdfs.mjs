import fs from "fs";
import path from "path";
import pdfjs from "pdfjs-dist/legacy/build/pdf.mjs";

const catalogueDir = "public/Catalogue";
const files = fs.readdirSync(catalogueDir).filter(f => f.endsWith(".pdf"));

for (const file of files) {
  const filePath = path.join(catalogueDir, file);
  const data = new Uint8Array(fs.readFileSync(filePath));
  try {
    const doc = await pdfjs.getDocument({ data, disableFontFace: true }).promise;
    let fullText = "";
    for (let p = 1; p <= doc.numPages; p++) {
      const page = await doc.getPage(p);
      const content = await page.getTextContent();
      const items = content.items.map((it) => it.str);
      fullText += items.join("");
    }
    console.log(`\n${"=".repeat(80)}`);
    console.log(`FILE: ${file}`);
    console.log(`PAGES: ${doc.numPages}`);
    console.log(`${"=".repeat(80)}`);
    console.log(fullText);
    await doc.destroy();
  } catch (e) {
    console.log(`ERROR reading ${file}: ${e.message}`);
  }
}
