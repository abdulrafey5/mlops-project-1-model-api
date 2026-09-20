from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("I love building MLOps pipelines!")
print(result)