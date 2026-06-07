from openai import OpenAI
from utils.prompts import PRODUCT_ANALYSIS_PROMPT
import json

client = OpenAI()


def analyze_images(
    image_base64_list,
    manual_info
):

    content = [
        {
            "type": "text",
            "text":
            PRODUCT_ANALYSIS_PROMPT
            + "\n\n補足情報:\n"
            + manual_info
        }
    ]

    for image_base64 in image_base64_list:

        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url":
                    f"data:image/jpeg;base64,{image_base64}"
                }
            }
        )

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        result = (
            response
            .choices[0]
            .message
            .content
        )

        result = result.replace(
            "```json",
            ""
        )

        result = result.replace(
            "```",
            ""
        )

        result = result.strip()

        return json.loads(result)

    except Exception as e:

        return {
            "error": str(e)
        }
