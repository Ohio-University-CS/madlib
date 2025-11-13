# ai.py - Fixed version with proper fallback
import random

is_loading = False

def generate_madlib_prompt():
    global is_loading
    is_loading = True
    
    # Simulate loading time
    import time
    time.sleep(1)
    
    templates = [
        "In a mysterious {place}, a {adjective} {noun} decided to {verb} all day long. It was the most {emotion} experience ever! Everyone shouted '{exclamation}!' when they saw it.",
        "The {adjective} {animal} from {place} loved to {verb} more than anything. One sunny day, it found a shiny {object} and felt incredibly {emotion}. What a {adjective2} day!",
        "When I traveled to {place}, I encountered the most {adjective} {noun} imaginable. It was busy trying to {verb} while balancing a {food} on its head. How {emotion}!",
        "Deep in the {place}, a {adjective} {occupation} was learning to {verb}. The journey was {emotion} and filled with {adjective2} surprises. '{exclamation}!', they yelled in excitement.",
        "On a {adjective} morning in {place}, the local {animal} started to {verb} uncontrollably. This caused quite the {emotion} scene at the {place2}. What a {adjective2} situation!"
    ]
    
    is_loading = False
    return random.choice(templates)

def fallback_template():
    return generate_madlib_prompt()

def generate_local_story():
    return generate_madlib_prompt()