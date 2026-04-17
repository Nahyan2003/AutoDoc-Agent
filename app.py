import os
import hashlib
import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_code_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def read_code():
    # Make sure this filename matches YOUR file exactly (case-sensitive!)
    filename = "sample_code.py" 
    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = f.read()
            print(f"DEBUG: Successfully read {filename}. Length: {len(content)}")
            return content
    else:
        print(f"ERROR: {filename} not found!")
        return None

def ask_ai(code_content):
    print("DEBUG: Sending code to Groq AI...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a technical writer. Summarize this code in one short sentence."},
            {"role": "user", "content": f"Summarize this Python code: {code_content}"}
        ]
    )
    return completion.choices[0].message.content

def update_readme(summary):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("README.md", "a", encoding="utf-8") as f:
        f.write(f"\n\n### AI AutoDoc Update ({timestamp})\n> {summary}\n")
    print(f"DEBUG: README.md updated successfully at {timestamp}")

if __name__ == "__main__":
    try:
        content = read_code()
        if content:
            # We skip the hash check for THIS run to force a correct update
            ai_msg = ask_ai(content)
            update_readme(ai_msg)
            
            # Save hash so it doesn't repeat next time unless code changes
            new_hash = get_code_hash(content)
            with open(".code_hash", "w") as f:
                f.write(new_hash)
        else:
            print("Action failed: No code content found to summarize.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")