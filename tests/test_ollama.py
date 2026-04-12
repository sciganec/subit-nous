import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {"role": "system", "content": "You are a text editor. Change the perspective from WE to ME. Output only the rewritten text."},
        {"role": "user", "content": "We recommend this product."}
    ],
    options={"temperature": 0.3}
)

print(response['message']['content'])