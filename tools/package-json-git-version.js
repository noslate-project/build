#!/usr/bin/env node
'use strict';

const fs = require('fs').promises;
const path = require('path');
const childProcess = require('child_process');

const help = `package-json-git-version [options] <target-dir> <output>

  --prefix <prefix>          version prefix, e.g. nightly
`;

/**
 *
 * @param {string[]} args
 */
async function main(args) {
  const varag = [];
  const options = {};
  while (args.length > 0) {
    switch (args[0]) {
      case '--help': {
        console.log(help);
        return process.exit(0);
      }
      case '--prefix': {
        options.prefix = args[1];
        args.shift();
        break;
      }
      default: {
        varag.push(args[0]);
      }
    }
    args.shift();
  }
  await tagPackageJson(varag[0], varag[1], options);
}

async function tagPackageJson(targetDir, outputPath, options) {
  targetDir = path.resolve(process.cwd(), path.normalize(targetDir));
  outputPath = path.resolve(process.cwd(), path.normalize(outputPath));
  const prefix = (options?.prefix ?? 'nightly') + '.';
  const revision = await gitHead(targetDir);

  const targetPackageJsonContent = await fs.readFile(path.join(targetDir, 'package.json'), 'utf8');
  const targetPackageJson = JSON.parse(targetPackageJsonContent);
  targetPackageJson.version = `${targetPackageJson.version}-${prefix}${revision.substring(0, 6)}`;
  await fs.writeFile(outputPath, JSON.stringify(targetPackageJson, null, 2), 'utf8');
}

async function gitHead(dir) {
  return new Promise((resolve, reject) => {
    childProcess.exec('git rev-parse --short=6 HEAD', {
      cwd: dir,
    }, (error, stdout, stderr) => {
      if (error) {
        error.stdout = stdout;
        error.stderr = stderr;
        return reject(error);
      }
      resolve(stdout.trim());
    });
  });
}

if (require.main === module) {
  main(process.argv.slice(2))
    .catch(e => {
      console.error(e);
      process.exit(1);
    });
}
