# Politifact Web Scraping Project

## Overview

Unveiling the intricacies of political discourse, the Politifact Web Scraping Project is a Python-powered endeavor utilizing the Scrapy framework. This initiative seeks to extract and analyze fact-checking data from [Politifact.com](https://politifact.com), providing valuable insights into political statements, rulings, and the evolving information landscape.

## Key Features

1. **Data Extraction:** Scraps author names, saying dates, headlines, rulings, publishers, and article URLs for a comprehensive dataset.
2. **File Management:** Dynamically creates directories for organized storage of scraped data, ensuring a systematic approach from the project's outset.
3. **Image Downloads:** Utilizes Scrapy's image pipeline for downloading header images, enhancing the visual context of each article.
4. **Efficient CSV Handling:** Implements regular write intervals to prevent data loss and alleviate memory burden during asynchronous requests.


## Requirements
- **Python 3.x**
- **Scrapy**
- **Requests**
- **Pandas**

## Getting Started
1. **Clone the Repository:**
    ```
    git clone https://github.com/Muneeb1030/WebScrapper_Politifact.git
    ```

2. **Install Dependencies:**
    ```
    pip install scrapy pandas requests
    ```


3. **Run the Scraper:**
    ```
    scrapy crawl politifact
    ```

## Additional Information
- **Customization:**
    - Tailor the scraper to your needs by modifying the Scrapy spiders.
- **GitHub Repository:**
    - Explore, contribute, and stay updated on the [GitHub repository](\https://github.com/Muneeb1030/WebScrapper_Politifact.git).


## Disclaimer
This project is intended for educational purposes and strictly adheres to Politifact's terms of service. Users are advised to deploy the scraper responsibly and in compliance with platform policies.

## Additional Resources

Explore the project in detail through my [Medium blog](https://medium.com/@m.muneeb.ur.rehman.2000/fact-checking-the-fact-checkers-scraping-politifact-com-for-political-truths-with-pythons-scrapy-fcfa42f5bcf2), where I share insights, motivation, and in-depth explanations about the Politifact Scraper.

## Contributors
- M Muneeb ur Rehman

Feel free to fork, contribute, and enhance the capabilities of this Mastodon scraper. Happy scraping! 🌐💻


