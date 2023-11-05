from auto_everything.ml import ML
from auto_everything.disk import Disk
from auto_everything.terminal import Terminal
ml = ML()
disk = Disk()
terminal = Terminal()

text_generator = ml.Yingshaoxo_Text_Generator(
    input_txt_folder_path="../18.fake_ai_asistant/input_txt_files",
    use_machine_learning=False
)

import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("Intel/dynamic_tinybert")
model = AutoModelForQuestionAnswering.from_pretrained("Intel/dynamic_tinybert")

def get_answer_by_using_context_and_question(context, question) -> str:
    context = context[-512:]
    question = question[-512:]

    #context = "remember the number 123456, I'll ask you later."
    #question = "What is the number I told you?"

    # Tokenize the context and question
    #tokens = tokenizer.encode_plus(question, context, return_tensors="pt")
    tokens = tokenizer.encode_plus(context, question, return_tensors="pt")

    # Get the input IDs and attention mask
    input_ids = tokens["input_ids"]
    attention_mask = tokens["attention_mask"]

    # Perform question answering
    outputs = model(input_ids, attention_mask=attention_mask)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # Find the start and end positions of the answer
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][answer_start:answer_end]))

    answer = answer.replace("[CLS]", "").replace("[SEP]", "").strip()

    return answer

def decode_response(text: str, chat_context: str, return_more: bool = False):
    splits = text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n")

    if return_more == True:
        #splits = [terminal.run_python_code(one) for one in splits]
        return "\n".join(splits[:2])

    if (len(splits) > 1):
        response = splits[1].strip()
    elif (len(splits) == 1):
        response = splits[0].strip()
    else:
        response = ""
    new_code = f"""
chat_context = '''{chat_context}'''

{response}
"""
    final_response = terminal.run_python_code(code=new_code)
    if final_response.strip() == "":
        final_response = response
    final_response = "\n".join([one for one in final_response.split("\n") if not one.strip().startswith("__**")])

    return final_response


print("\n\n")
all_input_text = ""

while True:
    input_text = input("What you want to say? \n")

    all_input_text += input_text + "\n"
    real_input = all_input_text[-800:].strip()

    response = text_generator.search_and_get_following_text_in_a_exact_way(input_text=real_input, quick_mode=True)

    response = decode_response(text=response, chat_context=all_input_text, return_more=False)
    #print("\n************\n" + response + "\n************\n")
    response2 = get_answer_by_using_context_and_question(all_input_text + "\n" + response, input_text)
    if response2 == "":
        pass
    else:
        response = response2
        print("by bert")

    print("\n\n---------\n\n")
    print(response)
    print("\n\n---------\n\n")
