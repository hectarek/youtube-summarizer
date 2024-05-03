# YouTube Transcript Summarizer

This application is a simple Next.js app that takes a YouTube video URL as input, retrieves the transcript using a Python script, summarizes the content using OpenAI, and then displays the summary on the screen.

## Prerequisites

Before you can run this application, you'll need the following:

- Node.js (Recommended version: 14.x or later)
- Python (Version 3.8 or later)
- Pip (Python package manager)

## Setup

To get the application running on your local machine, follow these steps:

### Clone the Repository

Clone this repository to your local machine:

    git clone https://github.com/your-username/your-repository.git
    cd your-repository

### Install JavaScript Dependencies

Install the required Node.js packages:

    npm install

### Set Up Python Environment

It's recommended to use a virtual environment for Python dependencies:

    python3 -m venv venv
    source venv/bin/activate

Install the required Python packages:

    pip install -r requirements.txt

### Environment Variables

Create a `.env.local` file in the root directory and add your OpenAI API key:

    NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key_here

## Running the Application

With the dependencies installed and the environment properly configured, you can run the application:

    npm run dev

This will start the Next.js development server. Open `http://localhost:3000` in your browser to view the app.

## How It Works

1. **Input URL**: The user enters a YouTube video URL into the input field on the web page.
2. **Fetch Transcript**: The Python script is triggered which fetches the transcript of the specified YouTube video.
3. **Summarize**: The fetched transcript is then sent to OpenAI's API, which returns a summary of the transcript.
4. **Display Summary**: The summary is displayed on the web page, allowing the user to read through the condensed content.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

#### The following resources inspired this project:

- [Scraping YouTube with OpenAI API](https://www.youtube.com/watch?v=2TL3DgIMY1g)
- [How to Create a Flask + Next.js Project | Python Backend + Next.js & React Frontend](https://www.youtube.com/watch?v=OwxxCibSFKk)

