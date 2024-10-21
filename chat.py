import streamlit as st

def arquivoConf(nome_arquivo, extensao="toml"):
    import os
    
    arquivo_local = nome_arquivo.replace('.toml', '.local.toml')

    if os.path.isfile(arquivo_local):
        return arquivo_local
    else:
        return nome_arquivo
    
def conf():
    import toml

    dados = []

    caminho_arquivo_tom = arquivoConf('.streamlit/secrets.toml')

        # Ler o arquivo TOM
    with open(caminho_arquivo_tom, 'r') as arquivo:
        dados = toml.load(arquivo)
    return dados

def chat():
    from pandasai import SmartDataframe
    from pandasai.llm.openai import OpenAI
    import matplotlib.pyplot as plt
    import os

    if "prompt_history" not in st.session_state:
        st.session_state.prompt_history = []
        #chat.response = "Digite uma pergunta, por exemplo 'Qual o melhor estudante?' "
        #st.session_state.prompt_history.append(chat)


    with st.form("Question"):
        question = st.text_input(("Digite aqui uma pergunta sobre os dados"), value="", type="default")
        chat.question = question
        submitted = st.form_submit_button(("Gerar"))
        if submitted:
            with st.spinner():
                llm = OpenAI(api_token=conf()['key'])
                pandas_ai = SmartDataframe("./assets/demo.csv", config={
                      "llm": llm, 
                    "conversational": False, 
                    "enable_cache": True,
                })

                x = pandas_ai.chat(question)

                if os.path.isfile('exports/charts/temp_chart.png'):
                    im = plt.imread('exports/charts/temp_chart.png')
                    chat.img = im
                    st.image(im)
                    os.remove('exports/charts/temp_chart.png')

                if x is not None:
                    chat.response = x
                    st.write(x)

                st.session_state.prompt_history.append(chat)
    

        st.subheader(("Prompt history:"))
        flag = False
        for elemento in reversed(st.session_state.prompt_history):
            if flag == False:
                flag = True
                continue
            if hasattr(elemento, 'question') and elemento.question:
                st.markdown(
                f"<p style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: right;'> {elemento.question}</p>",  unsafe_allow_html=True
                )

            if hasattr(elemento, 'img'):
                st.image(elemento.img)

            if hasattr(elemento, 'response') and elemento.response:
                st.markdown(
                    f"<p style='border: 1px solid #ccc; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: left;'> {elemento.response}</p>",  unsafe_allow_html=True
                )
                                   
           
            
        

        if "prompt_history" in st.session_state.prompt_history and len(st.session_state.prompt_history) > 0:
            if st.button(("Limpar")):
                st.session_state.prompt_history = []


st.header("Chat")
chat()

