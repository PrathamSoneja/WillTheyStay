import streamlit as st
st.markdown("", unsafe_allow_html=True)

st.markdown(
    """
    <h1 style="text-align: center; color: red;">
    WillTheyStay.ai 👋
    </h1>
    
    <div style="text-align: justify">
    
     WillTheyStay.ai is an open-source web app specifically developed for companies in the Telecommunication Industry. This platform provides a service for the companies to predict the churning probability of a customer.
    
    **👈 Select the Predictor tab from the sidebar** to know whether your customer is about to leave you for someone else.
    
    </div>
    """
    , unsafe_allow_html=True
)

for i in range(17):
    st.write('')

st.caption(
    "developed &nbsp; by &nbsp; Pratham Soneja"
)