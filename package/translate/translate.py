from logging import getLogger

from googletrans import Translator

logger = getLogger("__main__").getChild(__name__)

def translate(japanese:str):
    """日本語を英語に機械翻訳する

    Args:
        japanese (str): 翻訳する日本語

    Returns:
        str: 機械翻訳された結果の英語
    """
    logger.info({
        'action': 'translate',
        'status': 'run'
    })
    translator = Translator()
    translation = translator.translate(japanese, src='ja', dest="en").text
    logger.info({
        'action': 'translate',
        'status': 'success'
    })
    return translation