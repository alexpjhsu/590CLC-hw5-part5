import json
import telegram
import os
import logging
import tg_token

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}


def configure_telegram():
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)


def webhook(event, context):
    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if event.get('requestContext').get('http').get('method') == 'POST' and event.get('body'): 
        logger.info('Message received')
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)
        chat_id = update.message.chat.id
        text = update.message.text
        
        if text == '/start':
            text = 'Hello, human! I am an echo bot!'

        bot.sendMessage(chat_id=chat_id, text=text)
        logger.info('Message sent')

        return OK_RESPONSE

    return ERROR_RESPONSE


def set_webhook(event, context):
    logger.info('Event: {}'.format(event))
    bot = configure_telegram()
    url = 'https://' + event.get('headers').get('host')
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE
    
def lambda_handler(event, context):
    logger.info('Event: {}'.format(event))
    
    if event.get('requestContext').get('http').get('method') == 'POST':
        if  event.get('rawPath') == '/hw5-part5/set_webhook/':
            logger.info('set_webhook received')
            return set_webhook(event, context)
        else:
            logger.info('webhook received')
            return webhook(event, context)
    return ERROR_RESPONSE