import random
from ollama import chat

def load_words():
    """
    Loads a set of valid English words from words.txt.
    Each word in the file is assumed to be on its own line.
    """
    with open('words.txt', 'r') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def generate_random_words(word_list, num_words=3):
    """
    Selects a few random words from the provided list or set.
    """
    words_list = list(word_list)
    return random.sample(words_list, num_words)

def generate_idea_with_ollama_stream(random_words, model='llama3:70b'):
    user_message = (
        "Generate an innovative technology or business idea that involves "
        f"the following concepts: {', '.join(random_words)}. "
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

    print("Generated Words:", random_words)

    idea = generate_idea_with_ollama_stream(random_words, model='llama3:70b')
    print("Complete Idea (accumulated):\n", idea)