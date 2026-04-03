name: Amazon Deals Bot Crawler

on:
  schedule:
    - cron: '*/30 * * * *'
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    name: Amazon Scraper Job

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install Libraries
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4 lxml

      - name: Run Amazon Bot
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
        run: python bot.py
