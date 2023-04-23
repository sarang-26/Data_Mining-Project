

import streamlit as st
#from extract_transcript import speech_to_text
from extract_reviews import get_top_review
from product_QA import get_answer
st.title('Amazon Product Chatbot')

#create a streamlit text box for writing the text for the user


#create a slide bar for adding multiple drop down options
option = st.sidebar.selectbox(
    'Select the option',
    ('Top Reviews', 'Product Chatbot'))

if option == 'Top Reviews':
    url = st.text_area("Enter the url for the product")
    df=get_top_review(url)
    st.table(df)
elif option == 'Product Chatbot':
    # insert image in streamlit
    image = st.image('bert-model-calssification-output-vector-cls.png')
    description = st.text_area("Enter about this product information")
    question=st.text_area("Enter the question")
    answer=get_answer(question,description)
    st.write(answer)

    

#create a streamlit tab on the top of the page and add the options
