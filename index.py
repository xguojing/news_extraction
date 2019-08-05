from flask import Flask, request, render_template
from app.speaker_point import search_dependency
import json

app = Flask(__name__)

related_word = ['诊断', '交代', '说', '说道', '指出', '报道', '报道说', '称', '警告', '所说', '告诉', '声称', '表示', '时说', '地说', '却说', '问道',
                '写道', '答道', '感叹', '谈到', '说出', '认为', '提到', '强调', '宣称', '表明', '明确指出', '所言', '所述', '所称', '所指', '常说', '断言',
                '名言', '告知', '询问', '知道', '得知', '质问', '问', '告诫', '坚称', '辩称', '否认', '还称', '指责', '透露', '坦言', '表达', '中说',
                '中称', '他称', '地问', '地称', '地用', '地指', '脱口而出', '一脸', '直说', '说好', '反问', '责怪', '放过', '慨叹', '问起', '喊道', '写到',
                '如是说', '何况', '答', '叹道', '岂能', '感慨', '叹', '赞叹', '叹息', '自叹', '自言', '谈及', '谈起', '谈论', '特别强调', '提及', '坦白',
                '相信', '看来', '觉得', '并不认为', '确信', '提过', '引用', '详细描述', '详述', '重申', '阐述', '阐释', '承认', '说明', '证实', '揭示',
                '自述', '直言', '深信', '断定', '获知', '知悉', '得悉', '透漏', '追问', '明白', '知晓', '发觉', '察觉到', '察觉', '怒斥', '斥责', '痛斥',
                '指摘', '回答', '请问', '坚信', '一再强调', '矢口否认', '反指', '坦承', '指证', '供称', '驳斥', '反驳', '指控', '澄清', '谴责', '批评',
                '抨击', '严厉批评', '诋毁', '责难', '忍不住', '大骂', '痛骂', '问及', '阐明']


@app.route('/', methods=['GET', 'POST'])
def parse():
    if request.method == 'GET':
        return render_template('demo.html')
    news = request.form['news']
    result = search_dependency(news, related_word)
    result = json.dumps(result, ensure_ascii=False)
    if result:
        # print(result)
        return result
        # return render_template('demo.html', result=result)


if __name__ == "__main__":
    app.run(debug=True, port=8090)
