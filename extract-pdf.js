const { PDFParse } = require('pdf-parse');
const fs = require('fs');
const parser = new PDFParse();
parser(fs.readFileSync('D:/Office_Working/website/public/Catalogue/regulator.pdf')).then(d => console.log(d.text))