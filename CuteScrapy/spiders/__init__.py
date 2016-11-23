# coding:utf8
import re

pattern_a_s = '<a [^>]*>'
pattern_a_e = '</a>'
pattern_session_s = '<section [^>]*>'
pattern_session_e = '</section>'
pattern_div_s = '<div [^>]*>'
pattern_div_e = '</div>'
pattern_em_s = '<em [^>]*>'
pattern_em_e = '</em>'

pattern_style = '<style[^<]*</style>'
pattern_style_in = 'style="[^>]*;"'
pattern_script_s = '<script[^<]*</script>'
pattern_ins_s = '<ins[^<]*</ins>'
pattern_iframe_s = '<iframe[^<]*</iframe>'
pattern_note = '<!--[^<]*-->'
# pattern_class = 'class="[^>]*"'
# pattern_id = 'id="[^>]*"'
# pattern_par = '\w+="[^>]\d+"'
# pattern_par = '\s(?!(src|alt|href))[a-zA-Z]+(\-[a-zA-Z]+)?=[^>]*"'
pattern_par = '\s(?!(src|alt|href|\s))[a-zA-Z]+(\-[a-zA-Z]+)?="[^"]*"'
pattern_js = '\{[^};]*'


def replaceAllTag(text):
    text = text.replace('\t', '').replace('\n', '')
    text = re.sub(pattern_a_e, '', re.sub(pattern_a_s, '', text))
    text = re.sub(pattern_session_s, '', re.sub(pattern_session_e, '', text))
    text = re.sub(pattern_div_s, '', re.sub(pattern_div_e, '', text))
    text = re.sub(pattern_em_s, '', re.sub(pattern_em_e, '', text))
    text = re.sub(pattern_ins_s, '',
                  re.sub(pattern_style, '', re.sub(pattern_style_in, '', re.sub(pattern_script_s, '', text))))
    text = re.sub(pattern_note, '', re.sub(pattern_iframe_s, '', text))
    text = re.sub(pattern_par, '', text)
    # text = re.sub(pattern_js, '', text)
    return text.strip()


if __name__ == '__main__':
    text=''
    print replaceAllTag(text)