# AI-SDR

AI-SDR stands for Artificial Intelligence Sales Development Representative. This project automates and optimizes the sales outreach process, including generating cold emails, handling responses, and tracking interactions.


## Prerequisites

- Python 3.12.0

## Setup Instructions

### 1. Create and Activate a Virtual Environment

1. **Create a virtual environment:**
    ```bash
    python3.12 -m venv .venv
    ```
2. **Activate the virtual environment:**
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
3. **Upgrade pip to the latest version:**
    ```bash
    pip install --upgrade pip
    ```

### 2. Install Required Packages

1. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Process Flow Diagram

1. 

### 4. Scope of Improvement

1. **CXO Finder:**

    Paid API required - Testing and improvement Pending


2. **Email Bounce:**

    A logic can be implemented to verify if the mail will bounce. Right not it is only working on Regex operation


3. **Analytics Page:**

    Analytics page can be design which can shows different plot, which can be helpfull for the Sales team.
    for ex. plot showing who have opened our cold mail.


4. **Sentiment Analysis:**

    Right Now the sentiment Analysis(as per the reply receive from the potential customer) is Hard coded


5. **Mail sending and LinkedIn message sending not started:**

    Right Now this is not started

              

## Notes

- Ensure that the virtual environment is activated before running any scripts or commands.
- If you encounter any issues, check that all dependencies are installed and that the Python path is set correctly.

## Troubleshooting

- **Missing Packages:** Ensure all packages listed in `requirements.txt` are installed.
- **Server Issues:** Check the terminal for error messages and ensure that the server is running correctly.
