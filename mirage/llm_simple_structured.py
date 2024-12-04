from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage
import re
from langchain_core.pydantic_v1 import BaseModel, Field

#llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatMistralAI(
    model="codestral-latest",
    temperature=0,
    max_retries=2,
    api_key="",
    streaming=False
)   

class Tab(BaseModel):
    tabName: str = Field(description="Name of the tab")
    tabDescription: str = Field(description="One line of description of the tab")

class WebApp(BaseModel):
    tabs: list[Tab] = Field(description="List of tabs")
    tabsCode: str = Field(description="HTML <div> code for tabs")
    tabContentCode: list[str] = Field(description="List of detailed HTML code for all tabs content")
    
structured_llm = llm.with_structured_output(WebApp, method="json_mode")
    

def explore_prompt(prompt: str):
    """Explore the prompt and generate code snippet.

    Args:
        prompt: user input to generate WebApp class contents
    """
    messages = [
        SystemMessage(
            content="You are a web development expert, and you are tasked is explore the promot and deside for web app how many tabs required, also provide the detailed one line of description for each tab." + 
            "respond in JSON with all list of tab names into `tabName` key, what html data needs to show into `tabDescription` key now that list into `tabs` key" + 
            "Now for tabs html code, create <div> and <style> code, don't add '...' generate all tabs code for tabs in `tabsCode` key and html code for all tabs into list of `tabContentCode` key"
        ),
        HumanMessage(
            content=prompt
        )
    ]
    result = structured_llm.invoke(messages)
    print("AI result:", result)
    
    # Save the generated code snippet to a provided file
    save_code_snippet_with_filename('static/components/nav.html', result.tabsCode)
    
    for tab in result.tabs:
        code = generate_code(tab.tabDescription)
        save_code_snippet_with_filename(f'static/components/{tab.tabName}.html', code)
    
    print("AI Job completed")
    
    return result

def generate_code(prompt: str):
    """Generate html code for x snippet.

    Args:
        prompt: user input for generate html code
    """
    messages = [
        SystemMessage(
            content="You are a html development expert, and you are tasked with creating a html code snippet that goes as content of single html page. Respond only with complete code after your code I don't need to add any manual code, and nothing else or else the code workflow will break. please add necessary style element along."
        ),
        HumanMessage(
            content=prompt
        )
    ]
    result = llm.invoke(messages)
    generated_code = result.content
    matchCode = re.search(r'```html\n(.*?)\n```', generated_code, re.DOTALL)
    if matchCode:
        generated_code = matchCode.group(1)
    print(generated_code)
    return generated_code
        
# Save the generated code snippet to a provided file
def save_code_snippet_with_filename(filename, code):
    """Save the generated code snippet to a file.

    Args:
        filename (str): The name of the file to save the code.
        code (str): The code to be saved.
    """
    print("code being written:", code)
    with open(filename, 'w+') as f:
        f.write(code)        