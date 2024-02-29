import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import folium
from streamlit_folium import folium_static


# Load the data
df_jkk = pd.read_csv('df_jkk_2023.csv', sep=';')
geojson = "indonesia.geojson"
df_kk = pd.read_csv('data_kasus.csv', sep=';')
df_peserta = pd.read_csv('data_peserta_bpjstk.csv', sep=';')

province_centroids = {
    "Aceh": (4.695135, 96.7493993),
    "Sumatera Utara": (2.1153547, 99.5450974),
    "Sumatera Barat": (-0.7399397, 100.8000051),
    "Riau": (0.2933469, 101.7068294),
    "Jambi": (-1.4851831, 102.4380581),
    "Sumatera Selatan": (-3.3194374, 103.914399),
    "Bengkulu": (-3.5778471, 102.3463875),
    "Lampung": (-4.5585849, 105.4068079),
    "Kepulauan Bangka Belitung": (-2.7410513, 106.4405872),
    "Kepulauan Riau": (3.9456514, 108.1428669),
    "DKI Jakarta": (-6.211544, 106.845172),
    "Jawa Barat": (-7.090911, 107.668887),
    "Jawa Tengah": (-7.150975, 110.1402594),
    "DI Yogyakarta": (-7.8753849, 110.4262088),
    "Jawa Timur": (-7.5360639, 112.2384017),
    "Banten": (-6.4058172, 106.0640179),
    "Bali": (-8.4095178, 115.188916),
    "Nusa Tenggara Barat": (-8.6529334, 117.3616476),
    "Nusa Tenggara Timur": (-8.6573819, 121.0793705),
    "Kalimantan Barat": (-0.2787808, 111.4752851),
    "Kalimantan Tengah": (-1.6814878, 113.3823545),
    "Kalimantan Selatan": (-3.0926415, 115.2837585),
    "Kalimantan Timur": (1.6406296, 116.419389),
    "Sulawesi Utara": (0.6246932, 123.9750018),
    "Sulawesi Tengah": (-1.4300254, 121.4456179),
    "Sulawesi Selatan": (-3.6687994, 119.9740534),
    "Sulawesi Tenggara": (-4.14491, 122.174605),
    "Gorontalo": (0.6999372, 122.4467238),
    "Sulawesi Barat": (-2.8441371, 119.2320784),
    "Maluku": (-3.2384616, 130.1452734),
    "Maluku Utara": (1.5709993, 127.8087693),
    "Papua Barat": (-1.3361154, 133.1747162),
    "Papua": (-4.269928, 138.0803529)
}

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title('Analisis Korelasi: Kecelakaan Kerja dan Jumlah Peserta BPJSTK di Indonesia Berdasarkan Jenis Kepesertaan')
st.markdown('**Tahun 2023**')

col1, col2, col3 = st.columns([1, 1, 1])  # Adjust width as needed

with col1:
    total_kasus = int(df_jkk['total_kasus'].sum())
    st.metric(label="Total Kasus", value=f"{total_kasus:,} kasus")

with col2:
    total_klaim = round(df_jkk['total_klaim'].sum() / 1e12, 2) 
    st.metric(label="Total Klaim", value=f"Rp {total_klaim} T")

with col3:
    total_peserta = round(df_peserta['total_peserta'].sum() / 1e6, 2)
    st.metric(label="Jumlah Peserta BPJSTK", value=f"{total_peserta} juta jiwa")


st.write('')  

col4, col5 = st.columns([2, 2])


with col4:
    st.caption('Data terbaru dari BPJS Ketenagakerjaan menunjukkan kenaikan signifikan insiden kecelakaan kerja selama lima tahun terakhir. Peningkatan ini terutama terlihat pada tahun 2023, dengan kasus-kasus yang terjadi akhir-akhir ini menjadi perhatian utama, termasuk kasus ledakan smelter beberapa bulan lalu yang mengakibatkan korban jiwa dan luka-luka. ')

#Line Chart
with col5:

    st.subheader('Trend Jumlah Kasus Kecelakaan di Indonesia (2018-2023)')
    line_chart = alt.Chart(df_kk).mark_line(point=True).encode(
        x=alt.X('tahun:O', title='Tahun'), 
        y=alt.Y('jumlah_kasus:Q', title='Jumlah Kasus') 
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
        labelAngle=0
    )

    st.altair_chart(line_chart, use_container_width=True)


st.subheader('Persebaran Jumlah Kasus Kecelakaan di Indonesia')

#Choropleth Map
m = folium.Map(location=[-2.5, 117], zoom_start=5, tiles='OpenStreetMap',attr='Map data © OpenStreetMap contributors')


choropleth = folium.Choropleth(
    geo_data=geojson,
    data=df_jkk,
    columns=['provinsi', 'total_kasus'],
    key_on='feature.properties.state',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Kasus Kecelakaan Kerja',
    highlight=True,
    smooth_factor=0,
).add_to(m)

