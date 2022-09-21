'use strict';

const fs = require('fs');
const path = require('path');
const assert = require('assert');
const { JSDOM } = require('jsdom');
const arg = require('arg');
const git = require('isomorphic-git');

async function main(argv) {
  const args = arg({
    '--out': String,
    '-o': '--out',
  }, {
    argv,
    stopAtPositional: true,
  });
  const [ manifestPath, version ] = args._;

  const repoRoot = path.resolve(__dirname, '../..');

  const dom = new JSDOM();
  const { DOMParser, XMLSerializer } = dom.window;

  const parser = new DOMParser();
  const serializer = new XMLSerializer();
  const manifestString = fs.readFileSync(manifestPath, 'utf8');
  const manifestDoc = parser.parseFromString(manifestString, 'application/xml');

  const defaultNode = manifestDoc.querySelector('manifest default');
  defaultNode.setAttribute('revision', version);
  const defaultBranch = defaultNode.getAttribute('branch') ?? 'master';

  {
    const projectNodes = manifestDoc.querySelectorAll('manifest project');
    for (const projectNode of projectNodes) {
      const revision = projectNode.getAttribute('revision');
      const groups = (projectNode.getAttribute('groups') ?? '').split(',');
      if (groups.includes('base')) {
        continue;
      }
      if (revision && revision.match(/^refs\/tags\//)) {
        continue;
      }
      const projectPath = projectNode.getAttribute('path') ?? projectNode.getAttribute('name');
      assert(projectPath != null);
      const commit = await git.resolveRef({ fs, dir: path.resolve(repoRoot, projectPath), ref: 'HEAD' });
      projectNode.setAttribute('dest-branch', revision ?? defaultBranch);
      projectNode.setAttribute('revision', commit);
    }
  }

  const output = serializer.serializeToString(manifestDoc);
  if (args['--out']) {
    fs.writeFileSync(args['--out'], output + '\n', 'utf8');
  } else {
    console.log(output);
  }
}

main(process.argv.slice(2));
