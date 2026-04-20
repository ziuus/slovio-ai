import config
import anthropic
import openai
import ollama

def ask(messages, tools, system_prompt):
    if config.BRAIN == "claude":
        return ask_claude(messages, tools, system_prompt)
    elif config.BRAIN == "openai":
        return ask_openai(messages, tools, system_prompt)
    elif config.BRAIN == "ollama":
        return ask_ollama(messages, tools, system_prompt)
    elif config.BRAIN == "grok":
        return ask_grok(messages, tools, system_prompt)
    elif config.BRAIN == "nvidia":
        return ask_nvidia(messages, tools, system_prompt)
    else:
        raise ValueError("Invalid BRAIN setting in config")

class NormalResponse:
    def __init__(self, content, stop_reason, tool_uses):
        self.content = content
        self.stop_reason = stop_reason
        self.tool_uses = tool_uses

def ask_claude(messages, tools, system_prompt):
    if not config.ANTHROPIC_API_KEY:
        return NormalResponse("Slovio AI Mock Response: API Key is missing. Please add it to config.py or .env.", "end_turn", [])
    
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    
    anthropic_tools = []
    for t in tools:
        anthropic_tools.append({
            "name": t["name"],
            "description": t["description"],
            "input_schema": t["input_schema"]
        })

    # Filter messages for anthropic (role: user/assistant)
    anth_messages = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "assistant"
        anth_messages.append({"role": role, "content": msg["content"]})

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2048,
        system=system_prompt,
        messages=anth_messages,
        tools=anthropic_tools
    )
    
    content = ""
    tool_uses = []
    for block in response.content:
        if block.type == "text":
            content += block.text
        elif block.type == "tool_use":
            tool_uses.append({
                "name": block.name,
                "id": block.id,
                "input": block.input
            })
            
    stop_reason = response.stop_reason
    if stop_reason == "tool_use":
         pass
    else:
         stop_reason = "end_turn"
         
    return NormalResponse(content, stop_reason, tool_uses)

def ask_openai(messages, tools, system_prompt):
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    
    oai_tools = []
    for t in tools:
        oai_tools.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"]
            }
        })
        
    oai_messages = [{"role": "system", "content": system_prompt}] + messages
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=oai_messages,
        tools=oai_tools if oai_tools else None
    )
    
    msg = response.choices[0].message
    content = msg.content or ""
    tool_uses = []
    
    if msg.tool_calls:
        for call in msg.tool_calls:
            import json
            tool_uses.append({
                "name": call.function.name,
                "id": call.id,
                "input": json.loads(call.function.arguments)
            })
            
    stop_reason = response.choices[0].finish_reason
    if stop_reason == "tool_calls":
        stop_reason = "tool_use"
    else:
        stop_reason = "end_turn"
        
    return NormalResponse(content, stop_reason, tool_uses)

def ask_ollama(messages, tools, system_prompt):
    o_messages = [{"role": "system", "content": system_prompt}] + messages
    
    import json
    response = ollama.chat(
        model=config.OLLAMA_MODEL,
        messages=o_messages,
        tools=tools
    )
    
    msg = response.get('message', {})
    content = msg.get('content', '')
    tool_uses = []
    
    if msg.get('tool_calls'):
        for i, call in enumerate(msg['tool_calls']):
            tool_uses.append({
                "name": call['function']['name'],
                "id": f"call_{i}",
                "input": call['function']['arguments']
            })
            
    stop_reason = "tool_use" if tool_uses else "end_turn"
    
    return NormalResponse(content, stop_reason, tool_uses)
def ask_grok(messages, tools, system_prompt):
    # Detect if it's Groq or xAI based on key prefix
    api_key = config.GROK_API_KEY
    base_url = config.GROK_BASE_URL
    model = config.GROK_MODEL
    
    if api_key.startswith("gsk_"):
        base_url = "https://api.groq.com/openai/v1"
        # If user just said "grok" with a Groq key, they might need a Groq model
        if model == "grok-beta":
            model = "llama-3.3-70b-versatile" # Premium default for Groq
            
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    
    oai_tools = []
    for t in tools:
        oai_tools.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"]
            }
        })
        
    oai_messages = [{"role": "system", "content": system_prompt}] + messages
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=oai_messages,
            tools=oai_tools if oai_tools else None
        )
    except Exception as e:
        # resilient fallback for Groq tool_use_failed
        err_msg = str(e)
        if "tool_use_failed" in err_msg and "failed_generation" in err_msg:
            import re
            match = re.search(r"failed_generation':\s*'((?:[^']|\\')*)'", err_msg)
            if match:
                content = match.group(1)
                # Sanitize trailing backslashes which cause 'unicodeescape' error
                if content.endswith('\\') and not content.endswith('\\\\'):
                    content = content[:-1]
                try:
                    content = content.encode().decode('unicode_escape')
                except UnicodeDecodeError:
                    pass # Use raw content if decoding fails
                return NormalResponse(content, "end_turn", [])
        raise e
    
    msg = response.choices[0].message
    content = msg.content or ""
    tool_uses = []
    
    if msg.tool_calls:
        for call in msg.tool_calls:
            import json
            tool_uses.append({
                "name": call.function.name,
                "id": call.id,
                "input": json.loads(call.function.arguments)
            })
            
    stop_reason = response.choices[0].finish_reason
    if stop_reason == "tool_calls":
        stop_reason = "tool_use"
    else:
        stop_reason = "end_turn"
        
    return NormalResponse(content, stop_reason, tool_uses)

def ask_nvidia(messages, tools, system_prompt):
    api_key = config.NVIDIA_API_KEY
    if not api_key:
        return NormalResponse("System Error: NVIDIA_API_KEY is not configured.", "end_turn", [])
        
    client = openai.OpenAI(api_key=api_key, base_url=config.NVIDIA_BASE_URL)
    
    oai_tools = []
    for t in tools:
        oai_tools.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"]
            }
        })
        
    oai_messages = [{"role": "system", "content": system_prompt}] + messages
    
    try:
        response = client.chat.completions.create(
            model=config.NVIDIA_MODEL,
            messages=oai_messages,
            tools=oai_tools if oai_tools else None
        )
    except Exception as e:
        return NormalResponse(f"Nvidia API Error: {str(e)}", "end_turn", [])
    
    msg = response.choices[0].message
    content = msg.content or ""
    tool_uses = []
    
    if msg.tool_calls:
        for call in msg.tool_calls:
            import json
            tool_uses.append({
                "name": call.function.name,
                "id": call.id,
                "input": json.loads(call.function.arguments)
            })
            
    stop_reason = response.choices[0].finish_reason
    if stop_reason == "tool_calls":
        stop_reason = "tool_use"
    else:
        stop_reason = "end_turn"
        
    return NormalResponse(content, stop_reason, tool_uses)
