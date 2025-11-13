from google import genai
from google.genai import types

client = genai.Client(api_key = "GEMINI_API_KEY")

is_loading = False

def generate_madlib_prompt():
    global is_loading
    is_loading = True

    prompt = """
    Create a madlib story template with blanks for user input.
    The story should be between 3-5 sentences long.
    Use placeholders like {noun}, {verb}, {adjective}, {place}.
    Do NOT fill the blanks in, leave the placeholders as is.
    Make sure that each placeholder appears at least once in the story, there can be repeats but make them unique to the story.
    The story can be serious or funny, as long as it is creative and engaging for users.

"""
    response = client.models.generate_text(
        model = "gemini-2.5-flash",
        contents = prompt,

        max_output_tokens = 300,

    )

    is_loading = False

    ## does there need to be a prompt limit in the prompt or reponse
    return response.text