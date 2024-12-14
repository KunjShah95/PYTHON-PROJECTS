import os
import openai

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_readme(repo_name, repo_description, repo_features, repo_usage, repo_contributors):
    # Combine all the information into a single string
    prompt = f"Repository Name: {repo_name}\nDescription: {repo_description}\nFeatures: {', '.join(repo_features)}\nUsage: {repo_usage}\nContributors: {', '.join(repo_contributors)}\n\nGenerate a README for this repository."

    # Generate the README using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": ""}
        ],
        max_tokens=1000
    )

    # Extract the generated README
    generated_readme = response.choices[0].message.content.strip()

    # Write the generated README to a file
    with open("README.md", "w") as file:
        file.write(generated_readme)

    print("README generated successfully!")

if __name__ == "__main__":
    # Get user input
    repo_name = input("Enter the repository name: ")
    repo_description = input("Enter the repository description: ")
    repo_features = input("Enter the repository features (comma-separated): ").split(",")
    repo_usage = input("Enter the repository usage instructions: ")
    repo_contributors = input("Enter the repository contributors (comma-separated): ").split(",")

    # Generate the README
    generate_readme(repo_name, repo_description, repo_features, repo_usage, repo_contributors)
