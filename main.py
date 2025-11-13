# ------------------------------------------------------------
# main.py — Example driver for the Mad Libs logic system
# ------------------------------------------------------------

from logic import (
    extract_placeholders,
    initialize_input_queue,
    add_user_input,
    fill_story,
)


def main():
    ai_output = (
        #AI generated text
    )

    placeholders = extract_placeholders(ai_output)
    user_inputs = initialize_input_queue(len(placeholders))

    #convert queue to list
    placeholders_list = list(placeholders)

    for token in placeholders_list:
        value = input(f"Enter a value for '{token}': ")
        add_user_input(user_inputs, value)

    result = fill_story(ai_output, placeholders, user_inputs)

if __name__ == "__main__":
    main()
