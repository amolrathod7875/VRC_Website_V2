const { PDFParse } = require("pdf-parse");
const fs = require("fs");
const path = require("path");

const catalogueDir = "public/Catalogue";
const files = fs.readdirSync(catalogueDir).filter(f => f.endsWith(".pdf"));

(async () => {
  for (const file of files) {
    const filePath = path.join(catalogueDir, file);
    const buf = fs.readFileSync(filePath);
    try {
      const data = new Uint8Array(buf);
      const parser = new PDFParse(data);
      const result = await parser.getText();
      console.log(`\n${"=".repeat(80)}`);
      console.log(`FILE: ${file}`);
      console.log(`PAGES: ${result.numpages}`);
      console.log(`${"=".repeat(80)}`);
      console.log(result.text);
      await parser.destroy();
    } catch (e) {
      console.log(`ERROR reading ${file}: ${e.message}`);
    }
  }
})();
