from celery.schedules import crontab
from .models import Bots, Profile
import datetime
from datetime import timedelta
from core.celery import app


@app.task
def bot_time(bot_id, profile_name):
    bot_data = Bots.objects.get(id=bot_id)
    if profile_name != "I'M ON VACATION":
        if str(bot_data.time_left) == "00:00:00":
            lock = True
        else:
            lock = False
        if lock == False:
            if bot_data.status == True:
                # calculate time left
                date_time_left = datetime.datetime.strptime(
                    str(bot_data.time_left), "%H:%M:%S"
                )
                subtraction = date_time_left - timedelta(0, 60)
                current_time_left = subtraction - datetime.datetime(1900, 1, 1)
                bot_data.time_left = str(current_time_left)

                bot_data.save()
        else:
            bot_data.status = False
            bot_data.stop = None
            bot_data.save()
