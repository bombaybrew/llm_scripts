from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import re

llm = ChatOpenAI(model="gpt-4o-mini")

def generate_code(prompt):

    define_nav(prompt)
    define_home(prompt)

    return True

def define_nav(prompt):
    messages = [
        SystemMessage(
            content="""You are a web development expert.
                     for the given user requirement, decide 4 tabs that are needed for the web app and then write only the nav component.
                     Just return the html and nothing else or else the code will break.
                     Keep the tab names short.
                     use following as example for home and fav tab
                     <nav class="bg-base-200 shadow-lg p-2 flex justify-around items-center sticky bottom-0 z-10">
                        <button class="btn btn-outline btn-sm flex flex-col items-center" hx-get="pages/home.html" hx-target="#content-area"
                            hx-swap="innerHTML">
                            <span>Home</span>
                        </button>
                        <button class="btn btn-outline btn-sm flex flex-col items-center" hx-get="pages/fav.html"
                            hx-target="#content-area" hx-swap="innerHTML">
                            <span>Fav</span>
                        </button>
                        </nav>"""
                     
        ),
        HumanMessage(
            content=prompt
        )
    ]

    result = llm.invoke(messages)
    nav_code = result.content
    match = re.search(r'```html\n(.*?)\n```', nav_code, re.DOTALL)

    if match:
        nav_code = match.group(1)

    print(nav_code)
    with open('static/components/nav.html', 'w') as f:
        f.write(nav_code)
    return True


def define_home(prompt):
    messages = [
        SystemMessage(
            content=("You are a web development expert."
                     "for the given user requirement, write the content of the home page."
                     "Wrap the content in a div tab. this content will be displayed withing a container which already has required html setup and uses tailwind css."
                     " Just return the html and nothing else or else the code will break."
                     )
        ),
        HumanMessage(
            content=prompt
        )
    ]

    result = llm.invoke(messages)
    home_code = result.content
    match = re.search(r'```html\n(.*?)\n```', home_code, re.DOTALL)

    if match:
        home_code = match.group(1)

    print(home_code)
    with open('static/pages/home.html', 'w') as f:
        f.write(home_code)
    return True