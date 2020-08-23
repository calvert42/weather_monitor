This is a bot script that send weather update to a specified email address in case the weather will be changing over a time period.

By default, it will run every hour for a total of six times. The time period it will check will be the next hour.
If it detects that the weather is changing (temperature of precipitations ofr ex) it will send an email specifying the expected weather changes to the specified user.

To work locally, the user will have to obtain a free API key at https://openweathermap.org/api and set the corresponding environments variables (or change the code accordingly)

By default the code identifies them in this manner:

API_WEATHER = the api key
MY_MAIL = the mail of the receiver of the update
BOT_MAIL = mail account of the sender
BOT_GOOGLE_APP_PASS = the app password to connect to a gmail account (it might be your regular mail account password if you're using another mail service)

The different parameters contained in config.json are explained in the __init__ method of weather_monitor.py
