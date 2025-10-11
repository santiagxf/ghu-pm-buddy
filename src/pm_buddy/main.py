import os


def main():
    input_text = os.environ.get("PM_BUDDY_INPUT", "Hello from pm-buddy!")
    print(f"PM Buddy running with input: {input_text}")


if __name__ == "__main__":
    main()
