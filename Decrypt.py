from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

SCRIPT_DIR = Path(__file__).parent.resolve()
SANDBOX_DIR = SCRIPT_DIR / "test_files"
KEY_FILE = SCRIPT_DIR / "ransom.key"
RANSOM_NOTE = "README_RANSOM.txt"


def decrypt_files(fernet):
    count = 0
    for filepath in SANDBOX_DIR.iterdir():
        if filepath.name == RANSOM_NOTE or not filepath.is_file():
            continue
        try:
            filepath.write_bytes(fernet.decrypt(filepath.read_bytes()))
            print(f"[+] Decrypted: {filepath.name}")
            count += 1
        except InvalidToken:
            print(f"[-] Skipped (wrong key or already decrypted): {filepath.name}")
    return count


def main():
    print("=" * 52)
    print("   DECRYPTION  —  RANSOMWARE SIMULATION")
    print("=" * 52)

    if not SANDBOX_DIR.exists():
        print("[!] No sandbox found. Run Ransom.py first.")
        return

    if not KEY_FILE.exists():
        print("[!] Key file not found — cannot decrypt.")
        return

    print(f"\n[*] Loading key from: {KEY_FILE.name}")
    fernet = Fernet(KEY_FILE.read_bytes())

    print("[*] Decrypting files...")
    count = decrypt_files(fernet)

    note_path = SANDBOX_DIR / RANSOM_NOTE
    if note_path.exists():
        note_path.unlink()
        print(f"[*] Ransom note removed.")

    print(f"\n[+] Done. {count} file(s) restored.")


if __name__ == "__main__":
    main()
