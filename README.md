# RansomwareSimulator

This repository contains files to simulate a ransomware attack. The 2 files in this project shows both how the attacker encrypts information, and when in a real world scenario receives the payments send the decryption key (which is what the Decrypt file is for). All of this is for educational purposes and meant to simulate how a real world ransomware attack can occur.

The 2 different files have the following objectives:
Ransom.py aka the "attacker" side:

1. Creates test_files/ with 4 dummy victim files
2. Generates a Fernet key (AES-128 + HMAC), saves it to ransom.key
3. Encrypts every file in the sandbox in-place
4. Drops a README_RANSOM.txt ransom note with a fake victim ID

Decrypt.py which simulates the victim receiving the key:

1. Reads ransom.key
2. Decrypts all files back to their original content
3. Removes the ransom note

To run the simulation you'll need the cryptography package. If you don't already have it you need to:
```
pip install cryptography
```

Remember! this simulation is only meant to show the basics of a ransomware attack. In a real world scenario the attacker would never save the ransom.key locally, but on the attacker's C2 server.
