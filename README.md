<<<<<<< HEAD
# Telegram shop bot
i dont like this project tbh :\

=======
# Telegram shop bot template
>>>>>>> 615f435077519525ac5276bafc4272ea6bfd3683
![licence](https://img.shields.io/badge/License-MIT-green.svg)
![version](https://img.shields.io/badge/Version-v1.3_beta-blue)
[![codecov](https://codecov.io/gh/anekobtw/telegram-shop-bot/graph/badge.svg?token=TXQWSC0UR9)](https://codecov.io/gh/anekobtw/telegram-shop-bot-template)
![made with love](https://img.shields.io/badge/Made_with-Love-red)

Customizable telegram shop bot
 
## Installing
Clone the project to your local machine.
```console
$ git clone https://github.com/anekobtw/telegram-shop-bot-template.git
```

## Setting up
Do not modify any files except `config.py`. Doing so may result in numerous bugs :)

- Replace `BOT_TOKEN` with your Telegram bot token (Obtain it from [BotFather](https://web.telegram.org/k/#@BotFather)).
```python
BOT_TOKEN = ''  #replace with your token
```

- Change the currency you're using for selling items. (optional)
```python
currency = '$'
```

- Furthermore, add the products you're selling into the dictionary using the following format:\
`'product name' - price`

```python
items = {
    'Item1': 100,
    'Item2': 200,
    'Item3': 500
}
```

Remember to restart the bot to apply the changes.

## Acknowledgements
 - [aiogram](https://github.com/aiogram/aiogram) - A modern and fully asynchronous framework for Telegram Bot API written in Python using asyncio 

## Contributing
Contributions are always welcome! If you have any suggestions, feature requests, or bug reports, please feel free to open an issue on the [GitHub repository](https://github.com/anekobtw/timewise).
