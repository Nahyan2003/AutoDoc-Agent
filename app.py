import os
import hashlib
from dotenv import load_dotenv
from groq import Groq

# 1. Setup
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_code_hash(content):
    """Creates a unique fingerprint of the code text."""
    return hashlib.md5(content.encode()).hexdigest()

def has_code_changed(new_content):
    """Checks if the code is different from the last time without saving it yet."""
    hash_file = ".code_hash"
    new_hash = get_code_hash(new_content)
    
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            old_hash = f.read().strip()
        if old_hash == new_hash:
            return False 
    return True

def save_hash(new_content):
    """Saves the fingerprint ONLY after a successful update."""
    hash_file = ".code_hash"
    new_hash = get_code_hash(new_content)
    with open(hash_file, "w") as f:
        f.write(new_hash)
    print("New hash saved to memory.")

def read_code():
    with open("sample_code.py", "r") as f:
        return f.read()

def ask_ai(code_content):
    print("AutoDoc Agent is thinking (using Groq)...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Summarize code in 1 short sentence."},
            {"role": "user", "content": code_content}
        ]
    )
    return completion.choices[0].message.content

def update_readme(summary):
    # 'a' means append. Ensure encoding is utf-8
    with open("README.md", "a", encoding="utf-8") as f:
        f.write(f"\n\n## AutoDoc Update (Groq)\n{summary}\n")
    print("README.md updated successfully!")

# --- THE MASTER PLAN ---
if __name__ == "__main__":
    try:
        content = read_code()
        
        if has_code_changed(content):
            ai_msg = ask_ai(content)
            update_readme(ai_msg)
            # ONLY save the hash if we successfully reached this point
            save_hash(content)
        else:
            print("No changes detected. Skipping AI update.")
            
    except Exception as e:
        print(f"Error: {e}")