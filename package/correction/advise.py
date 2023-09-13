from logging import getLogger

import spacy

logger = getLogger("__main__").getChild(__name__)

def create_advice(english, translation):
    """翻訳ミスの原因を特定して文章を生成する

    Args:
        english (str): 自分で翻訳した文章
        translation (str): 機械翻訳した文章

    Returns:
        str: 翻訳ミスの原因
    """
    logger.info({
        'action': 'create_advice',
        'status': 'run'
    })
    process_english = process_for_advice(english)
    process_translation = process_for_advice(translation)
    if process_english == process_translation:
        advice_word = 'あなたの訳はおそらく文法的に間違っています。'
    else:
        advice_word = 'あなたの訳はおそらく英単語が間違っています。'
    logger.info({
        'action': 'create_advice',
        'status': 'success'
    })
    return advice_word

def process_for_advice(text):
    """文章を前処理して重要な単語のみのセットにする

    Args:
        text (str): 前処理する文章

    Returns:
        set: 前処理された結果の単語のセット
    """
    logger.info({
        'action': 'process_for_advice',
        'status': 'run'
    })
    nlp = spacy.load('en_core_web_sm')
    # テキストの前処理を行う関数
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    logger.info({
        'action': 'process_for_advice',
        'status': 'success',
        'tokens': tokens
    })
    return set(tokens)

