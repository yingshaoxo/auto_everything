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
