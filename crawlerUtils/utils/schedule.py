import schedule
import time


__all__ = [
    "runSchedule", "regularFuncEverySecond", "regularFuncEverySeconds",
    "regularFuncEveryMinute", "regularFuncEveryMinuteTime",
    "regularFuncEveryMinutes", "regularFuncEveryHour", "regularFuncEveryHourTime",
    "regularFuncEveryHours", "regularFuncEveryDay", "regularFuncEveryDayTime",
    "regularFuncEveryDays", "regularFuncEveryWeek", "regularFuncEveryWeekTime",
    "regularFuncEveryWeeks", "regularFuncEveryMonday", "regularFuncEveryMondayTime",
    "regularFuncEveryTuesday", "regularFuncEveryTuesdayTime", "regularFuncEveryWednesday",
    "regularFuncEveryWednesdayTime", "regularFuncEveryThursday", "regularFuncEveryThursdayTime",
    "regularFuncEveryFriday", "regularFuncEveryFridayTime", "regularFuncEverySaturday",
    "regularFuncEverySaturdayTime", "regularFuncEverySunday", "regularFuncEverySundayTime",
]


def runSchedule(schedule):
    ''' 运行定时任务 '''
    while True:
        schedule.run_pending()
        time.sleep(1)


def regularFuncEverySecond(func, *args, **kwargs):
    ''' 每秒运行func函数 '''
    schedule.every().second.do(func, *args, **kwargs)
    runSchedule(schedule)


# def regularFuncEverySecondTime(func, secondtime, *args, **kwargs):
#     ''' 每秒某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
#     schedule.every().second.at(secondtime).do(func, *args, **kwargs)
#     runSchedule(schedule)


def regularFuncEverySeconds(func, seconds, *args, **kwargs):
    ''' 每多少秒运行func函数 '''
    schedule.every(seconds).seconds.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryMinute(func, *args, **kwargs):
    ''' 每分钟运行func函数 '''
    schedule.every().minute.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryMinuteTime(func, minutetime, *args, **kwargs):
    ''' 每分钟某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().minute.at(minutetime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryMinutes(func, minutes, *args, **kwargs):
    ''' 每多少分钟运行func函数 '''
    schedule.every(minutes).minutes.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryHour(func, *args, **kwargs):
    ''' 每小时运行func函数 '''
    schedule.every().hour.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryHourTime(func, hourtime, *args, **kwargs):
    ''' 每小时某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().hour.at(hourtime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryHours(func, hours, *args, **kwargs):
    ''' 每多少小时运行func函数 '''
    schedule.every(hours).hours.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryDay(func, *args, **kwargs):
    ''' 每天运行func函数 '''
    schedule.every().day.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryDayTime(func, daytime, *args, **kwargs):
    ''' 每天某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().day.at(daytime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryDays(func, days, *args, **kwargs):
    ''' 每多少天运行func函数 '''
    schedule.every(days).days.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryWeek(func, *args, **kwargs):
    ''' 每周运行func函数 '''
    schedule.every().week.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryWeekTime(func, weektime, *args, **kwargs):
    ''' 每周某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().week.at(weektime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryWeeks(func, weeks, *args, **kwargs):
    ''' 每多少周运行func函数 '''
    schedule.every(weeks).weeks.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryMonday(func, *args, **kwargs):
    ''' 每周一运行func函数 '''
    schedule.every().monday.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryMondayTime(func, mondaytime, *args, **kwargs):
    ''' 每周一某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().monday.at(mondaytime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryTuesday(func, *args, **kwargs):
    ''' 每周二运行func函数 '''
    schedule.every().tuesday.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryTuesdayTime(func, tuesdaytime, *args, **kwargs):
    ''' 每周二某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().tuesday.at(tuesdaytime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryWednesday(func, *args, **kwargs):
    ''' 每周三运行func函数 '''
    schedule.every().wednesday.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryWednesdayTime(func, wednesdaytime, *args, **kwargs):
    ''' 每周三某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().wednesday.at(wednesdaytime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryThursday(func, *args, **kwargs):
    ''' 每周四运行func函数 '''
    schedule.every().thursday.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryThursdayTime(func, thursdaytime, *args, **kwargs):
    ''' 每周四某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().thursday.at(thursdaytime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryFriday(func, *args, **kwargs):
    ''' 每周五运行func函数 '''
    schedule.every().friday.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEveryFridayTime(func, fridaytime, *args, **kwargs):
    ''' 每周五某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().friday.at(fridaytime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEverySaturday(func, *args, **kwargs):
    ''' 每周六运行func函数 '''
    schedule.every().saturday.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEverySaturdayTime(func, saturdaytime, *args, **kwargs):
    ''' 每周六某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().saturday.at(saturdaytime).do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEverySunday(func, *args, **kwargs):
    ''' 每周日运行func函数 '''
    schedule.every().sunday.do(func, *args, **kwargs)
    runSchedule(schedule)


def regularFuncEverySundayTime(func, sundaytime, *args, **kwargs):
    ''' 每周日某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    schedule.every().sunday.at(sundaytime).do(func, *args, **kwargs)
    runSchedule(schedule)
