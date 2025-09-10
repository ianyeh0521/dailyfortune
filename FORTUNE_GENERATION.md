# Fortune Generation Guide

This guide explains how to generate approximately 1000 fortune sentences using the OpenAI API.

## Prerequisites

1. **OpenAI API Key**: You need an OpenAI API key with available credits
2. **Python Dependencies**: Install the required package

## Setup

1. Install the OpenAI package:
   ```bash
   pip install openai==1.52.0
   ```

2. Set your OpenAI API key as an environment variable:
   
   **Windows:**
   ```bash
   set OPENAI_API_KEY=your_api_key_here
   ```
   
   **Linux/Mac:**
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

## Running the Generator

1. Navigate to the project directory
2. Run the generation script:
   ```bash
   python generate_fortunes.py
   ```

## What the Script Does

- Generates approximately 1000 unique fortune sentences across 8 categories:
  - encouraging
  - motivational
  - general
  - wisdom
  - success
  - happiness
  - courage
  - inspiration

- Creates the following files:
  - `generated_fortunes.json` - New fortunes only
  - `fortunes.json.backup` - Backup of your original fortunes
  - `fortunes.json` - Updated file with all fortunes (original + new)

## Fortune Format

Each fortune follows this structure:
```json
{
  "id": 21,
  "text": "Your kindness will be returned to you tenfold",
  "category": "encouraging"
}
```

## Cost Estimation

- Uses GPT-3.5-turbo model
- Approximately 20-25 API calls
- Estimated cost: $0.50-$1.00 (depending on current pricing)

## Troubleshooting

**Error: "No fortunes were generated"**
- Check your OPENAI_API_KEY is set correctly
- Verify you have API credits available
- Check your internet connection

**Rate limit errors:**
- The script includes delays to avoid rate limits
- If you still get errors, increase the delay in `generate_fortunes.py`

**Quality issues:**
- The script filters out low-quality responses
- You can manually review `generated_fortunes.json` before merging

## Manual Review (Optional)

Before the fortunes are integrated, you can review them in `generated_fortunes.json` and remove any you don't like, then manually merge them with your existing fortunes.

## Integration

Once generated, the new fortunes are automatically integrated into your existing `fortunes.json` file. Your app will immediately have access to the expanded fortune database.