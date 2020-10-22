# DrugBank Scraper
**This is a quick project that was used to scrape the following drugs from DrugBank:**
- "DB00619"
- "DB01048"
- "DB14093"
- "DB00173"
- "DB00734"
- "DB00218"
- "DB05196"
- "DB09095"
- "DB01053"
- "DB00274"


**To run a containerized version of this project (requires docker):**  
```git clone https://github.com/chrisabbott/drugbank-ingest.git && cd drugbank-ingest && docker build -t drugbank-ingest . && docker run -it drugbank-ingest```

**Note about scraping from DrugBank**  
As per DrugBank terms and conditions, this is not intended to be used for bulk scraping.
