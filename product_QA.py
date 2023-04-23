from transformers import pipeline


model_name = "distilbert-base-cased-distilled-squad"
qa_pipeline = pipeline("question-answering", model=model_name, tokenizer=model_name)



# make a function to get the answer from the question
def get_answer(question, context):
    answer = qa_pipeline({
        'question': question,
        'context': context
    })
    return answer['answer']