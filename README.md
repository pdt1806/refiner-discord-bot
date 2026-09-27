<p align="center"><img width="50%" src="https://raw.githubusercontent.com/pdt1806/refiner-discord-bot/main/public/frieren.gif" /></p>
<h1 align="center">Refiner Discord Bot</h1>
<p align="center">"Feel free to praise me more" <(￣︶￣)></p>

## About Refiner

In order for [Discord Status as Image](https://disi.fyi/) to work, users' data need to be obtained by someone powerful, and Refiner is the one who can do that!

Why Refiner? I mean, why not? (￣ ▽ ￣)ノ She is the Greatest Mage of All Time after all 🪄

## Why the name Refiner?

<img width="30%" style="min-width: 250px" src="https://raw.githubusercontent.com/pdt1806/refiner-discord-bot/main/public/refiner.gif" />

## Local Development Setup

### Prerequisites

- A registered [Discord Bot Token](https://discord.com/developers/applications)
- [Python](https://www.python.org/) (>=3.12)
- [uv](https://docs.astral.sh/uv/)

### Environment Variables

1. Locate the `.env.example` file in the repository and duplicate it. Rename the duplicated file to `.env`.
2. Open the new `.env` file and populate it with your specific `APP_ID` and `TOKEN`.

### Start the Application

```bash
uv run main.py
```

The application is now running on `localhost:8010`.

## Command-Line Flags

| Flag | Long Flag | Type  | Default | Description                                   |
| :--- | :-------- | :---- | :------ | :-------------------------------------------- |
| `-p` | `--port`  | `int` | `8010`  | The port for the FastAPI server to listen on. |

#### Usage Examples

```bash
# Run on the default port (8010)
python main.py

# Run on a custom port using the short flag
python main.py -p 7001

# Run on a custom port using the long flag
python main.py --port 7001
```

## Technologies

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SlowAPI](https://slowapi.readthedocs.io/en/latest/)
- [uvicorn](https://www.uvicorn.org/)
