from logging import getLogger

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = getLogger("__main__").getChild(__name__)

def scoring(english,translation):
    """cos類似度を仮にスコアとして計算して出力

    Args:
        english (str): スコアを出したい翻訳した英文
        translation (str): 機械翻訳した結果の英文

    Returns:
        float: スコア
    """
    logger.info({
        'action': 'scoring',
        'status': 'run'
    })
    similarity = calculate_similarity(english, translation)
    similarity = round(similarity,1)
    logger.info({
        'action': 'scoring',
        'status': 'success'
    })
    return similarity

def preprocess_text(text):
    """cos類似度を求められるよう前処理

    Args:
        text (str): 前処理するテキスト

    Returns:
        str: 前処理されたテキスト
    """
    logger.info({
        'action': 'preprocess_text',
        'status': 'run'
    })
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha]
    logger.info({
        'action': 'preprocess_text',
        'status': 'success',
        'tokens': tokens
    })
    return ' '.join(tokens)

def calculate_similarity(text1, text2):
    """2つの文章の類似度を計算する関数
    Args:
        text1 (str): 類似度を計算する文章１
        text2 (str): 類似度を計算する文章２

    Returns:
        float: 類似度
    """
    logger.info({
        'action': 'calculate_similarity',
        'status': 'run'
    })
    
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])
    similarity = cosine_similarity(vectors)[0][1]

    logger.info({
        'action': 'calculate_similarity',
        'status': 'success'
    })
    return similarity * 100

