# Storybook Prompt Generator

A Python script that analyzes journal entries and generates a Pixar-style children's story based on the emotional content of the entries.

## Features

- Analyzes journal entries for emotional content using both VADER sentiment analysis and keyword matching
- Generates a story arc based on the emotional patterns in the entries
- Uses OpenAI's GPT-3.5 to create a Pixar-style children's story in first person
- Outputs both the emotional analysis and the generated story to a text file

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/storybook-prompt-generator.git
cd storybook-prompt-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Create a CSV file named `journal_entries.csv` with two columns:
   - `date`: The date of the entry
   - `entry_text`: The text content of the entry

## Usage

Run the script:
```bash
python generate_story.py
```

The script will:
1. Read the journal entries from `journal_entries.csv`
2. Analyze the emotional content of each entry
3. Generate a story arc based on the emotional patterns
4. Create a Pixar-style children's story using GPT-3.5
5. Save the results to `weekly_story.txt`

## Output

The `weekly_story.txt` file will contain:
- Emotional analysis of each journal entry
- The generated story arc
- The final Pixar-style children's story

## Requirements

- Python 3.6+
- pandas
- nltk
- openai

## License

MIT License 