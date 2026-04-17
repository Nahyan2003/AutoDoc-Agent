import os
import hashlib
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- FORCED DEBUGGING ---
def update_readme_force(summary):
    print("DEBUG: Force-writing to README.md...")
    # Using 'a' to append, but let's add a clear separator
    with open("README.md", "a", encoding="utf-8") as f:
        f.write(f"\n\n## AGENT TEST SUCCESS\n{summary}\n")
    print("DEBUG: Write complete.")

if __name__ == "__main__":
    try:
        # 1. Force a summary regardless of hash for this one test
        print("DEBUG: Starting AI call...")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Write 'The Agent is active' in 3 words."}]
        )
        msg = completion.choices[0].message.content
        
        # 2. Force the update
        update_readme_force(msg)
        
        # 3. Create a dummy hash file just to satisfy Git
        with open(".code_hash", "w") as f:
            f.write("force_test_123")
            
    except Exception as e:
        print(f"ERROR: {e}")