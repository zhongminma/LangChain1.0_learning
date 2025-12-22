from llm import llm
prompts = 'what is the color of the sun'
chunks = []
for chunk in llm.stream(prompts):
    if chunk.content:
        print(chunk.content, end='|', flush=True)
        chunks.append(chunk.content)
final_answer = "".join(chunks)
print(final_answer)

'''
this code has some improvements:
1. llm must set streaming=true 
2. for loop for chunks, chunks is a 
2. use PromptTemplate.from_template() for prompt reuse
3. use astream instead of stream for async
4. Do not use llm.astream, using chain.astream
'''