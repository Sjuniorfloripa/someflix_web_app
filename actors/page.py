import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from actors.service import ActorService
import pandas as pd
from datetime import datetime


def show_actors():
    actor_service = ActorService()
    actors = actor_service.get_actors()
    
    if actors:
        st.write('Lista de Atores & Atrizes:')
        actors_df = pd.json_normalize(actors)
        AgGrid(
            data=actors_df,
            # update_mode=True,
            key='actors_grid'
        )
    else:
        st.warning('Nenhum Ator/Atriz encontrado.')
    
    st.title('Cadastrar novo(a) Ator/Atriz')
    name = st.text_input('Nome do(a) Ator/Atriz')
    birthday = st.date_input(
        label='Data de nascimento',
        value=datetime.today(),
        min_value=datetime(1600,1,1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY'
    )
    nationality_dropdown = ['USA', 
                            'BRAZIL', 
                            'CANADA', 
                            'MEXICO', 
                            'ISRAEL', 
                            'UK', 
                            'AUSTRALIA', 
                            'FRANCE', 
                            'SPAIN']
    nationality = st.selectbox(label='Nacionalidade', options=nationality_dropdown)
    
    if st.button('Cadastrar'):
        new_actor = actor_service.create_actor(
            name=name,
            birthday=birthday,
            nationality=nationality,
        )
        if new_actor:
            st.rerun()
        else:
            st.error('Erro ao cadastrar o(a) Ator/Atriz. Verifique os campos.')
