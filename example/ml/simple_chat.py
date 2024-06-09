while True:
    input_text = input("What you want to say? ").lower()
    response = "(keep silence)"
    if "?" in input_text and " to " in input_text:
        response = "By doing the right thing."
    elif "?" in input_text and any([input_text.startswith(one.lower()) for one in ["what ", "how ", "why ", "where ", "can ", "should ", "will ", "are ", "is ", "were ", "does", "do ", "who "]]):
        response = "I do not tell you."
    print("\n\n----------\n\n")
    print(response)
    print("\n\n----------\n\n")
