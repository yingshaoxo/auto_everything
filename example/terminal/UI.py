from auto_everything.terminal import Terminal_User_Interface

def seperate_page_loading_function(page_size:int, current_page:int):
    all_elements = [
    ]
    for i in range(1000):
        #all_elements.append((str(i)*11, None))
        all_elements.append(str(i)*11)

    index = page_size * current_page
    return all_elements[index: index + page_size]

terminal_user_interface = Terminal_User_Interface()
result = terminal_user_interface.selection_box(text="Please select one:", selections=[], seperate_page_loading_function=seperate_page_loading_function)
print(result)
