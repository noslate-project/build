'use strict';

const fs = require('fs');
const { JSDOM } = require('jsdom');
const arg = require('arg');

async function main(argv) {
  const args = arg({
    '--out': String,
    '-o': '--out',
  }, {
    argv,
    stopAtPositional: true,
  });
  const files = args._;

  const dom = new JSDOM();
  const { DOMParser, XMLSerializer } = dom.window;

  const parser = new DOMParser();
  const serializer = new XMLSerializer();

  for (const file of files) {
    const fileContent = fs.readFileSync(file, 'utf8');
    const doc = parser.parseFromString(fileContent, 'application/xml');
    const formatted = serializer.serializeToString(doc);
    fs.writeFileSync(file, formatted, 'utf8');
  }
}

main(process.argv.slice(2));
