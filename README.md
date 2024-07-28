# Apsiyon Social Content Check

This application is a simple web demo used for monitoring posts shared in the Apsiyon Social app. This system works during the post-sharing step in the Apsiyon Social app.

First, it checks if the post contains any words from the blacklist in [this](https://github.com/ooguz/turkce-kufur-karaliste/blob/master/karaliste.txt) repo. If it passes the blacklist check, a sentiment analysis is performed by the LLM Agent. The agent categorizes the post as "Uygun", "Uygunsuz", "Saldırgan", "Kötümser", or "Kinayeli". If the post is categorized as "Uygun", it can be shared.

For visual posts, the LLM checks if the visual content is appropriate.

---

## Requirements

### Environment

Ensure that your Python version is set to `3.10.12` (pip version is `24.1.2`):

```bash
python --version
```
- Setting up Virtualenv:

```bash
pip install virtualenv
```
- Creating a Virtual Environment:
```bash
virtualenv venv
```
- Activating the Virtual Environment:
```bash
source venv/bin/activate
```
- Installing the necessary libraries:
```bash
pip install -r requirements.txt
```

#### Configuration

- Set up your .env file:

```bash
cd <project-directory>
```

```bash
- Create the .env file and add your OPENAI_API_KEY:

    OPENAI_API_KEY='key' # .env file

```

#### Run

- Launch the Streamlit app in terminal:
```bash
python3 app.py
```
----
