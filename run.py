import argparse
from dotenv import load_dotenv
from auto_release_notes import generate_release_notes

def main():
    parser = argparse.ArgumentParser(description="Generate release notes for a specific path.")
    parser.add_argument(
        "--path", 
        default=".", 
        help="Only include changes under this directory"
    )
    args = parser.parse_args()
    load_dotenv('.secrets')
    release_notes = generate_release_notes(path=args.path)
    print(release_notes)

if __name__ == "__main__":
    main()
