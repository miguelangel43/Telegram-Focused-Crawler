# A Framework for Focused-crawling of Telegram Channels and Messages

The objective of this BSc thesis is to develop a framework for focused-crawling of Telegram channels with different crawling and evaluation strategies along with a data collection component.
German-speaking Telegram groups related to misinformation during the COVID-19 pandemic will be crawled and a dataset with the messages contained in those groups along with metadata will be created. 

## Theoretical principles

This work draws inspiration from the following papers:

> Jalilvand, Asal, and Mahmood Neshati.
> ["Channel retrieval: finding relevant broadcasters on Telegram."](https://link.springer.com/article/10.1007/s13278-020-0629-z)
> Social Network Analysis and Mining 10.1 (2020): 1-16.

>Srinivasan, Padmini, Filippo Menczer, and Gautam Pant.
>["A general evaluation framework for topical crawlers."](https://link.springer.com/content/pdf/10.1007/s10791-005-6993-5.pdf)
>Information Retrieval 8.3 (2005): 417-447

<!-- ## License
GNU GENERAL PUBLIC LICENSE Version 3 -->

# File structure

`telegram_crawler/`

- `models/`: Crawling strategies.
    - `mo_balog1.py`: Balog1.
    - `mo_okapi_bm25.py`: Okapi BM25.
- `evaluation/`: Evaluation strategies.
    - `ev_recollection_rate.py`: Rate of seed recollection.
- `database/`: DBMS code.
- __`crawler.py`__: Focused crawler pipeline.
- `data_collection.py`: Data collection pipeline. 
- `telegram.py`: Telegram API (Telethon) code.
