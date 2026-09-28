import pandas as pd
import random
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

easy_prompts = [
    "Hello, how are you?", "What is the capital of France?", 
    "Summarize this text.", "Write a polite email saying I will be late.",
    "What is the weather like today?", "Translate 'hello' to Spanish."
]
medium_prompts = [
    "Compare the differences between Python and Java.", 
    "What are the main causes of the French Revolution?",
    "Explain quantum computing to a 5-year-old.",
    "Write a short essay on climate change impacts.",
    "How do I structure a JSON payload for a REST API?"
]
hard_prompts = [
    "Write a Python script to scrape a website and save to CSV.",
    "How do I fix this React useEffect dependency array infinite loop: ```javascript ... ```",
    "Calculate the time complexity of a recursive Fibonacci sequence using Big O notation.",
    "Write a SQL query with multiple INNER JOINS and a window function.",
    "Debug this memory leak in my C++ pointer assignment: ```cpp ... ```"
]

data = []
for _ in range(300):
    data.append({"prompt": random.choice(easy_prompts) + " " * random.randint(0, 5), "tier": 0})
    data.append({"prompt": random.choice(medium_prompts) + " " * random.randint(0, 10), "tier": 1})
    data.append({"prompt": random.choice(hard_prompts) + " " * random.randint(0, 15), "tier": 2})

df = pd.DataFrame(data)
# Shuffle dataset
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("data/training_data.csv", index=False)
print("✅ Successfully generated 900 synthetic prompts in data/training_data.csv!")