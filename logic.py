import re
from collections import deque

def extract_placeholders(template_text: str) -> deque:
    tokens = re.findall(r"\{(.*?)\}", template_text)
    return deque(tokens)

def initialize_input_queue(num_tokens: int) -> deque:
    return deque([""] * num_tokens)

def add_user_input(input_queue: deque, value: str):
    # FIXED: Find the next empty slot and fill it
    for i in range(len(input_queue)):
        if input_queue[i] == "":
            input_queue[i] = value
            return
    
    # If no empty slot found, append to the end
    input_queue.append(value)

def fill_story(template_text: str, placeholders: deque, user_inputs: deque) -> str:
    if len(placeholders) != len(user_inputs):
        raise ValueError(f"Number of placeholders ({len(placeholders)}) and user inputs ({len(user_inputs)}) do not match.")

    final_text = template_text
    ph_copy = deque(placeholders)
    ui_copy = deque(user_inputs)

    while ph_copy:
        token = ph_copy.popleft()
        value = ui_copy.popleft()
        final_text = final_text.replace("{" + token + "}", value, 1)

    return final_text