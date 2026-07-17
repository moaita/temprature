import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="تحليل درجات الحرارة", layout="wide")
st.title("🌡️ تحليل درجات الحرارة: مصر والسعودية")

@st.cache_data
def load_data():
    return pd.read_excel('Egypt_Saudi_Temperatures.xlsx')

try:
    df = load_data()
    cities = df['City'].unique().tolist()
    selected_cities = st.sidebar.multiselect("اختر المدن:", options=cities, default=['Cairo', 'Riyadh'])
    
    filtered_df = df[df['City'].isin(selected_cities)]

    if not filtered_df.empty:
        df_melted = filtered_df.melt(id_vars=['Month', 'City'], 
                                     value_vars=['Max_Temp', 'Min_Temp'], 
                                     var_name='Type', value_name='Temperature')

        fig = px.line(
            df_melted, x='Month', y='Temperature', color='City', 
            line_dash='Type', markers=True, text='Temperature',
            title="متوسط درجات الحرارة (العظمى والصغرى)",
            labels={'Temperature': 'درجة الحرارة (°C)'}
        )
        
        fig.update_traces(textposition="top center")
        fig.update_layout(template="plotly_white")
        
        # استخدام الخاصية الجديدة width='stretch'
        st.plotly_chart(fig, width='stretch')
        
        st.subheader("جدول البيانات")
        # استخدام الخاصية الجديدة width='stretch'
        st.dataframe(filtered_df, width='stretch')
    else:
        st.warning("يرجى اختيار مدينة واحدة على الأقل.")

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الملف: {e}")