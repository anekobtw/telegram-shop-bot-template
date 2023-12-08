# zverskly bot
 upd 08/12/2023: what a shit code I was writing lol

 A telegram bot for zverskly. It was made to order.

# Available Commands
`/start`: Start a conversation and access various features.\
`/links`: Display links to social media.\
`/developer`: Get information about the bot's developer.\
`/orders [status]`: View orders based on their status (e.g., /orders 0 to view orders in "Waiting for Acceptance" status).\
`/change_status [order_id] [new_status]`: Change the status of an order (admin only).\
`/next`: View the first order in the database.\
`/order`: Start the process of placing a new order.\
`/my_orders`: View your own orders.\
`/cancel_order [order_id]`: Cancel an order (admin only).\
`/review [text]`: Submit a review.\
`/reviews`: View all submitted reviews.

## Prerequisites
Before you can run this project, you need to have the following prerequisites in place:

Python 3.7 or higher\
[aiogram](https://github.com/aiogram/aiogram) library\
MemoryStorage from aiogram\
A Telegram bot token\
A Telegram web app URL (for handling web app data)

## Installation
Clone the project repository:\
`git clone https://github.com/anekobtw/zverskly-bot`

Install the required Python packages using pip:\
`pip install aiogram`

## Configuration
Replace `BOT_TOKEN` in the code with your Telegram bot token.

Set the `web_app_info` variable to the URL of your Telegram web app (e.g., https://yourwebsite.com/index.html).

## License
This project is licensed under the MIT License

## Contact
If you have any questions or need assistance, you can contact the bot developer:

Telegram: [@anekobtw](https://t.me/anekobtw)\
Thank you for using Zverskly Bot! I hope you find it useful.
