from celery.decorators import task
from celery.utils.log import get_task_logger

from athena_app.harvest_manager import create_harvest

logger = get_task_logger(__name__)


@task(name="harvest_task")
def harvest_task(hashtag, start_date, end_date):
    """Harvests a Twitter history of tweets, using a hashtag and date limits"""
    logger.info("Starting harvest...")
    return create_harvest(hashtag, start_date, end_date)
