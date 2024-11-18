from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import re

llm = ChatOpenAI(model="gpt-4o-mini")

def generate_code(prompt):

    messages = [
        SystemMessage(
            content="You are a web development expert, and you are tasked with creating a code snippet that goes as content of single html page. Respond only with code and nothing else or else the code workflow will break. skip header footer and other tags. just wrap content in a div. please add necessary style element along."
        ),
        HumanMessage(
            content=prompt
        )
    ]

    result = llm.invoke(messages)
    generated_code = result.content
    match = re.search(r'```html\n(.*?)\n```', generated_code, re.DOTALL)

    if match:
        generated_code = match.group(1)

    print(generated_code)

    return generated_code

# Save the generated code snippet to a file
def save_code_snippet(code):
    print("code being written:", code)
    with open('static/pages/home.html', 'w') as f:
        f.write(code)