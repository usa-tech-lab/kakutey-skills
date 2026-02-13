---
name: image-describer
description: Describe or analyze image content using Gemini 3 Flash. Use this skill when you need to understand what is in an image or pdf file (e.g., icons, screenshots, diagrams) to proceed with a task.
---
# Image Describer

This skill allows you to analyze image files by providing a prompt and the file path. It uses the `gemini-3-flash-preview` model for fast and accurate vision analysis.

## Workflow for Agents

When you encounter an image file and need to understand its content:

1. Identify the absolute path of the image file.
2. Decide what information you need from the image (e.g., general description, text extraction, UI component identification).
3. Execute the `describe.py` script.

### Example Usage

```bash
python3 scripts/describe.py --prompt "Extract all text from this image." --image "screenshot.png"
```

### Specific Use Cases

- **OCR**: `python3 scripts/describe.py --prompt "Extract all text from this image." --image "screenshot.png"`
- **UI Analysis**: `python3 scripts/describe.py --prompt "Identify the main UI components and their layout." --image "mockup.jpg"`
- **Icon Identification**: `python3 scripts/describe.py --prompt "What does this icon represent?" --image "icon.svg"`

## Resource Details

- `scripts/describe.py`: Vertex AI SDK (google-genai) を使用して、画像や PDF を解析する Python スクリプト。
