from pathlib import Path
import random

import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
from openai import OpenAI
import inflect


REPO_ROOT_DIR = Path(__file__).parent.parent
APP_DIR = REPO_ROOT_DIR / "app"
ENGINE = inflect.engine()


load_dotenv()
client = OpenAI()


def horoscope(birthday):
    prompt = generate_prompt(birthday)
    model = load_config_file()["model"]
    print(prompt)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message
    return content


def generate_prompt(birthday):
    config = load_config_file()
    prompt = random.choice(config["prompts"])
    prompt = prompt.replace("BIRTHDAY", birthday)
    return prompt


def load_config_file():
    filepath = APP_DIR / "config.yaml"
    config = load_yaml_file(filepath)
    return config


def load_yaml_file(filepath):
    with open(filepath) as file:
        obj = yaml.load(file, Loader=SafeLoader)
    return obj






# completion = client.chat.completions.create(
#   model=config["model"],
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)