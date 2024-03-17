import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from collections import Counter
import PyPDF2
import docx2txt

nltk.download('stopwords')

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    text = docx2txt.process(file_path)
    return text

def get_text_from_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words('portuguese'))
    words = nltk.word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return filtered_words

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def main():
    st.title('Análise Estatística de Texto')

    input_option = st.radio('Selecione o tipo de entrada de dados:', ('PDF', 'Word', 'Link da Página', 'Texto Direto'))

    if input_option == 'PDF':
        file = st.file_uploader('Carregar PDF:', type=['pdf'])
        if file is not None:
            text = extract_text_from_pdf(file)
    elif input_option == 'Word':
        file = st.file_uploader('Carregar documento Word:', type=['docx'])
        if file is not None:
            text = extract_text_from_docx(file)
    elif input_option == 'Link da Página':
        url = st.text_input('Insira o URL da página:')
        if url:
            text = get_text_from_web(url)
    else:
        text = st.text_area('Insira o texto aqui:')

    if text:
        st.subheader('Texto Analisado:')
        st.write(text)

        filtered_words = remove_stopwords(text)
        word_freq = Counter(filtered_words)
        most_common_words = word_freq.most_common(20)

        st.subheader('Top 20 Palavras Mais Frequentes (exceto stopwords):')
        for word, freq in most_common_words:
            st.write(f'{word}: {freq}')

        st.subheader('Nuvem de Palavras:')
        generate_wordcloud(' '.join(filtered_words))

if __name__ == "__main__":
    main()
