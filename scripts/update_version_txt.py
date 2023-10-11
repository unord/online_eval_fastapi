def main():
    try:
        with open("version.txt", "r") as f:
            current_version = float(f.read().strip())
    except FileNotFoundError:
        current_version = 1.00  # Default version if version.txt does not exist

    new_version = "{:.2f}".format(current_version + 0.01)

    with open("version.txt", "w") as f:
        f.write(new_version)

if __name__ == "__main__":
    main()
