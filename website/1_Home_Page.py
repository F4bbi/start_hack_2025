import streamlit as st
from utils import IMAGE_FOLDER

st.set_page_config(
    page_title="START Hack 2025 - Innovating for Land Restoration",
    page_icon="🏜️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🏜️ Innovating for Land Restoration in the Sahel - START Hack 2025")
st.image(str(IMAGE_FOLDER / "banner.jpg"), caption="UNCCD & G20 Global Land Initiative")

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

right_col.image(str(IMAGE_FOLDER / "g20.png"))
st.markdown("---")
st.markdown("""
### 🔍 How Can Data Help?
By harnessing **Earth observation data** and **geospatial technology**, we can: \\
✅ Track **land cover changes** and vegetation productivity. \\
✅ Identify **hotspots of degradation & restoration opportunities**. \\
✅ Map and analyze **climate trends & resource availability**. \\
✅ Develop **interactive dashboards** to visualize land-use patterns and inform decision-making.
""")
st.markdown("---")
st.markdown("""
## 🎯 What we have built
🔹 **Interactive Dashboards** - Data-driven insights on climate, land, and population over the last decades. \\
🔹 **Machine Learning Models** - Predicting future land cover changes and climate trends. \\
🔹 **Correlation Analysis** - Relationships between climate variables and vegetation health. \\
🔹 **Chatbot** - AI-powered assistant for land restoration queries.

Through this **hackathon**, we invite innovators to develop solutions that contribute to global land restoration, empower communities, and drive meaningful environmental change.
""")
