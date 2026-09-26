const fs = require("fs");
const path = require("path");

const catalogueDir = "public/Catalogue";
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

  // Also extract text from other patterns
  const textRegex = />([^<>]{10,})<\/[^>]+>/g;
  const texts = [];
  while ((match = textRegex.exec(str)) !== null) {
    const text = match[1].trim();
    if (text.length > 10 && !text.includes("http") && !text.includes("xml") && !text.includes("xmp")) {
      texts.push(text);
    }
  }

  console.log(`\n${"=".repeat(80)}`);
  console.log(`FILE: ${file}`);
  console.log(`${"=".repeat(80)}`);
  if (layers.length > 0) {
    console.log("LAYER NAMES:");
    layers.forEach(l => console.log("  -", l));
  }
  if (texts.length > 0) {
    console.log("\nTEXT FRAGMENTS:");
    texts.slice(0, 100).forEach(t => console.log("  -", t));
  }
  if (layers.length === 0 && texts.length === 0) {
    console.log("No extractable text found");
  }
}
