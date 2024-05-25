import json


def extract_and_save_text(json_file_path, output_file_path):
    # Load JSON data from file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Extract 'text' fields from each message
    texts = []
    for message in data["messages"]:
        for content in message["content"]:
            if "text" in content:
                texts.append(content["text"])

    # Concatenate all texts into a single string
    combined_text = "\n".join(texts)

    # Save the combined text to a new text file
    with open(output_file_path, "w") as file:
        file.write(combined_text)


# Example usage
extract_and_save_text(
    "14-gpt4o-0511-updated-code-blocks.json",
    "14-gpt4o-0511-updated-code-blocks.md",
)
