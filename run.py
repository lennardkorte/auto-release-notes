from dotenv import load_dotenv
from auto_release_notes import generate_release_notes

def main():
    try:
        load_dotenv('.secrets')
        release_notes = generate_release_notes()
        print("\n📢 Generated Release Notes:\n")
        print(release_notes)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
