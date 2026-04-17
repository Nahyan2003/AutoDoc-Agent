import os
import hashlib
import datetime
from dotenv import load_dotenv
from groq import Groq

# 1. Setup
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_code_hash(content):
    """Creates a unique fingerprint of the code text."""
    return hashlib.md5(content.encode()).hexdigest()

def has_code_changed(new_content):
    """Checks if code changed without saving the hash yet."""
    hash_file = ".code_hash"
    new_hash = get_code_hash(new_content)
    
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            old_hash = f.read().strip()
        if old_hash == new_hash:
            return False 
    return True

def save_hash(new_content):
    """Saves memory only after a successful update."""
    hash_file = ".code_hash"
    new_hash = get_code_hash(new_content)
    with open(hash_file, "w") as f:
        f.write(new_hash)
    print("DEBUG: Hash saved to memory.")

def read_code():
    with open("sample_code.py", "r") as f:
        return f.read()

def ask_ai(code_content):
    print("AutoDoc Agent is thinking...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a technical writer. Summarize this code in one short, clear sentence."},
            {"role": "user", "content": code_content}
        ]
    )
    return completion.choices[0].message.content

def update_readme(summary):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("README.md", "a", encoding="utf-8") as f:
        f.write(f"\n\n### AI AutoDoc Update ({timestamp})\n> {summary}\n")
    print(f"DEBUG: README.md updated successfully at {timestamp}!")

if __name__ == "__main__":
    try:
        code_content = read_code()
        
        if has_code_changed(code_content):
            ai_summary = ask_ai(code_content)
            update_readme(ai_summary)
            save_hash(code_content)
        else:
            print("No changes detected in sample_code.py. Skipping update.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")