import os
import re

def remove_emojis(text):
    # This regex targets the Unicode ranges typically used for emojis
    emoji_pattern = re.compile(
        "["
        "\U00010000-\U0010ffff"  # Supplemental Planes (including most emojis)
        "\u2600-\u27BF"          # Miscellaneous Symbols and Dingbats
        "\u2300-\u23FF"          # Miscellaneous Technical
        "\u2B50-\u2B50"          # Star emoji
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    clean_content = remove_emojis(content)
    
    # Also clean up double spaces that might be left behind
    clean_content = clean_content.replace('  ', ' ')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    print(f"Cleaned: {file_path}")

if __name__ == "__main__":
    directory = "XRD"
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            clean_file(os.path.join(directory, filename))
