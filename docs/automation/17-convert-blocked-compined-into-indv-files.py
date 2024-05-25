import re
import os


import re
import os


def extract_files_from_markdown(md_content):
    # Regex to find code blocks and paths
    # code_block_pattern = re.compile(r"\d+\.\s+`(.*?)`\n```(.*?)\n(.*?)```", re.DOTALL)
    code_block_pattern = re.compile(r"`([^`]+)`\n\n```(\w+)\n([\s\S]+?)```")

    # Find all code blocks
    blocks = code_block_pattern.findall(md_content)

    for block in blocks:
        file_path, language, code = block
        print(file_path, language, code)
        # Create directories if they do not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Write code to the file
        with open(file_path, "w") as file:
            print(f"Writing to {file_path}")
            file.write(code.strip())


def main():
    # Read the markdown content from a file
    with open("docs/automation/17-gpt4o-0511-blocks.md", "r") as file:
        md_content = file.read()

    # Extract files from the markdown content
    extract_files_from_markdown(md_content)


if __name__ == "__main__":
    main()


def main():
    # Read the markdown content from a file
    with open("./docs/automation/17-gpt4o-0511-blocks.md", "r") as file:
        md_content = file.read()

    # Extract files from the markdown content
    extract_files_from_markdown(md_content)


if __name__ == "__main__":
    main()
