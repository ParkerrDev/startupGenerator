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

def get_word_definitions(words, english_dict):
    """
    Gets definitions for the given words using the English dictionary.
    Returns a dictionary of word: definition pairs.
    """
    definitions = {}
    for word in words:
        try:
            definition = english_dict[word]
            definitions[word] = definition
        except KeyError:
            continue
    return definitions

def generate_random_words(word_list, num_words=3):
    """
    Selects random words from the provided list or set, ensuring each word has a valid definition.
    """
    words_list = list(word_list)
    selected_words = set()
    english_dict = get_dict()
    
    while len(selected_words) < num_words:
        word = random.choice(words_list)
        try:
            if word not in selected_words and english_dict[word]:
                selected_words.add(word)
        except KeyError:
            continue
    
    return list(selected_words)

def generate_idea_with_ollama_stream(random_words, definitions, model='llama3:70b'):
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
    english_dict = get_dict()
    random_words = generate_random_words(english_words, num_words=3)
    definitions = get_word_definitions(random_words, english_dict)

    print("Generated Words with Definitions:")
    for word in random_words:
        print(f"{word}: {definitions[word]}")
    print()

    idea = generate_idea_with_ollama_stream(random_words, definitions, model='llama3:70b')
    print("Complete Idea (accumulated):\n", idea)