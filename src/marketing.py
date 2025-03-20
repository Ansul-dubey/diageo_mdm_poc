import sys, os

current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir))
sys.path.append(parent_dir)
import json
import re
import pandas as pd
from src.config import *
from src.utility import *
import os
import base64
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv(
    "AZURE_OPENAI_API_KEY", ""
)  # Initialize Azure OpenAI Service client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)  # IMAGE_PATH = "YOUR_IMAGE_PATH" # encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii') #Prepare the chat prompt

input_file = INPUT_PATH_FILE_MARKETING  # Update with your actual input file path
output_file = "marketing_processed.csv"

df = read_data(input_file)

input_column = "PUConsumerRetailItemName"

chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "give me information about space",
            }
        ],
    }
]  # Include speech result if speech is enabled
messages = chat_prompt  # Generate the completion
# completion = client.chat.completions.create(model=deployment, messages=messages, max_tokens=800, temperature=0.7, top_p=0.95, frequency_penalty=0, presence_penalty=0, stop=None, stream=False)  # type: ignore

# print(completion.to_json())


def generate_liquor_details(description):
    if description.strip().lower() == "unknown":
        return "Unknown", 0, "Unknown", 0, "Unknown", 0
    prompt = f"""
    You are an expert in alcoholic beverages and product categorization. Your task is to analyze the given Beverage Description and extract structured details, filling in unknown values based on historical data or the best possible estimate, along with a confidence score for each value.

    ### Instructions:
    - Read the given Beverage Description.
    - Identify its quantity (e.g., "0.750L", "0.350L", "0.50L", "1.00L", "0.180L", "4.0L", "0.558L").
    - Identify its pack_count (e.g., "1 Pack", "4 Pack", "6 Pack", "7 Pack", "120 Pack").
    - Identify its packaging_type (e.g., "Glass Bottle", "Can", "Bottle PET", "Sachet", "KEG").
    - Identify its info (e.g., "Smirnoff Seltzer Natural Orange (RTD)", "Linkwood 15YO Item", "Flavored Vodka", "Ready-To-Drink (RTD)").
    - If a value is unknown, populate it using historical data or the most probable estimate and provide a confidence score between 0 and 1.
    - Packaging Type Classification Logic:
        -If the packaging type is already known and not "Unknown," retain its value.
        -Otherwise, classify it as follows (ignoring case sensitivity):
        -If it contains "can" (case-insensitive), categorize it as "ALUMINIUM CAN".
        -If it contains "glass bottle", categorize it as "STANDARD".
        -If it contains "bottle":
        -If it also contains "pet" or "plastic", categorize it as "LIGHTWEIGHT".
        -Otherwise, categorize it as "STANDARD".
        -If it contains "keg", categorize it as "KEG".
        -If it contains "cardboard box", categorize it as "CARDBOARD BOX".
        -This ensures a standardized classification of packaging types while handling case-insensitive variations.
        - and after these steps combine the pack count and packagin type like 6X01 STANDARD and show it's confidence socre as average of  pack_count and Packagin_type
    -Respond only in JSON format.

    ### Example Inputs & Outputs:

    #### Input 1:
    Beverage Description: "Smirnoff Seltzer Natural Orange (RTD) 0.250L Can 4 Pack"

    **Expected Output (JSON):**
    ```json
    {{
    "quantity": "0.25L",
    "quantity_confidence": 1.0,
    "pack_count_packaging": "4X01 ALUMINIUM CAN",
    "pack_count_packaging_confidence": 1.0,
    "info": "Smirnoff Seltzer Natural Orange (RTD)",
    "info_confidence": 1.0
    }}
    ```

    #### Input 2:
    Beverage Description: "Linkwood 15YO Item Bottle 1 Pack"

    **Expected Output (JSON):**
    ```json
    {{
    "quantity": "0.7L",
    "quantity_confidence": 0.9,
    "pack_count_packaging": "1X01 STANDARD",
    "pack_count_packaging_confidence": 1.0,
    "info": "Linkwood 15YO Item",
    "info_confidence": 1.0
    }}
    ```

    #### Input 3:
    Beverage Description: "Smirnoff Peach Lemonade 0.05L Bottle 10 Pack 30.00% PET"

    **Expected Output (JSON):**
    ```json
    {{
    "quantity": "0.05L",
    "quantity_confidence": 1.0,
    "pack_count_packaging": "10X01 LIGHTWEIGHT",
    "pack_count_packaging_confidence": 1.0,
    "info": "Smirnoff Peach Lemonade",
    "info_confidence": 1.0
    }}
    ```

    #### Input 4:
    Beverage Description: "Tanqueray No. Ten Gin 0.700L Unknown"

    **Expected Output (JSON):**
    ```json
    {{
    "quantity": "0.7L",
    "quantity_confidence": 1.0,
    "pack_count_packaging": "1X01 STANDARD",
    "pack_count_packaging_confidence": 0.5,
    "info": "Tanqueray No. Ten Gin",
    "info_confidence": 1.0
    }}
    ```

    #### Input 5:
    Beverage Description: "Bulleit Bourbon 10YO 0.700L Bottle 1 Pack 45.60%"

    **Expected Output (JSON):**
    ```json
    {{
    "quantity": "0.7L",
    "quantity_confidence": 1.0,
    "pack_count_packaging": "1X01 STANDARD",
    "pack_count_packaging_confidence": 1.0,
    "info": "Bulleit Bourbon 10YO",
    "info_confidence": 1.0
    }}
    ```

    **Input 5:**
    Beverage Description: **"{description}"**
    """

    try:

        response = client.chat.completions.create(
            model=deployment,  # type: ignore
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )

        result = json.loads(
            re.sub(
                r"```json\n|\n```",
                "",
                dict(json.loads(response.to_json()))["choices"][0]["message"][
                    "content"
                ],
            )
        )
        print(result)

        quantity = result.get("quantity", "Unknown")
        quantity_c_score = result.get("quantity_confidence", "Unknown")
        pack_count_packaging = result.get("pack_count_packaging", "Unknown")
        pack_count_packaging_confidence = result.get(
            "pack_count_packaging_confidence", "Unknown"
        )
        des = result.get("info", "Unknown")
        des_c_score = result.get("info_confidence", "Unknown")

        return (
            des,
            des_c_score,
            quantity,
            quantity_c_score,
            pack_count_packaging,
            pack_count_packaging_confidence,
        )

    except Exception as e:
        print(f"Error processing: {description} - {str(e)}")
        return "Unknown", "Unknown", "Unknown", "Unknown"


# Apply function to each row in the CSV
(
    df["IBV_SAPPHL5Description_D"],
    df["IBV_SAPPHL5Description_D_c_score"],
    df["Item_SAPPHL6Description"],
    df["Item_SAPPHL6Description_c_score"],
    df["SKU_SAPPHL7Description"],
    df["SKU_SAPPHL7Description_c_score"],
) = zip(*df[input_column].apply(generate_liquor_details))
output_file = "marketing_processed_gpt_7.csv"
df.to_csv(f"{parent_dir}/data/output/{output_file}", index=False)
