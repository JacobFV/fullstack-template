import re
import os


def extract_files_from_markdown(md_content):
    # Regex to find code blocks and paths
    code_block_pattern = re.compile(r"```(.*?)\n(.*?)```", re.DOTALL)
    path_pattern = re.compile(r"`(.*?)`")

    # Find all code blocks
    blocks = code_block_pattern.findall(md_content)

    for block in blocks:
        language, code = block
        # Find the path from the language line if it contains a path
        path_match = path_pattern.search(language)
        if path_match:
            file_path = "frontend/" + path_match.group(1)
            # Create directories if they do not exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # Write code to the file
            with open(file_path, "w") as file:
                file.write(code.strip())


def main():
    # Read the markdown content from a file
    with open("./docs/automation/17-gpt4o-0511-blocks.md", "r") as file:
        md_content = file.read()

    # Extract files from the markdown content
    extract_files_from_markdown(md_content)


if __name__ == "__main__":
    main()
