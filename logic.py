import re
from collections import deque


# extract all tokens between { } and return them in a queue
def extract_placeholders(template_text: str) -> deque:
    tokens = re.findall(r"\{(.*?)\}", template_text)
    return deque(tokens)

# make queue to hold user inputs in samee order
def initialize_input_queue(num_tokens: int) -> deque:
    return deque([""] * num_tokens)

# insert a user input into the next slot of the input queue
def add_user_input(input_queue: deque, value: str):
    if not input_queue:
        raise ValueError("Input queue is already full.")
    input_queue.popleft()
    input_queue.appendleft(value)

# replace tokens in template using the user input queue
def fill_story(template_text: str, placeholders: deque, user_inputs: deque) -> str:
    if len(placeholders) != len(user_inputs):
        raise ValueError("Number of placeholders and user inputs do not match.")

    final_text = template_text
    ph_copy = deque(placeholders)
    ui_copy = deque(user_inputs)

    while ph_copy:
        token = ph_copy.popleft()
        value = ui_copy.popleft()

        final_text = final_text.replace("{" + token + "}", value, 1)

    return final_text