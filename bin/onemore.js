#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const scriptDir = path.join(__dirname, '..', 'scripts');
const searchPy = path.join(scriptDir, 'search.py');

if (!fs.existsSync(searchPy)) {
  console.error('Error: search.py not found at', searchPy);
  process.exit(1);
}

try {
  const result = execSync(`python3 "${searchPy}" ${args.join(' ')}`, {
    stdio: 'inherit',
    cwd: path.join(__dirname, '..'),
  });
} catch (e) {
  process.exit(e.status || 1);
}
