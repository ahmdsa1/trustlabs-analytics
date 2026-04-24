"""
Run this script once to generate hashed passwords for config.yaml.
Usage: python generate_passwords.py
Then copy the hashed passwords into config.yaml.
"""
import streamlit_authenticator as stauth

passwords = ["292712@Aa", "DNAequation"]
hashed = stauth.Hasher(passwords).generate()

print("=== Hashed Passwords ===")
print(f"admin password hash:   {hashed[0]}")
print(f"manager password hash: {hashed[1]}")
print()
print("Paste these into config.yaml under each user's 'password' field.")
