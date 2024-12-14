# GitHub README Generator

This project is a simple Python script that generates a README file for a GitHub repository using the OpenAI API.

## Features

- Generates a README file based on user input.
- Uses the OpenAI API to create a well-formatted and informative README.

## Usage

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/github-readme-generator.git
   cd github-readme-generator
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:

   - Create an environment variable `OPENAI_API_KEY` with your OpenAI API key.
   - Alternatively, you can set the API key directly in the `main.py` file.

4. Run the script:

   ```sh
   python main.py
   ```

5. Follow the prompts to enter the repository details.

## Example

```sh
Enter the repository name: my-repo
Enter the repository description: A sample repository for generating README files.
Enter the repository features (comma-separated): Feature 1, Feature 2, Feature 3
Enter the repository usage instructions: To use this repository, clone it and run the script.
Enter the repository contributors (comma-separated): John Doe, Jane Smith
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
