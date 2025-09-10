# Yingshaoxo_Language

Chinese and English.

## How to parse?

Similar to how you write python.

You write a nutrual language parsing software.

## Example 1

```
{
    "你说": {
        "呢": {
            "?": {
                "__action__": "python_code: write my view"
            }
        },
        "话": {
            "。": {
                "__action__": "python_code: response to show I am alive"
            }
        }
        "__router__": "python_code"
    },
    "i ": {
        "am ": {
            "{description}": {
                "__action__": "python_code: take a note, user said he/she is {description}"
            }
        },
        "like ": {
            "you": {
                "__action__": "python_code: save note, someone likes me"
            },
            "her": {},
        },
    }
    "what is ": {
        "{an_object}": {
            "__action__": "python_code: search {an_object} in internet to get description and reply"
        },
    }
}

你甚至可以用这个来写python解析器，或者自然语言解析器。每次路由到下一级还附带新信息帮助下一级分类。
```

## Example 2

Write code. 

Low inteligence people can't write high inteligence code. Unless he or she do copy.

## Thinking

shi_jie_shang hao_duo_dong_xi dou_hui_guo_shi, dan_shi wo_zhe_ge xiang_fa, ji_qian_nian dou_bu_hui guo_shi.

## Detailed (Language Generation) Algorithm

### Step 1, split text into 8000 char sub_string_window

```
source_text = "..."

string_window_list = []
for index, _ in enumerate(source_text):
    string_window = source_text[index: index+8000]
```

> the 8000 can be 512, so in the end you can complete '(512 - len(input_text))' characters.

### Step 2, get language tree

```
{
    "what": {
        "is": {
            "your": {
                "name": {},
                "age": {},
            }
        },
        "are": {}
    }
}
```

```
language_magic_tree = {}

def put_word_into_tree(sub_dict_tree, word_list):
    if len(word_list) == 0:
        return
    word = word_list[0]
    if word not in sub_dict_tree.keys():
        sub_dict_tree[word] = {"__counting__": 1}
    else:
        sub_dict_tree[word]["__counting__"] += 1
    put_word_into_tree(sub_dict_tree[word], word_list[1:])

for string_window in string_window_list:
    words = string_window.split(" ")
    put_word_into_tree(language_magic_tree, words)
```

### Step3, search input_text in tree

```
{
    "what": {
        "is": {
            "your": {
                "name": {},
                "age": {},
            }
        },
        "are": {}
    }
}
```

If input_text is "what is your", there basically only has two result, one is "name", another is "age".

If input_text is "what shit your", when you search to "what", there has no other option in tree, it seems like it is a new word "shit". So you remember "shit", you search the next word "your" in child tree, if you found one, called "what is your name", then "shit == is", so you do a global replacement for "is", "shit" is everywhere now. Do you understand now?

By doing unknown word global replacement, we can let the unknown word in question be exists in our answers. Just similar to what big_ai_model did.

> chinese: 查tree时有可能遇到没有词的情况，跳过那一级节点，查下一级，跳过的部分要记住，在后面要做文本全局替换。这样就和高端大模型一样了，能把问句里面的未知词汇带入回答里面。

> Or if you do not like to search the sub_tree, you can randomly choose one from keys as 'shit' and do global replacement.

### Step4, tree size can be reduced by reuse similar sub_tree

For two sub_tree that is similar, you simply extract and give it an ID, you put the sub_tree ID into main tree.

### Step5, super speed while low storage usage

We are using a dict tree.
