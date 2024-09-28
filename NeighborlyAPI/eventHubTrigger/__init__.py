import json
import logging
import azure.functions as func


def main(event: func.EventHubEvent):
    logging.info('Function triggered to process a message: ', event.get_body().decode())
    logging.info('EnqueuedTimeUtc =', event.enqueued_time)
    logging.info('SequenceNumber =', event.sequence_number)
    logging.info('Offset =', event.offset)

    result = json.loads(event.get_body().decode())
    logging.info("Python EventGrid trigger processed an event: {}".format(result))


