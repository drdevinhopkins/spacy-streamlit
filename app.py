import spacy
import streamlit as st
import pandas as pd
import json
import requests
import umls
from spacy.tokens import Span
from spacy import displacy

try:
    with open('umls_api.txt', 'r') as file:
        umls_apikey = file.read().replace('\n', '')
    st.write('local ', umls_apikey)
except:
    url = "https://www.dropbox.com/s/m10v41n5to4jfo8/umls_api.txt?dl=1"
    file = urllib.request.urlopen(url)

    for line in file:
        decoded_line = line.decode("utf-8")
        # print(decoded_line)
    umls_apikey = decoded_line
    st.write('dropbox ', umls_apikey)


def get_html(html: str):
    """Convert HTML so it can be rendered."""
    WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")
    return WRAPPER.format(html)


# nlp = spacy.load("en_core_sci_sm")
# doc = nlp("Past medical history includes hypertension, dyslipidemia and diabetes, and a family history of coronary artery disease.")
# visualize_ner(doc,
#               labels=nlp.get_pipe("ner").labels,
#               show_table=False
#               )

# spacy_model = 'en_core_sci_sm'

# spacy_model = st.sidebar.selectbox("Model name", ["en_core_sci_sm", "en_core_web_md"])
# nlp = load_model(spacy_model)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_model(name):
    return spacy.load(name)


spacy_model = 'en_core_sci_sm'
nlp = load_model(spacy_model)

# st.write(nlp.pipeline)

# disabled = nlp.disable_pipes(['tagger', 'parser'])

# st.write(nlp.pipeline)


def add_umls_entities(doc):
    new_ents = []
    for ent in doc.ents:
        # if ent.label_ == "PERSON" and ent.start != 0:
        #     prev_token = doc[ent.start - 1]
        #     if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
        tgt = umls.get_tgt(umls_apikey)
        cui = umls.search_by_atom(ent.text, tgt).loc[0].ui
        new_label = umls.search_by_cui(cui, tgt)[
            'semanticTypes'][0]['name']
        new_ent = Span(doc, ent.start, ent.end, label=new_label)
        new_ents.append(new_ent)
        # else:
        #     new_ents.append(ent)
    doc.ents = new_ents
    return doc


try:
    nlp.add_pipe(add_umls_entities, after='ner')
except:
    st.write('')

text = st.text_area(
    'Text', "Past medical history includes hypertension, dyslipidemia and diabetes, and a family history of coronary artery disease. He started having chest pain 4 hours ago, associated with dyspnea, nausea, and diaphoresis.")

doc = nlp(text)

# disabled.restore()
target_labels = ['Finding', 'Disease or Syndrome',
                 'Sign or Symptom', 'Pathologic Function']

# st.write(doc.ents)

# for ent in doc.ents:
#     st.write(ent.text, ' - ', ent.label_)

# data = [
#     [str(getattr(ent, attr)) for attr in ["text", "label_", "start", "end", "start_char", "end_char"]
#      ]
#     for ent in doc.ents
#     if ent.label_ in target_labels
# ]
# df = pd.DataFrame(data, columns=["text", "label_", "start", "end", "start_char", "end_char"]
#                   )
# st.dataframe(df)

html = displacy.render(
    doc, style="ent",
    options={
        "ents": ['FINDING', 'DISEASE OR SYNDROME',
                 'SIGN OR SYMPTOM', 'PATHOLOGIC FUNCTION'],
        "colors": {'FINDING': '#D0ECE7', 'DISEASE OR SYNDROME': '#D6EAF8',
                   'SIGN OR SYMPTOM': '#E8DAEF', 'PATHOLOGIC FUNCTION': '#FADBD8'}
        # DAF7A6
    }
)
style = "<style>mark.entity { display: inline-block }</style>"
st.write(f"{style}{get_html(html)}", unsafe_allow_html=True)


# visualize_ner(doc,
#               #   labels=nlp.get_pipe("ner").labels,
#               labels=['ENTITY'],
#               show_table=True,
#               )

# tgt = umls.get_tgt()

# cui_text = st.text_input('CUI Text', 'chest pain')

# search_cui = umls.search_by_atom(cui_text, tgt).loc[0].ui

# st.write(search_cui)

# st.write(umls.search_by_cui(search_cui, tgt)['semanticTypes'][0]['name'])

# st.write(umls.cui_to_atoms(search_cui, tgt))
