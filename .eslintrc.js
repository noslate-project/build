'use strict';

module.exports = {
  extends: 'eslint-config-egg',
  parser: '@babel/eslint-parser',
  parserOptions: {
    requireConfigFile: false,
    babelOptions: {
      plugins: [
        '@babel/plugin-proposal-class-properties',
        '@babel/plugin-proposal-private-methods',
      ],
    },
  },
  env: {
    es2021: true,
    serviceworker: true,
  },
  rules: {
    'no-bitwise': 'off',
    'no-constant-condition': 'off',
    'no-loop-func': 'off',
    'no-unused-vars': [ 'error', { vars: 'all', args: 'after-used' }],
  },
};
