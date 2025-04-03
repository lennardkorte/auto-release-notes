from dotenv import load_dotenv
from auto_release_notes import generate_release_notes

def main():
    load_dotenv('.secrets')
    release_notes = generate_release_notes()
    print(release_notes)

if __name__ == "__main__":
    main()
