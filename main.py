import argparse
from logging import DEBUG, FileHandler, Formatter, basicConfig, getLogger

import gradio as gr

from package.correction import advise, scoring
from package.translate import translate


def main(japanese,english):
    """UIのためのメイン関数

    Args:
        japanese (str): 翻訳する日本語の原文
        english (str): 自分で翻訳した英語の文

    Returns:
        str: 表示するためのマークダウン形式の結果の文字列
    """
    translation = translate.translate(japanese)
    score = scoring.scoring(english,translation)
    if score == 100:
        advise_=''
    else:
        advise_ = advise.create_advice(english,translation)

    if score == 100.0:
        review = '完璧です！その調子！'
    elif score >= 70.0:
        review = 'おしいです！継続して頑張ってください！'
    else:
        review = 'もう一回やってみましょう'

    return_markdown=f'''
    # Score: {score}
    ## {review}

    ***
    ### {advise_}

    ### 日本語の原文：{japanese}
    ### あなたの翻訳：{english}
    ### 　機械の翻訳：{translation}
    '''
    return return_markdown

if __name__ == '__main__':
    '''logger'''
    parser = argparse.ArgumentParser(
            description='--debug でloggerのレベルをDEBUGにする'
            )
    parser.add_argument('--debug', help='', action='store_true')
    args = parser.parse_args()
    logger = getLogger(__name__)
    if args.debug:
        basicConfig(level=DEBUG)
        formatter = Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        filehandler = FileHandler('test.log')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        
    '''main'''
    with gr.Blocks(
        title='Scoring your translation',
        theme='shivi/calm_seafoam',
        css='''
        #title_{
            text-align: center;
        }
        '''
    ) as demo:
        gr.HTML(value='''
        <h2 id="title_">Let's start your job!</h2>
        ''')
        inp1 = gr.Textbox(label='日本語',placeholder="翻訳する原文を入力してください")
        inp2 = gr.Textbox(label='英語',placeholder="翻訳してください")
        
        btn = gr.Button("Enter")
        
        out = gr.Markdown()
        
        gr.Markdown(value='''
        ***
        ## 使い方
        <br>「日本語」と書かれたテキストボックスに訳したい日本語の文章を、
        <br>「英語」と書かれたテキストボックスにあなたが訳した英語の文章を
        <br>入力してください。
        <br>            
        <br>あなたの翻訳を採点します。
        ''')
        
        inp2.submit(main, [inp1,inp2], [out])
        btn.click(main, [inp1,inp2], [out])
    demo.launch(share=False)

    #demo = gr.ChatInterface(main)

    #demo.launch(share=True)