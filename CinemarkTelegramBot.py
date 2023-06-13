import time
import os
import logging
import CinemarkAut as cinemark

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

async def today_functions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wait a moment please!!")
    functionsMessage = ""
    if(len(context.args) == 2):
        
        functionsDict = cinemark.get_today_functions(context.args[0], context.args[1])
        if(isinstance(functionsDict, str)):
            functionsMessage = functionsDict
        else:
            
            for functionDate in functionsDict:
                functionsMessage += "***{:0}***\n".format(functionDate)
                
                for functionFormat, functionHours in functionsDict[functionDate].items():
                    functionsMessage += "{:0}\n".format(functionFormat)
                    
                    for functionHour in functionHours:
                        functionsMessage += "*{:0}\n".format(functionHour)
                        
    else:
       functionsMessage = "You are missing some parameters" 

    await update.message.reply_text(functionsMessage)

async def functions_date_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wait a moment please!!")
    functionsMessage = ""
    if(len(context.args) == 3):
        
        functionsDict = cinemark.get_functions_for_date(context.args[0], context.args[1], context.args[2])
        if(isinstance(functionsDict, str)):
            functionsMessage = functionsDict
        else:
            
            for functionDate in functionsDict:
                functionsMessage += "***{:0}***\n".format(functionDate)
                
                for functionFormat, functionHours in functionsDict[functionDate].items():
                    functionsMessage += "{:0}\n".format(functionFormat)
                    
                    for functionHour in functionHours:
                        functionsMessage += "*{:0}\n".format(functionHour)

    else:
       functionsMessage = "You are missing some parameters" 

    await update.message.reply_text(functionsMessage)

async def movies_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wait a moment please!!")
    moviesMessage = ""
    moviesDict = cinemark.get_movies()
    if(isinstance(moviesDict, str)):
        moviesMessage = moviesDict
    else:
        for movie in moviesDict:
            moviesMessage += "{:0}\n".format(movie)
    await update.message.reply_text(moviesMessage)

async def cinemas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wait a moment please!!")
    cinemasMessage = ""
    cinemasDict = cinemark.get_cinemas()
    if(isinstance(cinemasDict, str)):
        cinemasMessage = cinemasDict
    else:
        for cinema in cinemasDict:
            cinemasMessage += "{:0}\n".format(cinema)
    await update.message.reply_text(cinemasMessage)
    
async def cinemas_movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wait a moment please!!")
    cinemasMessage = ""
    if (context.args):  
        cinemasDict = cinemark.get_cinemas_for_movie(context.args[0])
        if(isinstance(cinemasDict, str)):
            cinemasMessage = cinemasDict
        else:
            for cinema in cinemasDict:
                cinemasMessage += "{:0}\n".format(cinema)
    else:
        cinemasMessage = "You are missing the movie parameter"
    await update.message.reply_text(cinemasMessage)
    
async def movies_cinema_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wait a moment please!!")
    moviesMessage = ""
    if(context.args):
        moviesDict = cinemark.get_movies_for_cinema(context.args[0])
        if(isinstance(moviesDict, str)):
            moviesMessage = moviesDict
        else:
            for movie in moviesDict:
                moviesMessage += "{:0}\n".format(movie)
    else:
        moviesMessage = "You are missing the cinema parameter"    
    await update.message.reply_text(moviesMessage)

async def dates_movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wait a moment please!!")
    datesMessage = ""
    if(len(context.args) == 2):
        datesDict = cinemark.get_dates_for_movie_in_cinema(context.args[0], context.args[1])
        for date in datesDict:
            datesMessage += "{:0}\n".format(date)
    else:
        datesMessage = "You are missing some parameters"
    
    await update.message.reply_text(datesMessage)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    helpMessage = "This bot only works with commands:\n\n1. /getmovies brings a list of the current movies in cinemark.\n\n2. /getcinemas brings a list of the current cinemas in cinemark.\n\n3. /getcinemasformovie brings a list of the current cinemas that display the movie that you're looking for. Use one parameter: movie.\n\n4. /getmoviesforcinema brings a list of the current movies that are in the cinema that you're looking for. Use one parameter: cinema.\n\n5. /gettodayfunctions brings a list of the functions of the movie in a cinema. Use two parameters: cinema and movie.\n\n6. /getdates brings a list of the dates of the movie in a cinema. Use two parameters: cinema and movie.\n\n7. /getfunctionsfordate brings a list of the functions of the movie in a cinema in a specific day. Use three parameters: cinema, movie and date with the format dd/mm.\n\n8. /help brings the list of commands.\n\n9. for parameters, replace spaces with underscore(_) and the movie always in mayus"
    await update.message.reply_text(helpMessage)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("If you need help use the command /help")

def main() -> None:
    print("Starting...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("getmovies", movies_command))
    app.add_handler(CommandHandler("getcinemas", cinemas_command))
    app.add_handler(CommandHandler("getcinemasformovie", cinemas_movie_command))
    app.add_handler(CommandHandler("getmoviesforcinema", movies_cinema_command))
    app.add_handler(CommandHandler("getdates", dates_movie_command))
    app.add_handler(CommandHandler("gettodayfunctions", today_functions_command))
    app.add_handler(CommandHandler("getfunctionsfordate", functions_date_command))
    app.add_handler(CommandHandler("help", help_command))
    
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling...")
    app.run_polling(poll_interval=2)

if __name__ == "__main__":
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')