for province, centroid in province_centroids.items():
    if province in df_jkk['provinsi'].values:
        total_kasus = int(df_jkk.loc[df_jkk['provinsi'] == province, 'total_kasus'].values[0])
        popup_content = f"Provinsi: {province}  Jumlah Kasus: {total_kasus}"
        folium.Marker(
            location=centroid,
            popup=folium.Popup(popup_content, parse_html=True),
            icon=None
        ).add_to(m)


folium.LayerControl().add_to(m)


folium_static(m, width=1280)

st.write(' ')

st.subheader('Distribusi Kasus Kecelakaan Kerja di Indonesia')


caption = """
Persebaran jumlah kasus kecelakaan kerja berdasarkan jenis kepesertaan BPJS pada tiap provinsi digambarkan melalui peta dan diagram batang. Terlihat pada peta bahwa semakin biru warna pada suatu provinsi, maka semakin tinggi jumlah kasus keecelakaan kerja yang terjadi di daerah tersebut. Sedangkan, semakin kuning warna pada peta maka semakin rendah jumlah kasus kecelakaan kerja pada provinsi tersebut. Dalam hal ini, provinsi Jawa Barat, Jawa Timur, dan Jawa Tengah memiliki jumlah kasus kecelakaan kerja tertinggi di Indonesia pada tahun 2023. Dengan menggunakan diagram batang di samping, terlihat bahwa pada ketiga provinsi tersebut, kasus kecelakaan kerja kebanyakan dialami oleh golongan penerima upah. Hal ini berarti bahwa penerima upah merupakan kelompok yang paling rentan terhadap kecelakaan kerja di ketiga provinsi tersebut.
"""

#Bar Chart
col6, col7 = st.columns([5,3])  
with col6:
    selected_province = st.selectbox('Pilih Provinsi', df_jkk['provinsi'].unique(), key='selectbox')
    df_selected_province = df_jkk[df_jkk['provinsi'] == selected_province]

    
    data = {
        'Kategori': ['kasus_pu', 'kasus_bpu', 'kasus_jakon'],
        'Jumlah Kasus': [
            df_selected_province['kasus_pu'].values[0],
            df_selected_province['kasus_bpu'].values[0],
            df_selected_province['kasus_jakon'].values[0]
        ]
    }
    df_selected_province_melted = pd.DataFrame(data)

    
    bar_chart = alt.Chart(df_selected_province_melted).mark_bar().encode(
        x=alt.X('Kategori:N', title='Kategori'),
        y=alt.Y('Jumlah Kasus:Q', title='Jumlah Kasus'),
        color='Kategori:N',
        tooltip=['Kategori:N', alt.Tooltip('Jumlah Kasus:Q', title='Jumlah Kasus')]
    ).properties(
        title=f'Provinsi {selected_province}',
        width=800,  
        height=400  
    ).configure_axisX(labelAngle=0)
    st.write(bar_chart, use_container_width=True)
with col7:
    st.caption(caption)


#Pie Chart
jumlah_peserta = df_peserta[['peserta_pu', 'peserta_bpu', 'peserta_jakon']].sum()
total_peserta = jumlah_peserta.sum()
data_pie = pd.DataFrame({
    'Jenis Kepesertaan': ['Penerima Upah', 'Bukan Penerima Upah', 'Jasa Konstruksi'],
    'Jumlah Peserta': jumlah_peserta.values,
    'Persentase': (jumlah_peserta / total_peserta * 100).round(2).astype(str) + '%'
})

st.write(' ')
st.write(' ')
col8, col9 = st.columns([4,3])  

with col8:
    st.caption('Pada proporsi jumlah peserta BPJSTK di Indonesia yang digambarkan dengan diagram pie di samping, terlihat bahwa golongan Penerima Upah (PU) memiliki porsi terbesar, mencapai 60.16%, dibandingkan dengan golongan Bukan Penerima Upah (BPU) yang memiliki persentase sebesar 22.12% dan golongan Jasa Konstruksi (Jakon) sebesar 17.72%. Analisis proporsi peserta BPJSTK ini mencerminkan dominasi sektor formal dalam kepesertaan program, yang menggambarkan signifikansi kontribusi para pekerja penerima upah dalam perlindungan ketenagakerjaan. ')
with col9:
    pie_chart = alt.Chart(data_pie).mark_arc().encode(
        color=alt.Color('Jenis Kepesertaan:N', legend=alt.Legend(title="Jenis Kepesertaan")),
        tooltip=['Jenis Kepesertaan:N', 'Jumlah Peserta:Q', 'Persentase:O'],
        theta='Jumlah Peserta:Q',
        radius=alt.value(100),
        text='Persentase:N'
    ).properties(
        width=500,
        height=600,
        title='Proporsi Jumlah Peserta BPJS Ketenagakerjaan'
    )
    st.write(pie_chart)

#Scatter plot
data_merged = pd.merge(df_peserta, df_jkk, on='provinsi', how='inner')

