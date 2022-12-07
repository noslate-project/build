#!/usr/bin/env node
'use strict';

const fs = require('fs').promises;
const path = require('path');

const help = `package-json-version [options] <target-dir>`;

/**
 *
 * @param {string[]} args
 */
async function main(args) {
  const varag = [];
  while (args.length > 0) {
    switch (args[0]) {
      case '--help': {
        console.log(help);
        return process.exit(0);
      }
      default: {
        varag.push(args[0]);
      }
    }
    args.shift();
  }


  const content = await fs.readFile(path.join(varag[0], 'package.json'), 'utf-8');
  const pkgJson = JSON.parse(content);
  console.log(pkgJson.version);
}

if (require.main === module) {
  main(process.argv.slice(2))
    .catch(e => {
      console.error(e);
      process.exit(1);
    });
}
