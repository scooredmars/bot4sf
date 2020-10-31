from .models import Bots, Profile, Plan
import datetime
from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.contrib import messages


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
                    current_time_left = subtraction - \
                        datetime.datetime(1900, 1, 1)
                    bot.time_left = str(current_time_left)
                    # calculate converted time
                    converted_time = bot_time.hour + bot_time.minute / 60.0
                    bot.converted_time = converted_time
                    bot.save()


@shared_task
def plan_check():
    users_plans = Profile.objects.all().exclude(plan__name="STARTER")
    for user_plan in users_plans:
        today_date = timezone.now()
        today_date.astimezone(timezone.utc).replace(tzinfo=None)
        if user_plan.plan_expiration_date:
            if today_date >= user_plan.plan_expiration_date:
                starter_plan = Plan.objects.get(name="STARTER")
                user_plan.plan = starter_plan
                user_plan.plan_expiration_date = None
                user_plan.save()

                bots = Bots.objects.filter(profile=user_plan)
                current_bots = bots.count()
                if current_bots > starter_plan.max_bots:
                    first_bot = bots[0].id
                    for bot in bots:
                        if first_bot != bot.id:
                            Bots.objects.filter(id=bot.id).delete()
                        elif first_bot:
                            bot.time_left = "06:00:00"
                            bot.converted_time = 6
                            bot.save()
