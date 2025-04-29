# The Austen Experience

A Python-based interactive story creator that generates Regency-era romance stories in the style of Jane Austen. This application allows users to create custom stories with unique characters, settings, and themes.

## Features

- Create custom Regency-era romance stories
- Character customization (Heroine and Hero)
- Multiple story themes (Romance, Drama, Mystery, Comedy, Tragedy)
- Interactive story generation
- Text-to-speech narration
- Background music for different themes
- PDF export capability
- Modern GUI with themed interface
- Typewriter effect for story display

## Requirements

- Python 3.7 or higher
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. In the application:
   - Fill in character details for both Heroine and Hero
   - Select a theme and setting for your story
   - Click 'Generate Story' to create your tale
   - Use the controls to:
     - Read the story aloud
     - Export to PDF
     - Toggle background music
     - Clear the story

## Project Structure

- `main.py` - Main application file
- `data/` - Directory containing story elements
  - `characters.json` - Character traits and statuses
  - `settings.json` - Story settings and locations
  - `plots.json` - Plot elements and templates
- `images/` - Background images for different themes
- `music/` - Background music files for different themes

## Settings

The application includes customizable settings for:
- Font size
- Application theme
- Voice speed
- Music preferences

## Help

The application includes a comprehensive help section with:
- Getting started guide
- Character creation tips
- Story elements explanation
- Controls overview

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the works of Jane Austen
- Uses various open-source libraries (see requirements.txt) 