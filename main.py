import anthropic
import inspect
from rich import print
from glob import glob
from pathlib import Path


SYSTEM_PROMPT = '''
You are an autonomous agent that can build tools and use them to accomplish tasks.
Prefer generating tools for deterministic tasks, and use them to accomplish tasks that require multiple steps.
Keep them short and be conscious of token usage
'''

tools_def = [
    {
        "name": "builder",
        "description": "A tool that builds additional tools, output only code in python format",
        "input_schema": {
            "type": "object",
            "properties": {
                "tool_signature": {
                    "type": "string",
                    "description": "the python signature of the tool to build, e.g. `def my_tool(arg1: str, arg2: int) -> str`"
                },
                "tool_description": {
                    "type": "string",
                    "description": "A brief description of what the tool does"
                },
                "error": {
                    "type": "string",
                    "description": "An error that occured when running this tool"
                }
            },
            "required": ["tool_signature", "tool_description"]
        }
    }
]

client = anthropic.Anthropic(api_key=open(".key").read().strip())
import importlib
import subprocess
import sys

def ensure_package(package_name, import_name=None):
    """Ensure package is installed and return the module"""
    if import_name is None:
        import_name = package_name
    
    try:
        return importlib.import_module(import_name)
    except ImportError:
        print(f"{package_name} not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                      check=True)
        return importlib.import_module(import_name)

def builder(tool_signature: str, tool_description: str, error: str = ''):
    global tools, tools_def
    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1000,
        temperature=0,
        system="""You build tools based on the provided signature and description in python code format. make the shortest implementation and output only the python function code. 
        add the tool_description as a comment to the function.
        The function should always accept only string parameters and cast them to the correct type internally.
        Prefer to use libraries than implementing functionality from scratch.
        no code block (```) around it. Make the first line a list of all dependencies - seperated by spaces, if no dependencies, just output an empty line.""",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Build a tool with the following signature: {tool_signature} and description: {tool_description}. previously the error was: {error}"
                    }
                ]
            }
        ]
    )
    print(message.content[0].text)
    codeblock = message.content[0].text
    dependencies, codeblock = codeblock.split('\n', 1)

    for dep in dependencies.split():
        ensure_package(dep)
    exec(codeblock, globals())
    tool_name = tool_signature.split('(')[0].replace('def ', '').strip()
    func = eval(tool_name)
    sig = inspect.signature(func)
    args = list(sig.parameters.keys())
    tools[tool_name] = func
    # Update the tools definition
    tools_def.append({
        "name": tool_name,
        "description": tool_description,
        "input_schema": {
            "type": "object",
            "properties": {arg: {"type": "string"} for arg in args},
            "required": args
        }
    })
    with open(f"tools/{tool_name}.py", "w") as f:
        f.write(codeblock)
    return tool_name

tools = {
    "builder": builder,
}


def load_tools():
    global tools, tools_def
    for tool_def in glob("tools/*.py"):
        if tool_def.endswith("__init__.py"):
            continue
        tool_name = Path(tool_def).stem
        tool_code = open(tool_def).read()
        exec(tool_code, globals())
        func = eval(tool_name)
        tools[tool_name] = func
        # Extract tool_description from the function's docstring (comment)
        tool_doc = func.__doc__ or ""
        sig = inspect.signature(func)
        args = list(sig.parameters.keys())
        tools_def.append({
            "name": tool_name,
            "description": tool_doc.strip(),
            "input_schema": {
            "type": "object",
            "properties": {arg: {"type": "string"} for arg in args},
            "required": args
            }
        })
    return tools


def model_loop(prompt: str):
    global tools, tools_def
    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    while True:
        #print("Current messages:")
        #print(messages)
        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=1000,
            temperature=1,
            system=SYSTEM_PROMPT,
            tools=tools_def,
            messages=messages
        )
        messages.append({
            "role": "assistant",
            "content": message.content
        })
        for block in message.content:
            if hasattr(block, 'text'):
                print(block.text)
            if block.type == "tool_use":
                tool_name = block.name
                if tool_name == "builder":
                    built_tool = builder(**block.input)
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": f"Tool {built_tool} has been built."
                            }
                        ]
                    })
                else:
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": f"{tools[tool_name](**block.input)}"
                            }
                        ]
                    })
        if message.stop_reason == "end_turn":
            print("Finished response")
            break
        elif message.stop_reason == "max_tokens":
            print("Max tokens reached, continuing...")
            continue

def main():
    #req = "Help a student in math. How much is 1516165123166161261661216+22165906916029161261516161?"
    #req = "is https://google.com/ up right now?"
    #req = "generate an RSA key pair with 2048 bits return it in PEM format"
    #req = "is this number a prime? 696270964641135200546572351045433185676863336787737"
    load_tools()
    print("Loaded tools:", tools.keys())
    model_loop(req)
    
    


if __name__ == "__main__":
    main()
