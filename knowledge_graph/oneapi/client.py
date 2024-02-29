from openai import OpenAI

# client = OpenAI(
#     api_key="EMPTY",
#     base_url="http://127.0.0.1:8000/v1/",
# )

client = OpenAI(
    api_key="",
	base_url="https://aigptx.top/v1/",
)


def generate(model_name, prompt, system=None, template=None, context=None, options=None, callback=None):

# create a chat completion
	completion = client.chat.completions.create(
	model=model_name,
	messages=[
		{"role": "system", "content": system},
		{"role": "user", "content": prompt}]
	)
	# print the completion
	response= completion.choices[0].message.content

	return response

