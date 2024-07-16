import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from reviews.service import ReviewService
from movies.service import MovieService


def show_reviews():
    review_service = ReviewService()
    reviews = review_service.get_reviews()
    
    if reviews:
        st.write('Lista de Reviews:')
        reviews_df = pd.json_normalize(reviews)
        AgGrid(
            data=reviews_df,
            # update_mode=True,
            key='reviews_grid'
        )
    else:
        st.warning('Nenhuma review encontrada.')

    st.title('Cadastrar Review')
    
    movie_service = MovieService()
    movies = movie_service.get_movies()
    
    movie_titles = {movie['title']: movie['id'] for movie in movies}
    
    selected_movie_title = st.selectbox('Filme', list(movie_titles.keys()))
    stars = st.number_input(label='Estrelas' ,min_value=0, max_value=5, step=1)
    comment = st.text_area(label='Comentário')
    
    if st.button('Cadastrar'):
        new_review = review_service.create_review(
            movie=movie_titles[selected_movie_title],
            stars=stars,
            comment=comment
        )
        if new_review:
            st.rerun()
        else:
            st.error('Erro ao cadastrar avaliaão. Verifique os campos')
