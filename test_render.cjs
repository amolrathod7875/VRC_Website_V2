const fs = require("fs");
const path = require("path");
const pdfjs = require("pdfjs-dist");
const { createCanvas } = require("canvas");

const catalogueDir = "public/Catalogue";
const files = ["rhino.pdf"];

(async () => {
  for (const file of files) {
    const filePath = path.join(catalogueDir, file);
    const data = new Uint8Array(fs.readFileSync(filePath));
    try {
      const doc = await pdfjs.getDocument({ data, disableFontFace: true }).promise;
      console.log("numPages:", doc.numPages);
      const page = await doc.getPage(1);
      const viewport = page.getViewport({ scale: 2 });
      const canvas = createCanvas(viewport.width, viewport.height);
      const ctx = canvas.getContext("2d");
      await page.render({ canvasContext: ctx, viewport, canvas }).promise;
      const out = `temp_pdf_images/test_${file.replace(/\.pdf$/, "")}_page1.png`;
      fs.writeFileSync(out, canvas.toBuffer("image/png"));
      console.log(`Rendered to ${out}`);
      doc.destroy();
    } catch (e) {
      console.log(`ERROR: ${e.message}`);
      console.log(e.stack);
    }
  }
})();
