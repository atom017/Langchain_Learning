# import fitz  # PyMuPDF

# def extract_text_from_pdf(file):
#     text = ""
#     pdf_document = fitz.open(stream=file.read(), filetype="pdf")
#     for page in pdf_document:
#         text += page.get_text()
#     return text


import PyPDF2
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize the language model (ensure you have the appropriate API key set)
#llm = OpenAI(model_name="gpt-3.5-turbo")  # Use your specific model here

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to summarize text
def summarize_text(text):
    # Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)

    # Create a prompt template for summarization
    summary_prompt = PromptTemplate(
        template="Summarize the following text:\n\n{text}\n\nSummary:",
        input_variables=["text"]
    )

    # Create a summarization chain
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

    # Summarize each chunk and combine the results
    summaries = [summary_chain.run({"text": chunk}) for chunk in chunks]
    return " ".join(summaries)

# Function to answer a question based on the context
def answer_question(question, context):
    answer_prompt = PromptTemplate(
        template="Answer question politely and conversatively. {context}\n\nQuestion: {question}\nAnswer:",
        input_variables=["context", "question"]
    )
    answer_chain = LLMChain(llm=llm, prompt=answer_prompt)
    return answer_chain.run({"context": context, "question": question})

# Path to the PDF file (change this to your file path)
pdf_path = 'the-last-leaf.pdf'  # Update with your PDF file path

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Summarize the PDF content
summary = summarize_text(pdf_text)
print("Summary:\n", summary)

# Example question
question = "What is the main topic of the document?"
answer = answer_question(question, summary)
print("Answer:\n", answer)