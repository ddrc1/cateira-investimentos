from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login
from decouple import config
import json
import warnings

warnings.simplefilter("ignore")

API_TOKEN = config("API_TOKEN")
MODEL = "meta-llama/Llama-3.2-3B"#config("MODEL")
print(MODEL)
login(API_TOKEN)

model = AutoModelForCausalLM.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)

pipe = pipeline("text-generation", 
                model=model, 
                tokenizer=tokenizer, 
                device=0, 
                max_new_tokens=1024, 
                temperature=0.5, 
                top_k=5,
                repetition_penalty=1.2)

llm = HuggingFacePipeline(pipeline=pipe)

documents = []
with open("../../assets/fixtures/sub_sector.json") as file:
    json_data = json.load(file)
    for sub_sector in json_data:
        documents.append(f"{sub_sector['fields']['name']}. {sub_sector['fields']['description']}")

embedding = HuggingFaceEmbeddings()
vectorstore = FAISS.from_texts(texts=documents, embedding=embedding)
retriever = vectorstore.as_retriever()

# print(retriever.get_relevant_documents(input))

def chat(description, question):
    context = [document.page_content for document in retriever.get_relevant_documents(description)]
    template = """<s> [INST] <<SYS>>
        You are a helpful IA assistent. 
        Be concise and just include the response. 
        Answer based on the context provided. If you don't know the correct answer, say "I don't know". 
        Just include the response.
        <</SYS>>
        {context}
        Question: {question}
        Answer: [/INST]"""
    prompt = PromptTemplate(template=template, input_variables=["question", "context"])
    chain = prompt | llm
    response = chain.invoke({"question": question, "context": context})

    return response

description = "Airbnb, Inc., together with its subsidiaries, operates a platform that enables hosts to offer stays and experiences to guests worldwide. The company's marketplace connects hosts and guests online or through mobile devices to book spaces and experiences. It primarily offers private rooms, primary homes, and vacation homes. The company was formerly known as AirBed & Breakfast, Inc. and changed its name to Airbnb, Inc. in November 2010. Airbnb, Inc. was founded in 2007 and is headquartered in San Francisco, California."
input = "What sector does this company belongs to?"
print(chat(description, input))