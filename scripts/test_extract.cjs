const { PDFParse } = require("pdf-parse");
const fs = require("fs");

const filePath = "public/Catalogue/rhino.pdf";
const buf = fs.readFileSync(filePath);
const data = new Uint8Array(buf);

(async () => {
  const parser = new PDFParse(data, { max: 10 });
  const result = await parser.getText();
  console.log("numPages:", result.numpages);
  console.log("text length:", result.text.length);
  console.log("text:", result.text);
  await parser.destroy();
})();
