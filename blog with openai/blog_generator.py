# Generate a Blog with OpenAI 📝

import openai
from dotenv import dotenv_values

config = dotenv_values('.env')

openai.api_key = config['API_KEY']

def generate_blog(blog_topic):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',  # Using GPT-3.5 Turbo for better results
        messages=[
            {"role": "system", "content": "You are a professional blog writer."},
            {"role": "user", "content": f"Write a complete blog about the topic: {blog_topic}. Include an introduction, detailed body, and a conclusion."}
        ],
        max_tokens=2000,  # Increased token limit for detailed blogs
        temperature=0.3  # Adjust for creativity
    )
    retrieve_blog = response['choices'][0]['message']['content']
    return retrieve_blog

keep_writing = True

while keep_writing:
    answer = input('Would you like to generate a blog? Type "Y" for yes, anything else for no: ')
    if answer.upper() == 'Y':
        blog_topic = input('What should this blog be about? ')
        print("Generating your blog... Please wait.\n")
        print(generate_blog(blog_topic))
    else:
        keep_writing = False