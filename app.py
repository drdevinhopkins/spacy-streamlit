# import spacy
from spacy_streamlit import visualize_ner

# nlp = spacy.load("en_core_sci_sm")
# doc = nlp("Past medical history includes hypertension, dyslipidemia and diabetes, and a family history of coronary artery disease.")
# visualize_ner(doc,
#               labels=nlp.get_pipe("ner").labels,
#               show_table=False
#               )


import streamlit as st
from spacy_streamlit import load_model

spacy_model = 'en_core_sci_sm'
# spacy_model = st.sidebar.selectbox("Model name", ["en_core_sci_sm", "en_core_web_md"])
nlp = load_model(spacy_model)

text = "Past medical history includes hypertension, dyslipidemia and diabetes, and a family history of coronary artery disease."

doc = nlp(text)

st.write(doc.ents)

visualize_ner(doc,
              labels=nlp.get_pipe("ner").labels,
              show_table=False
              )
