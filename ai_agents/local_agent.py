from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load a small, local model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create a function to retrieve current date and time
import datetime

# 1. Define your Tool
def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def local_agent(prompt, max_length=50):
    # 2. Update the system prompt to give the model a "choice"
    system_prompt = (
        "Assistant instructions: If you need the time, write 'ACTION: get_time'.\n"
        f"User: {prompt}\n"
        "Assistant: "
    )
    encoded = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **encoded,
        max_length=max_length,
        temperature=0.8,
        do_sample=True,
        top_p=0.9,
        repetition_penalty=1.2,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 3. THE AGENT LOGIC: Check for the "Action" keyword
    if "ACTION: get_time" in response:
        print("--- System: Agent is calling a tool... ---")
        time_val = get_time()
        return f"The current time is {time_val}." # Simple version
    return response
# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    response = local_agent(user_input)
    print("Agent:", response)
