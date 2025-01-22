import random
from ollama import chat
from english_dictionary.scripts.read_pickle import get_dict

def load_words():
    """
    Loads a set of valid English words from words.txt.
    Each word in the file is assumed to be on its own line.
    """
    with open('words.txt', 'r') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def get_word_definitions(words):
    """
    Gets definitions for the given words using the English dictionary.
    Returns a dictionary of word: definition pairs.
    """
    english_dict = get_dict()
    definitions = {}
    for word in words:
        try:
            definitions[word] = english_dict[word]
        except KeyError:
            definitions[word] = "Definition not found"
    return definitions

def generate_random_words(word_list, num_words=3):
    """
    Selects a few random words from the provided list or set.
    """
    words_list = list(word_list)
    return random.sample(words_list, num_words)

def generate_idea_with_ollama_stream(random_words, definitions, model='llama3:8b'):
    word_def_pairs = [f"{word} ({definitions[word]})" for word in random_words]
    user_message = (
        "Generate a profitable business idea that involves "
        f"the following concepts and their definitions: {', '.join(word_def_pairs)}. "
        "Explain what makes this idea unique and how it could be implemented."
    )

    response_stream = chat(
        model=model,
        messages=[{'role': 'user', 'content': user_message}],
        stream=True
    )

    print("Generated idea (streaming):")
    idea_chunks = []
    for chunk in response_stream:
        chunk_text = chunk['message']['content']
        print(chunk_text, end='', flush=True)
        idea_chunks.append(chunk_text)

    print("\n")
    return ''.join(idea_chunks)

if __name__ == "__main__":
    english_words = load_words()
    random_words = generate_random_words(english_words, num_words=3)
    definitions = get_word_definitions(random_words)

    print("Generated Words with Definitions:")
    for word in random_words:
        print(f"{word}: {definitions[word]}")
    print()

    idea = generate_idea_with_ollama_stream(random_words, definitions, model='llama3:8b')
    print("Complete Idea (accumulated):\n", idea)