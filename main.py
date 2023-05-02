

import streamlit as st
#from extract_transcript import speech_to_text
from extract_reviews import get_top_review, get_word_cloud, plot_sentiment
from product_QA import get_answer
st.title('Amazon Product Review Analysis')

#create a streamlit text box for writing the text for the user


#create a slide bar for adding multiple drop down options
option = st.sidebar.selectbox(
    'Select the option',
    ('Top Reviews', 'Product Chatbot'))

if option == 'Top Reviews':
    url = st.text_area("Enter the url for the product")
    if st.button('Submit'):
        df=get_top_review(url)
        tab1, tab2, tab3 = st.tabs(["🗃 Data","📈 Temporal Sentiment Analysis", "📊 Keyword Extraction"])
        tab1.subheader("Extracted Data")
        tab2.subheader("Sentiment Trend Analysis")
        tab3.subheader("Keyword Extraction")
        with tab1:

            st.table(df)
        with tab2:
            plot_sentiment(df)
        with tab3:
            get_word_cloud(df['Reviews'])

        

        

   
elif option == 'Product Chatbot':
    # insert image in streamlit
    image = st.image('bert-model-calssification-output-vector-cls.png')
    description = st.text_area("Enter about this product information")
    question=st.text_area("Enter the question")
    if st.button('Submit'):
        
        answer=get_answer(question,description)
        st.write(answer)

    
    
    

    

#create a streamlit tab on the top of the page and add the options
