#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');

function main() {
  const args = process.argv.slice(2);
  let prompt = '';
  let imagePath = '';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' && args[i + 1]) {
      prompt = args[i + 1];
      i++;
    } else if (args[i] === '--image' && args[i + 1]) {
      imagePath = args[i + 1];
      i++;
    }
  }

  if (!prompt || !imagePath) {
    console.error('Usage: node describe.cjs --prompt "{instruction}" --image "{image_path}"');
    process.exit(1);
  }

  const absoluteImagePath = path.resolve(process.cwd(), imagePath);
  
  // Construct the gemini command
  // Note: Escaping prompt for shell execution
  const escapedPrompt = prompt.replace(/"/g, '\\"');
  const command = `gemini "${escapedPrompt} @${absoluteImagePath}" --model gemini-3-flash-preview`;

  try {
    const stdout = execSync(command, { encoding: 'utf8' });
    console.log(stdout);
  } catch (error) {
    console.error('Error executing gemini command:', error.message);
    if (error.stdout) console.error('Stdout:', error.stdout);
    if (error.stderr) console.error('Stderr:', error.stderr);
    process.exit(1);
  }
}

main();
