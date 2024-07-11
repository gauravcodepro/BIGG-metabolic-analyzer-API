#! usr/bin/env python3
# Author Gaurav
# Date 2024-6-21
# a streamlit application for the analysis of the metabolic models from BIGG database.

import streamlit as st
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

st.set_page_config(
                 page_title="Metabolic models analyzer",
                 layout="centered",
                 initial_sidebar_state="expanded")
st.header("Metabolic models analyzer")
st.subheader("Developed by Gaurav Sablok")

help = st.button("Display the help toggle button")
if help:
    st.write("You can analyze the following from the BIGG database for the metabolic models")
    st.write("1. Metabolic reactions")
    st.write("2. Metabolites")
    st.write("3. Genes and Proteins")
metabolite = st.text_input("Please enter the metabolite present in the BIGG database")
if metabolite and st.button("analyze metabolite"):
    st.write(metabolite)
    url = f"http://bigg.ucsd.edu/universal/metabolites/{metabolite}"
    st.write(url)
    url_fetch =  urlopen(url)
    element = BeautifulSoup(url_fetch, "html.parser").find_all("div", class_="table-row")
    species = list(map(lambda n: ''.join(n).strip().split("\n"),list(map(lambda n: list(n), \
                                      list(map(lambda n: list(n)[1],[element[i]for i in
                                                                  range(len(element)) if len(element[i]) > 3]))))))
    model = list(map(lambda n: ''.join(n).strip().split("\n"),list(map(lambda n: list(n), \
                                  list(map(lambda n: list(n)[3],[element[i]for i in \
                                                                  range(len(element)) if len(element[i]) > 3]))))))
    biggid = list(map(lambda n: ''.join(n).strip().split("\n"),list(map(lambda n: list(n), \
                            list(map(lambda n: list(n)[5],[element[i]for i in \
                                                                  range(len(element)) if len(element[i]) > 3]))))))
    st.write("metabolites analyzed and please select the option below:")
    dataframe = pd.DataFrame([species, model, biggid])
    st.write(dataframe)

metabol = st.text_input("Please enter the metabolite")
model = st.text_input("Please enter the model")
if metabol and model and st.button("analyze model"):
    url = f"http://bigg.ucsd.edu/models/{metabol}/metabolites/{model}"
    url_fetch =  urlopen(url)
    subelement = BeautifulSoup(url_fetch, "html.parser").find_all("div", class_="table-row")
    biggid = [j for i in (list(map(lambda n: ''.join(n).split(">"),[list(i)[1] \
                                                    for i in subelement if len(i) > 4]))) for j in i][1:]
    biggname = [j for i in (list(map(lambda n: ''.join(n).split(">"),[list(i)[3] \
                                                for i in subelement if len(i) > 4]))) for j in i][1:]


    modeldataframe = pd.DataFrame([biggid, biggname])
    st.write("The biggid with the associated model are:")
    st.write(modeldataframe)

sequence = st.text_input("Please enter the gene name:")
sequencemodel = st.text_input("Please enter the sequence model name:")
if sequence and sequencemodel and st.button("analyze genes and proteins"):
    urlsequence = f"http://bigg.ucsd.edu/models/{sequencemodel}/genes/{sequence}"
    urlseq =  urlopen(urlsequence)
    element = BeautifulSoup(urlseq, "html.parser").find_all("p", class_= "sequence")
    dnasequence = ''.join(element[0])
    proteinsequence = ''.join(element[1])
    st.write("The associated DNA sequence is:")
    st.write(dnasequence)
    st.write("The associated protein sequence is:")
    st.write(proteinsequence)
