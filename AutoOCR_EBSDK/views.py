from django.shortcuts import render
import erniebot
import json
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html') 

def ask(request):
    question = request.GET.get('question', '')
    print(question)

    erniebot.api_type = 'aistudio'
    erniebot.access_token = 'api-key'
    model = 'ernie-bot'

    message_content = "The task scenario is: I need you to refine the knowledge points I provide into four small modules to help me learn."\
                    "The best wat to refine is to follow a good learning path, and you need to stand from the perspective of a teacher to help me learn the knowledge well"\
                    f"-对每个模块及逆行介绍，让读者能够直观地知道该模块的学习内容 我提供的知识点为：{question}" \
                    "-示例json文件如下，参考它的格式：[{\"模块主题\": \"\", \"本模块内容简介\": \"\"},] " \
                    "- Strictly follow the format I provided" \
                    "- 每个模块的介绍在30个中文汉字左右。" \
                    "- The output is just pure JSON format, with no other descriptions."
    messages = [
        {
            'role': 'user',
            'top_p': '0.001',
            'content': message_content
        }
    ]

    response = erniebot.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    answer = response.result

    try:
        json_start = answer.find('[')
        json_end = answer.find(']')
        if json_start != -1 and json_end != -1:
            json_content = answer[json_start:json_end+1]

            answer_dict = json.loads(json_content)

        else:
            answer_dict = {}
        
    except json.JSONDecodeError:
        answer_dict = {}

    module_titles = []
    for item in answer_dict:
        module_title = item.get("模块主题", "")
        module_description = item.get("本模块内容简介", "")
        if module_title and module_description:
            module_titles.append({"title":module_title, "content":module_description})

    print(module_titles)
    return JsonResponse(module_titles, safe=False)

