import streamlit as st

st.set_page_config(
    page_title="Sahel Desert Visualizer",
    page_icon="🏜️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏜️ Innovating for Land Restoration in the Sahel")
st.image("static/images/banner.jpg", caption="UNCCD & G20 Global Land Initiative")

st.markdown("""
The **G20 Global Land Initiative**, launched by the **United Nations Convention to Combat Desertification (UNCCD)**, aims to halt and restore **50% of land degradation by 2040**. The goal is to promote sustainable land management, combat desertification, and foster climate resilience by leveraging **Earth observation data, geospatial insights, and technology**.
""")
st.markdown("---")
left_col, right_col = st.columns(2)
left_col.markdown("""
## 📍 The Challenge
The **Sahel region** is facing severe environmental and socio-economic challenges:
- **Land degradation & desertification** due to climate change and unsustainable practices.
- **Resource conflicts** among farmers, herders, and pastoralist groups over scarce land and water.
- **Urban expansion** influencing vegetation patterns and ecosystem health.
""")

right_col.image("static/images/g20.png")
st.markdown("---")
st.markdown("""
### 🔍 How Can Data Help?
By harnessing **Earth observation data** and **geospatial technology**, we can: \\
✅ Track **land cover changes** and vegetation productivity. \\
✅ Identify **hotspots of degradation & restoration opportunities**. \\
✅ Map and analyze **climate trends & resource availability**. \\
✅ Develop **interactive dashboards** to visualize land-use patterns and inform decision-making. \\
""")
st.markdown("---")
st.markdown("""
## 🎯 What we have built
🔹 **Interactive Dashboards** - Data-driven insights on land cover change over the past two decades.  
🔹 **Country Profiles** - In-depth analysis of national and sub-national land trends.  
🔹 **Trend Identification** - Detecting key patterns in vegetation productivity, land degradation, and recovery.  
🔹 **Restoration Strategies** - Tailored recommendations for policymakers and stakeholders.  

Through this **hackathon**, we invite innovators to develop solutions that contribute to global land restoration, empower communities, and drive meaningful environmental change.
""")
