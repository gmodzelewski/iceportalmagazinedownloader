# Georg's ICE Portal Magazine Downloader

A small python application to download magazines from the german ICE portal, an entertainment website for trains. Proudly created via vibe coding in a train from Hamburg to Ingolstadt, with heavily usage of Deepseek R1 Qwen (14b), Llama 4 (17b) and Mistral (24b).

### Problem statement 
Downloading individual magazines is time-consuming because you have to click on each magazine individually on the website and navigate to it. However, since the German ICE internet connection often drops out, and I prefer to use my own mobile internet on my phone, I wanted to save some time without having to decide on a specific magazine.

### Proposed solution
To have a thing that does the tedious clicking and downloading for you. Just start an application and you can switch to your own mobile network.

### Prerequisites: 
You sit in an ICE train and are connected to WLAN-on-ICE.

### How to use that

1. `uv sync`
2. `uv run main.py`

The magazines will be downloaded into the `downloaded_magazines` folder with appended date.