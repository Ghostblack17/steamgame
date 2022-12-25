import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_player import st_player

import matplotlib.pyplot as plt
import seaborn as sb
def main() :
    
    # streamlit 화면 비율
    st.set_page_config(layout="wide")

    st.title('Game Info & EDA \n 스팀게임에서 제공하는 게임 정보와 평점과 가격, 다운로드수에 대한 EDA페이지 입니다.')

    img1 = Image.open('data/steam_logo2.jpg')
    
    st.image(img1, width=1035)
    url = 'https://youtu.be/W-sbLEvINmk'

    st.video(url)
    st.subheader('')
    
    
    st.title('')
    st.title('Game Info')
    

    # 사이드바 이미지
    img2 = Image.open('data/steam_logo1.jpg')
    st.sidebar.image(img2, width=305)

    st.subheader('검색하신 게임을 확인하세요.')
    
    df = pd.read_csv('data/steam.csv', index_col=0)
    df = df.drop('Average_Hours-Played_Since_2009', axis=1)
    df = df.drop('Median_Hours_Played_Since_2009', axis=1)

    # 전체게임 검색
    game_serch = st.sidebar.text_input('게임 검색')
    result = df.loc[ df['Game'].str.lower().str.contains(game_serch.lower()),]

    st.dataframe(result)
    
    st.info('Metascore : 평점 / Price : 가격 / Game Type : 장르 / Game : 게임이름 / Release_date : 출시일 / Download : 다운로드 수 / Publishers : 제작사')
    st.title('')
    
    st.subheader('Game Type별 인기순위 TOP10')
    
    # 게임 타입별 인기 top10검색
    game_type_list = ['Strategy', 'Action', 'RPG', 'Adventure', 'Indie', 'Simulation','Sports']

    my_choice = st.sidebar.selectbox('TOP 10 Game Type 선택', game_type_list)
    if my_choice == game_type_list[0] :
        st.write('Stratgy 인기 TOP 10')
        st.dataframe(df.loc[df['Game_Type'] == 'Strategy'].head(10))
    elif my_choice == game_type_list[1] :
        st.write('Action 인기 TOP 10')
        st.dataframe(df.loc[df['Game_Type'] == 'Action'].head(10))
    elif my_choice == game_type_list[2] :
        st.write('RPG 인기 TOP 10')
        st.dataframe(df.loc[df['Game_Type'] == 'RPG'].head(10))
    elif my_choice == game_type_list[3] :
        st.write('Adventure 인기 TOP 10')
        st.dataframe(df.loc[df['Game_Type'] == 'Adventure'].head(10))
    elif my_choice == game_type_list[4] :
        st.write('Indie 인기 TOP 10')
        st.dataframe(df.loc[df['Game_Type'] == 'Indie'].head(10))
    elif my_choice == game_type_list[5] :
        st.write('Simulation 인기 TOP 10')
        st.dataframe(df.loc[df['Game_Type'] == 'Simulation'].head(10))
    elif my_choice == game_type_list[6] :
        st.write('Sports 인기 TOP 10')
        st.dataframe(df.loc[df['Game_Type'] == 'Sports'].head(10))

    st.info('Metascore : 평점 / Price : 가격 / Game Type : 장르 / Game : 게임이름 / Release_date : 출시일 / Download : 다운로드 수 / Publishers : 제작사')
    st.title('')
    
    # 무료게임 top100 검색
    df_free = df.loc[ df['Price'] == 0 ]
    df_free = df_free.sort_values('Download', ascending=False).head(100)
    
    free_game_serch = st.sidebar.text_input('무료게임 TOP100 검색')
    result2 = df_free.loc[ df_free['Game'].str.lower().str.contains(free_game_serch.lower()),]
    
    st.subheader('무료게임 인기 TOP 100')
    st.dataframe(result2)
    st.info('Metascore : 평점 / Price : 가격 / Game Type : 장르 / Game : 게임이름 / Release_date : 출시일 / Download : 다운로드 수 / Publishers : 제작사')
    st.title('')
    
    # 스팀게임 EDA
    st.title('EDA')
    column_list = df.columns
    column_list = st.multiselect('스팀게임 데이터 컬럼별 보기 (중복 선택 가능)', column_list)

    if len(column_list) != 0 :
        st.dataframe(df[column_list])

    st.title('')
    if st.checkbox('스팀게임의 기본 통계치입니다.') :
        st.dataframe(df.describe())
    
    if st.checkbox('게임회사별 판매중인 게임의 갯수와 평균평점보기') :
        public_meta_mean_df = df.groupby('Publishers')['Metascore'].mean().to_frame()
        public_count_game_df = df.groupby('Publishers')['Game'].count().to_frame()
        public_meta_mean_df.columns = ['MetaScore_AVG']
        public_count_game_df.columns = ['Game_CNT']
        public_cnt_avg_df = public_count_game_df.join(public_meta_mean_df)
        public_cnt_avg_df = public_cnt_avg_df.sort_values('Game_CNT', ascending=False)
        st.dataframe(public_cnt_avg_df)
    else :
        st.text('')
    
    
    col_list = df.columns[ : ]
    selected_col = st.selectbox('최대 최소 원하는 컬럼 선택', col_list)

    df_max = df.loc[df[selected_col] == df[selected_col].max(),]
    df_min = df.loc[df[selected_col] == df[selected_col].min(),]
    st.info('Metascore : 평점 / Price : 가격 / Game Type : 장르 / Game : 게임이름 / Release_date : 출시일 / Download : 다운로드 수 / Publishers : 제작사')
    st.text('{}컬럼의 최대값에 해당하는 데이터 입니다.'.format(selected_col))
    st.dataframe(df_max)
    st.text('{}컬럼의 최소값에 해당하는 데이터 입니다.'.format(selected_col))
    st.dataframe(df_min)

    selected_list = st.multiselect('컬럼들 선택', col_list)


    if len(selected_list) > 1 :
        fig1 = sb.pairplot(data=df[selected_list])
        st.pyplot(fig1)

    st.text('선택하신 컬럼끼리의 상관계수입니다.')
    st.dataframe(df[selected_list].corr())

    st.title('')
    st.title('')
    st.title('')
    st.text('데이터는 2022-05-20 기준 데이터입니다. \nReference : https://www.kaggle.com/datasets/eringray/steam-games-dataset.')


if __name__ == '__main__' :
    main()