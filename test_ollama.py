import ollama

# Відповідь на простий запит
response = ollama.generate(
    model='llama3.2:3b',
    prompt='Чому небо блакитне? Відповідь одним реченням.'
)
print(response['response'])