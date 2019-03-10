import schedule
import time


__all__ = [
    "Schedule"
]


class Schedule():

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def scheduleRun(self, schedule):
        ''' 运行定时任务 '''
        while True:
            schedule.run_pending()
            time.sleep(1)

    @classmethod
    def scheduleFuncEverySecond(self, func, *args, **kwargs):
        ''' 每秒运行func函数 '''
        schedule.every().second.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    # @classmethod
    # def scheduleFuncEverySecondTime(func, secondtime, *args, **kwargs):
    #     ''' 每秒某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
    #     schedule.every().second.at(secondtime).do(func, *args, **kwargs)
    #     self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEverySeconds(self, func, seconds, *args, **kwargs):
        ''' 每多少秒运行func函数 '''
        schedule.every(seconds).seconds.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryMinute(self, func, *args, **kwargs):
        ''' 每分钟运行func函数 '''
        schedule.every().minute.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryMinuteTime(self, func, minutetime, *args, **kwargs):
        ''' 每分钟某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().minute.at(minutetime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryMinutes(self, func, minutes, *args, **kwargs):
        ''' 每多少分钟运行func函数 '''
        schedule.every(minutes).minutes.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryHour(self, func, *args, **kwargs):
        ''' 每小时运行func函数 '''
        schedule.every().hour.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryHourTime(self, func, hourtime, *args, **kwargs):
        ''' 每小时某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().hour.at(hourtime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryHours(self, func, hours, *args, **kwargs):
        ''' 每多少小时运行func函数 '''
        schedule.every(hours).hours.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryDay(self, func, *args, **kwargs):
        ''' 每天运行func函数 '''
        schedule.every().day.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryDayTime(self, func, daytime, *args, **kwargs):
        ''' 每天某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().day.at(daytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryDays(self, func, days, *args, **kwargs):
        ''' 每多少天运行func函数 '''
        schedule.every(days).days.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryWeek(self, func, *args, **kwargs):
        ''' 每周运行func函数 '''
        schedule.every().week.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryWeekTime(self, func, weektime, *args, **kwargs):
        ''' 每周某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().week.at(weektime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryWeeks(self, func, weeks, *args, **kwargs):
        ''' 每多少周运行func函数 '''
        schedule.every(weeks).weeks.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryMonday(self, func, *args, **kwargs):
        ''' 每周一运行func函数 '''
        schedule.every().monday.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryMondayTime(self, func, mondaytime, *args, **kwargs):
        ''' 每周一某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().monday.at(mondaytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryTuesday(self, func, *args, **kwargs):
        ''' 每周二运行func函数 '''
        schedule.every().tuesday.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryTuesdayTime(self, func, tuesdaytime, *args, **kwargs):
        ''' 每周二某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().tuesday.at(tuesdaytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryWednesday(self, func, *args, **kwargs):
        ''' 每周三运行func函数 '''
        schedule.every().wednesday.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryWednesdayTime(self, func, wednesdaytime, *args, **kwargs):
        ''' 每周三某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().wednesday.at(wednesdaytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryThursday(self, func, *args, **kwargs):
        ''' 每周四运行func函数 '''
        schedule.every().thursday.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryThursdayTime(self, func, thursdaytime, *args, **kwargs):
        ''' 每周四某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().thursday.at(thursdaytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryFriday(self, func, *args, **kwargs):
        ''' 每周五运行func函数 '''
        schedule.every().friday.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEveryFridayTime(self, func, fridaytime, *args, **kwargs):
        ''' 每周五某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().friday.at(fridaytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEverySaturday(self, func, *args, **kwargs):
        ''' 每周六运行func函数 '''
        schedule.every().saturday.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEverySaturdayTime(self, func, saturdaytime, *args, **kwargs):
        ''' 每周六某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().saturday.at(saturdaytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEverySunday(self, func, *args, **kwargs):
        ''' 每周日运行func函数 '''
        schedule.every().sunday.do(func, *args, **kwargs)
        self.scheduleRun(schedule)

    @classmethod
    def scheduleFuncEverySundayTime(self, func, sundaytime, *args, **kwargs):
        ''' 每周日某一时刻运行func函数，格式HH:MM:SS, HH:MM,`:MM`, :SS '''
        schedule.every().sunday.at(sundaytime).do(func, *args, **kwargs)
        self.scheduleRun(schedule)