data_merged['proporsi_bpjstk'] = (data_merged['peserta_pu'] + data_merged['peserta_bpu'] + data_merged['peserta_jakon']) / data_merged['total_kasus']

#Regresi linear
m, b = np.polyfit(data_merged['proporsi_bpjstk'], data_merged['total_kasus'], 1)
data_regression = pd.DataFrame({'proporsi_bpjstk': data_merged['proporsi_bpjstk'],
                                'total_kasus': m * data_merged['proporsi_bpjstk'] + b})


brush = alt.selection_interval()

scatter_plot = alt.Chart(data_merged).mark_circle(color='blue', size=60).encode(
    x=alt.X('proporsi_bpjstk', title='Proporsi Peserta BPJS Ketenagakerjaan'),
    y=alt.Y('total_kasus', title='Total Kasus Kecelakaan Kerja'),
    tooltip=['proporsi_bpjstk', 'total_kasus'],
    color=alt.condition(brush, alt.value('steelblue'), alt.value('grey'))
).add_params(brush)



regression_line = alt.Chart(data_regression).mark_line(color='yellow').encode(
    x='proporsi_bpjstk',
    y='total_kasus'
)


chart=alt.layer(scatter_plot, regression_line).properties(
    title='Korelasi antara Proporsi Peserta BPJS Ketenagakerjaan dan Total Kasus Kecelakaan Kerja'
)


st.altair_chart(chart, use_container_width=True)

st.caption('Hasil korelasi menunjukkan bahwa terdapat korelasi negatif antara proporsi peserta aktif BPJS Ketenagakerjaan dengan total kasus kecelakaan kerja di setiap provinsi. Interpretasi dari korelasi ini adalah semakin tinggi proporsi peserta aktif BPJS Ketenagakerjaan di suatu provinsi, semakin rendah tingkat kecelakaan kerja cenderung terjadi di provinsi tersebut. Meskipun korelasi negatif, nilai korelasi yang negatif ini menunjukkan bahwa hubungan antara kedua variabel tersebut tidak terlalu kuat. Hal ini menunjukkan adanya indikasi bahwa program BPJS Ketenagakerjaan mungkin memiliki dampak positif dalam mengurangi risiko kecelakaan kerja di provinsi-provinsi di Indonesia, meskipun efeknya tidak cukup kuat untuk menghasilkan korelasi yang sangat tinggi. Dalam hal ini, analisis lebih lanjut dan evaluasi mendalam tentang implementasi dan efektivitas program BPJS Ketenagakerjaan di masing-masing provinsi dapat memberikan wawasan yang lebih mendalam.')

st.header("Kesimpulan:", divider='rainbow')
st.markdown("1. Data BPJS Ketenagakerjaan menunjukkan peningkatan signifikan insiden kecelakaan kerja selama lima tahun terakhir, terutama pada tahun 2023, dengan beberapa kasus penting seperti ledakan smelter yang menyita perhatian. Hal ini menyoroti perlunya upaya lebih lanjut dalam meningkatkan kesadaran akan keselamatan kerja dan perlindungan tenaga kerja di berbagai sektor industri.")
st.markdown("2. Analisis persebaran kasus kecelakaan kerja di Indonesia pada tahun 2023 menunjukkan bahwa provinsi Jawa Barat, Jawa Timur, dan Jawa Tengah memiliki jumlah kasus tertinggi, dengan mayoritas kasus dialami oleh golongan penerima upah. Temuan ini menunjukkan perlunya pengawasan dan penegakan regulasi yang lebih ketat di sektor-sektor ini guna mencegah terjadinya kecelakaan kerja yang serupa di masa depan.")
st.markdown("3. Selain itu, proporsi peserta BPJS Ketenagakerjaan yang didominasi oleh sektor formal, khususnya golongan penerima upah, menunjukkan pentingnya peran BPJS dalam memberikan perlindungan sosial bagi pekerja. Namun, masih dibutuhkan upaya lebih lanjut untuk meningkatkan aksesibilitas dan efektivitas program ini bagi seluruh masyarakat, terutama bagi pekerja di sektor informal.")
st.markdown("4. Hasil korelasi yang menunjukkan hubungan negatif antara proporsi peserta aktif BPJS Ketenagakerjaan dan total kasus kecelakaan kerja di setiap provinsi, meskipun berkorelasi negatif, memberikan indikasi awal bahwa program BPJS Ketenagakerjaan mungkin memberikan kontribusi dalam mengurangi risiko kecelakaan kerja di Indonesia. Oleh karena itu, perlu dilakukan evaluasi terus-menerus terhadap implementasi program ini guna memastikan efektivitasnya dalam melindungi tenaga kerja.")
st.markdown("5. Diperlukan analisis lebih lanjut untuk mengevaluasi efektivitas program BPJS Ketenagakerjaan dan memahami dampaknya secara lebih mendalam di tingkat provinsi.")
