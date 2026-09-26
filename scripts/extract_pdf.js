const { PDFParse } = require("pdf-parse");
const fs = require("fs");

(async () => {
  const buf = fs.readFileSync("D:\\Office_Working\\website\\public\\Catalogue\\TUBE VARNISH COATING SYSTEM.pdf");
  const data = new Uint8Array(buf);
  const parser = new PDFParse(data);
  const result = await parser.getText();
  console.log("=== PAGES:", result.numpages, "===");
  console.log(result.text);
  console.log("=== INFO ===");
  console.log(JSON.stringify(result.info, null, 2));
  await parser.destroy();
})();