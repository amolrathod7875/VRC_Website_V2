const fs = require("fs");
const path = require("path");

const catalogueDir = "public/Catalogue";
const outputDir = "extracted_catalogue_text";
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

const files = fs.readdirSync(catalogueDir).filter(f => f.endsWith(".pdf"));

for (const file of files) {
  const filePath = path.join(catalogueDir, file);
  const data = fs.readFileSync(filePath);
  const str = data.toString("latin1");

  // Extract text from photoshop LayerName tags
  const layerRegex = /photoshop:LayerName>([^<]+)<\/photoshop:LayerName>/g;
  const layers = [];
  let match;
  while ((match = layerRegex.exec(str)) !== null) {
    layers.push(match[1]);
  }

  // Also extract text from other patterns - look for text in PDF content streams
  // Look for text between > and < that looks like actual content
  const textRegex = />([^<>]{15,})<\/[^>]+>/g;
  const texts = [];
  while ((match = textRegex.exec(str)) !== null) {
    const text = match[1].trim();
    if (text.length > 15 && !text.includes("http") && !text.includes("xml") && !text.includes("xmp") && !text.includes("Adobe") && !text.includes("photoshop") && !text.includes("vnd.adobe") && !text.includes("docid")) {
      texts.push(text);
    }
  }

  // Also look for text in the PDF that has application/use keywords
  const appKeywords = ['Application', 'Use', 'Suitable', 'Recommended', 'Industry', 'Process', 'Description', 'Used for', 'Ideal for', 'Designed for', 'Purpose', 'Purpose-built'];
  const relevantTexts = texts.filter(t => {
    const lower = t.toLowerCase();
    return appKeywords.some(k => lower.includes(k.toLowerCase()));
  });

  const output = {
    file,
    layerNames: [...new Set(layers)],
    allTextFragments: [...new Set(texts)].slice(0, 200),
    relevantTexts: [...new Set(relevantTexts)],
  };

  const outPath = path.join(outputDir, file.replace(/\.pdf$/, "") + ".json");
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2));
  console.log(`Extracted: ${file} -> ${outPath}`);
}

console.log("\nDone! All extracted text saved to", outputDir);
