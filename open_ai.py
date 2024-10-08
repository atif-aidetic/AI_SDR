import openai
import json
import yaml
import os
from settings import ENV

env = ENV()

# Set OpenAI API key
openai_api_key = env.openai_api_key
openai.api_key = openai_api_key

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the mail.yaml file inside the 'config' folder
yaml_path = os.path.join(current_dir, "config", "mail.yaml")

# Load the YAML file
def load_mail_prompts(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return None

# Load the prompts
prompts = load_mail_prompts(yaml_path)
if prompts:
    mail_system_prompt = prompts['cold_mail_prompt']
else:
    mail_system_prompt = "write mail on the basis of user prompt"
    
prompts_message_gen = load_mail_prompts(yaml_path)
if prompts_message_gen:
    linkedin_mssg_prompt = prompts_message_gen['gen_linkedin_mssg']
else:
    linkedin_mssg_prompt = "write mail on the basis of user prompt"


# Function to generate cold email using OpenAI API
def generate_cold_email_openai(user_prompt_1):
    model = "gpt-3.5-turbo"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are John Jacob, a Sales Development Executive at Aidetic. \n\n{mail_system_prompt}",
            },
            {
                "role": "user",
                "content": f"You are John Jacob, a Sales Representative of Aidetic Software Pvt Ltd. Write the mail that can be sent as a cold mail to potential customers. Write the mail to {user_prompt_1}.",
            },
        ],
        max_tokens=1024,
        temperature=0.7,
    )

    # Get the response content
    response_content = response.choices[0].message.content

    # Try to load the response as JSON, handle any errors
    try:
        data = json.loads(response_content)
        subject = data["subject"]
        body = data["body"]
        return subject, body
    except json.JSONDecodeError:
        return None, None


# Function to generate cold LinkedIn message using OpenAI API
def generate_cold_message_openai(user_prompt_1):
    model = "gpt-3.5-turbo"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are John Jacob, a Sales Development Executive at Aidetic. \n\n{linkedin_mssg_prompt}",
            },
            {
                "role": "user",
                "content": f"You are John Jacob, a Sales Representative of Aidetic Software Pvt Ltd. Write the message that can be sent to potential customers. Write the message to {user_prompt_1}.",
            },
        ],
        max_tokens=1024,
        temperature=0.7,
    )

    # Return the response as plain text
    response_content = response.choices[0].message.content

    return response_content
