from logic import extract_placeholders, initialize_input_queue, add_user_input, fill_story
import ai

def main():
    # Test the AI generation and logic
    ai_output = ai.generate_madlib_prompt()
    
    if ai_output:
        print("Generated Template:")
        print(ai_output)
        print("\n" + "="*50 + "\n")
        
        placeholders = extract_placeholders(ai_output)
        user_inputs = initialize_input_queue(len(placeholders))
        
        placeholders_list = list(placeholders)
        
        for token in placeholders_list:
            value = input(f"Enter a value for '{token}': ")
            add_user_input(user_inputs, value)
        
        result = fill_story(ai_output, placeholders, user_inputs)
        print("\nYour MadLib Story:")
        print(result)
    else:
        print("Failed to generate story template")

if __name__ == "__main__":
    main()