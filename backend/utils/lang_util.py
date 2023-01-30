import langdetect


def check_lang(lang: str, text: str) -> bool:
    text = text.replace('<', '').replace('[', '').replace('{', '')
    text = text.replace('(', '').replace('<<', '').replace('/', '')
    try:
        curr_lang = langdetect.detect(text=text)
        if curr_lang == lang:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False
