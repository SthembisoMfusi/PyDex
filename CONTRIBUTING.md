# Contributing to PyDex

Thank you for your interest in contributing to PyDex! This project is designed to be beginner-friendly and help people learn how to contribute to open source projects.

## Getting Started

### 1. Fork the Repository

1. Go to the [PyDex repository](https://github.com/YOUR-USERNAME/PyDex)
2. Click the "Fork" button in the top right corner
3. This creates a copy of the repository in your GitHub account

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/PyDex.git
cd PyDex
```

### 3. Set Up the Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Test that everything works
python pokedex.py pikachu
```

### 4. Create a New Branch

```bash
git checkout -b my-new-feature
```

**Branch naming conventions:**
- `feature/display-height-weight` - for new features
- `bugfix/error-handling` - for bug fixes
- `docs/update-readme` - for documentation changes

## Making Changes

### 1. Choose an Issue

Look for issues labeled with:
- `good first issue` - Perfect for beginners
- `hackathon` - Issues created specifically for this hackathon
- `help wanted` - Issues that need community help

### 2. Make Your Changes

- Write clean, readable code
- Add comments to explain complex logic
- Test your changes thoroughly
- Follow the existing code style

### 3. Test Your Changes

```bash
# Test with different Pokémon
python pokedex.py pikachu
python pokedex.py charizard
python pokedex.py ditto

# Test error cases
python pokedex.py fake-pokemon
python pokedex.py
```

## Submitting Your Changes

### 1. Commit Your Changes

```bash
git add .
git commit -m "Add descriptive commit message"
```

**Commit message guidelines:**
- Use present tense: "Add feature" not "Added feature"
- Be descriptive: "Add height and weight display" not "Update code"
- Keep it under 50 characters for the subject line

### 2. Push to Your Fork

```bash
git push origin my-new-feature
```

### 3. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the pull request template
5. Submit the pull request

## Pull Request Guidelines

### Title
- Be descriptive: "Add height and weight display for Pokémon"
- Include the issue number: "Add height and weight display (#123)"

### Description
- Explain what your changes do
- Reference the issue you're fixing: "Fixes #123"
- Include screenshots if applicable
- List any testing you did

### Example Pull Request Description

```markdown
## Description
This PR adds height and weight display to the Pokémon information output.

## Changes
- Added height and weight fields to the display output
- Height is displayed in decimeters, weight in hectograms (as per PokéAPI)
- Added proper formatting for the new fields

## Testing
- Tested with multiple Pokémon (Pikachu, Charizard, Snorlax)
- Verified output formatting looks correct
- Tested error handling for invalid Pokémon names

Fixes #123
```

## Code Style Guidelines

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions
- Keep lines under 80 characters when possible

### Example Code Style

```python
def fetch_pokemon_data(pokemon_name):
    """
    Fetch Pokémon data from the PokéAPI.
    
    Args:
        pokemon_name (str): The name of the Pokémon to look up
        
    Returns:
        dict: The Pokémon data from the API
        
    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()
```

## Getting Help

### If You're Stuck

1. **Check existing issues** - Someone might have asked the same question
2. **Ask in the issue** - Comment on the issue you're working on
3. **Create a new issue** - If you can't find an existing one
4. **Join our discussions** - Use GitHub Discussions for general questions

### Common Issues

**"I can't find the issue I want to work on"**
- Look for issues labeled `good first issue`
- Check if the issue is assigned to someone else
- Ask in the issue comments if it's still available

**"My code doesn't work"**
- Make sure you've installed the requirements: `pip install -r requirements.txt`
- Check for typos in Pokémon names (they're case-insensitive)
- Test with a simple Pokémon like "pikachu" first

**"I don't understand the code"**
- Start with the simplest issues (like adding height/weight display)
- Read the existing code to understand the structure
- Ask questions in the issue comments

## Recognition

Contributors will be recognized in:
- The project's README.md
- Release notes
- GitHub's contributor graph

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## Questions?

If you have any questions about contributing, please:
1. Check this document first
2. Look at existing issues and discussions
3. Create a new issue with the "question" label
4. Join our community discussions

Happy contributing! 🎉
