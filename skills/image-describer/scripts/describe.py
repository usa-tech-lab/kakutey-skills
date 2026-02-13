import argparse
import os
import sys
import mimetypes
from google import genai
from google.genai import types

def describe_content(prompt, file_path, model_name="gemini-3-flash-preview"):
    # プロジェクトIDとロケーションの設定
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    
    # google-genai Client の初期化 (Vertex AI モード)
    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=10,
                initial_delay=10.0,
                max_delay=100.0,
                http_status_codes=[429]
            )
        )
    )

    # MIMEタイプの判定
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        if file_path.lower().endswith(".pdf"):
            mime_type = "application/pdf"
        else:
            mime_type = "image/png"

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Gemini 3 flash (Preview) へのリクエスト
    # thinking_level はデフォルトで試行
    response = client.models.generate_content(
        model=model_name,
        contents=[
            prompt,
            types.Part.from_bytes(data=file_data, mime_type=mime_type)
        ]
    )

    if response.text:
        print(response.text.strip())
    else:
        # テキストが直接取得できない場合の処理
        print("No text response received.", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze an image or PDF using Google Gen AI SDK (Vertex AI).")
    parser.add_argument("--prompt", required=True, help="Prompt for the model")
    parser.add_argument("--image", required=True, help="Path to the image or PDF file")
    parser.add_argument("--model", default="gemini-3-pro-preview", help="Model name")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"Error: File not found: {args.image}", file=sys.stderr)
        sys.exit(1)
        
    try:
        describe_content(args.prompt, args.image, args.model)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)