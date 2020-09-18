from .models import Bots
import datetime
from datetime import timedelta
from celery import shared_task

@shared_task
def bot_time():
    for bot in Bots.objects.all():
        if bot.profile.plan.name != "PREMIUM":
            bot_time = bot.time_left
            if str(bot_time) != "00:00:00":
                if bot.status == True:
                    # create datetime from time
                    date_time_left = datetime.datetime.strptime(
                        str(bot_time), "%H:%M:%S"
                    )
                    subtraction = date_time_left - timedelta(0, 60)
                    current_time_left = subtraction - datetime.datetime(1900, 1, 1)
                    bot.time_left = str(current_time_left)
                    # calculate converted time
                    converted_time = bot_time.hour + bot_time.minute / 60.0
                    bot.converted_time = converted_time
                    bot.save()
