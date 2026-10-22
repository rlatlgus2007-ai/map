import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math

# 웹 앱의 제목을 설정합니다.
st.title("부산 지하철 이용객 수 지도 분석")

# 1. CSV 파일 업로드 기능 만들기
uploaded_file = st.file_uploader("busan_subway.csv 파일을 올려주세요", type=['csv'])

# 파일이 정상적으로 업로드 되었을 때만 아래 코드를 실행합니다.
if uploaded_file is not None:
    # 판다스를 이용해 업로드된 CSV 파일을 읽어옵니다.
    df = pd.read_csv(uploaded_file)

    # ----------------------------------------------------
    # [새로운 기능 1] 호선 필터 (multiselect)
    # ----------------------------------------------------
    # 데이터에 있는 호선 목록을 중복 없이 가져옵니다.
    line_list = df['호선'].unique()

    # 사용자가 원하는 호선만 고를 수 있게 다중 선택창을 만듭니다. (기본값은 전체 선택)
    selected_lines = st.multiselect("지도로 확인할 호선을 선택하세요:", line_list, default=line_list)

    # 사용자가 선택한 호선만 남기도록 데이터를 걸러냅니다.
    filtered_df = df[df['호선'].isin(selected_lines)]

    # ----------------------------------------------------
    # [새로운 기능 2] 이용객 상위 5개 역 표로 표시
    # ----------------------------------------------------
    st.subheader("🏆 이용객 수 상위 5개 역")
    # '이용객수'를 기준으로 내림차순(큰 순서대로) 정렬한 뒤 위에서 5개만 뽑습니다.
    top5_df = filtered_df.sort_values(by='이용객수', ascending=False).head(5)
    st.dataframe(top5_df)

    # ----------------------------------------------------
    # [새로운 기능 3] 지도 그리기 & 호선별 색상 지정
    # ----------------------------------------------------
    st.subheader("🗺️ 부산 지하철 역별 이용객 수 지도")

    # folium 지도 만들기 (부산 중심부 좌표 기준)
    m = folium.Map(location=[35.1795, 129.0756], zoom_start=11)


    # 호선 이름에 따라 색상을 정해주는 아주 간단한 함수를 만듭니다.
    def get_color(line):
        line_str = str(line)  # 숫자로 되어있을 수도 있어서 글자로 바꿉니다.
        if '1' in line_str:
            return 'orange'  # 1호선은 주황
        elif '2' in line_str:
            return 'green'  # 2호선은 초록
        elif '3' in line_str:
            return 'brown'  # 3호선은 갈색
        elif '4' in line_str:
            return 'blue'  # 4호선은 파랑
        else:
            return 'gray'  # 나머지는 회색


    # 이제 '전체 데이터(df)'가 아닌 '필터링된 데이터(filtered_df)'로 지도를 그립니다!
    for index, row in filtered_df.iterrows():
        # 면적이 비례하도록 반지름 계산 (크기 조절을 위해 10으로 나눔)
        radius_size = math.sqrt(row['이용객수']) / 10

        # 위에서 만든 get_color 함수를 써서 호선에 맞는 색을 가져옵니다.
        line_color = get_color(row['호선'])

        # 지도에 마커를 추가합니다.
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=radius_size,
            color=line_color,  # 테두리 색상을 호선 색으로 지정
            fill=True,
            fill_color=line_color,  # 원 안쪽 색상도 호선 색으로 지정
            fill_opacity=0.6,
            tooltip=row['역명'],  # 마우스를 올리면 역명 표시
            popup=f"{row['이용객수']}명"  # 클릭하면 이용객수 표시
        ).add_to(m)

    # 스트림릿 화면에 완성된 지도를 띄워줍니다.
    st_folium(m, width=700, height=500)

else:
    # 파일을 올리지 않았을 때 보여줄 안내 문구입니다.
    st.info("데이터 분석을 시작하려면 CSV 파일을 업로드해주세요!") 