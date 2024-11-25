import json
import os
import random
import string

WORDS = [
    "and", "the", 
    "quick", "slow", "steady",
    "brown", "grey", "white",
    "grebe", "heron", "ibis",
    "jumps", "walks", "flies",
    "slowly", "quickly", "steadily",
    "over", "under", "between",
    "lazy", "calm", "collected",
    "dog", "frog", "bird"
]

CSS_PROPERTIES = [
    "background-color", "color", "font-size", "margin",
    "padding", "border", "width", "height", "display",
    "flex", "justify-content", "align-items", "border-radius",
    "box-shadow", "opacity", "transition", "transform",
    "position", "top", "left", "right", "bottom"
]

JSON_KEYS = [
    "name", "version", "description", "keywords", "author",
    "license", "dependencies", "scripts", "repository",
    "homepage", "bugs", "engines", "main", "types", "files"
]

MARKDOWN_HEADERS = ["# ", "## ", "### ", "#### ", "##### ", "###### "]

def generate_words(min_words=5, max_words=30):
    word_count = random.randint(min_words, max_words)
    return ' '.join(random.choices(WORDS, k=word_count))

def generate_css():
    num_rules = random.randint(1, 5)
    rules = []
    for _ in range(num_rules):
        selector = random.choice(['body', 'h1', 'p', '.class', '#id', 'div', 'span'])
        num_props = random.randint(2, 5)
        props = []
        for _ in range(num_props):
            prop = random.choice(CSS_PROPERTIES)
            value = generate_words(1, 3).replace(' ', '-')
            props.append(f"{prop}: {value};")
        rule = f"{selector} {{ {' '.join(props)} }}"
        rules.append(rule)
    return '\n'.join(rules)

def generate_json():
    num_keys = random.randint(3, 7)
    data = {}
    for _ in range(num_keys):
        key = random.choice(JSON_KEYS)
        if key == "id":
            data[key] = random.randint(1, 1000)
        elif key == "version":
            data[key] = round(random.uniform(0.1, 5.0), 2)
        elif key in ["dependencies", "scripts"]:
            data[key] = {f"package_{i}": f"^{random.randint(1,10)}.{random.randint(0,20)}.{random.randint(0,20)}" for i in range(random.randint(2,5))}
        else:
            data[key] = generate_words(3, 10)
    return json.dumps(data, indent=2)

def generate_markdown():
    num_sections = random.randint(1, 4)
    content = []
    for _ in range(num_sections):
        header = random.choice(MARKDOWN_HEADERS)
        header_text = generate_words(3, 7).capitalize()
        content.append(f"{header}{header_text}\n")
        paragraph = generate_words(20, 50)
        content.append(f"{paragraph}\n")
    return '\n'.join(content)

def generate_text():
    return generate_words(5, 30)

def create_file(file_path, file_type):
    content = ""
    
    if file_type == "txt":
        content = generate_text()
    elif file_type == "md":
        content = generate_markdown()
    elif file_type == "json":
        content = generate_json()
    elif file_type == "css":
        content = generate_css()
    elif file_type == "py":
        content = f"print('{generate_words(3, 7)}')"
    elif file_type == "html":
        content = f"<html><body><h1>{generate_words(2, 5).capitalize()}</h1><p>{generate_words(10, 20)}</p></body></html>"
    elif file_type == "js":
        content = f"console.log('{generate_words(3, 7)}');"
    else:
        content = generate_words(5, 30)
    
    with open(file_path, "w") as f:
        f.write(content)

def create_sample_files(directory="./data", file_types=("txt", "md", "json", "css", "py", "html", "js"), num_files=5):
    os.makedirs(directory, exist_ok=True)

    for i in range(1, num_files + 1):
        for file_type in file_types:
            file_name = f"sample_{i}.{file_type}"
            file_path = os.path.join(directory, file_name)
            create_file(file_path, file_type)
            print(f"Created: {file_path}")

if __name__ == '__main__':
    # use: directory, file_types, num_files
    create_sample_files(directory="./data", file_types=("txt", "md", "json", "css", "py", "html", "js"), num_files=10)
