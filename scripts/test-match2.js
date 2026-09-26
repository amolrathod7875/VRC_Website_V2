function normalize(str) {
    return str.toLowerCase().replace(/&/g, ' and ').replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').trim();
}
function stripCorpWords(str) {
    const result = str.replace(/\b(ltd|pvt|co|limited|private|corporation|corp)\b/g, '').replace(/\s+/g, ' ').trim();
    return result;
}

const testStr = "mm barels";
const na = normalize("MM Barrel");
const nb = normalize("MM BARELS");
const naClean = stripCorpWords(na);
const nbClean = stripCorpWords(nb);

console.log('na:', JSON.stringify(na), 'len:', na.length);
console.log('nb:', JSON.stringify(nb), 'len:', nb.length);
console.log('naClean:', JSON.stringify(naClean), 'len:', naClean.length);
console.log('nbClean:', JSON.stringify(nbClean), 'len:', nbClean.length);
console.log('nbClean chars:', JSON.stringify(Array.from(nbClean).map(c => c + '=' + c.charCodeAt(0))));

// Test the regex replace directly
console.log('\nDirect replace test:');
console.log('naClean.replace(/s$/, ""):', JSON.stringify(naClean.replace(/s$/, '')), 'len:', naClean.replace(/s$/, '').length);
console.log('nbClean.replace(/s$/, ""):', JSON.stringify(nbClean.replace(/s$/, '')), 'len:', nbClean.replace(/s$/, '').length);

// Check if stripCorpWords changed nb
console.log('\nstripCorpWords("mm barels"):', JSON.stringify(stripCorpWords("mm barels")));
console.log('stripCorpWords("mm barrel"):', JSON.stringify(stripCorpWords("mm barrel")));
