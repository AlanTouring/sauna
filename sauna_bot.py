##!/usr/bin/env python
# pylint: disable=W0613, C0116
"""
Telegram Bot to control my sauna with Telegram messages.
First, a few handler functions are defined.
Then, those functions are passed to the Dispatcher
and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic sauna control bot.
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
type /help for help in Telegram
"""

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import io_port
from sauna import Sauna, Login
from testframe.test_util import print_stderr

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

__login: Login = Login()
__sauna: Sauna = Sauna()

"""Define command handlers for Telegram.
These usually take the two arguments update and context.
Error handlers also receive the raised TelegramError object in error."""


def login(update: Update, context: CallbackContext) -> None:
    """Perform password check when the command /login is issued."""
    update.message.reply_text('Hi!\nI am your sauna control bot.')
    try:
        __login.login_user(context.args[0])
        update.message.reply_text(__login.get_log_status_text())

    except (IndexError, ValueError):
        update.message.reply_text(__login.get_log_status_text())
    return


def temp(update: Update, context: CallbackContext) -> None:
    """Send temp of sauna when the command /temp is issued."""
    txt = str(__sauna.control.getPortValue("Temperature Sensor 2"))
    update.message.reply_text(txt)


def lighton(update: Update, context: CallbackContext) -> None:
    """Switch light on when the command /lighton is issued."""
    if __sauna.control.getPortValue("Light Sensor") == 0:
        __sauna.control.togglePortValue("Light Switch")
        update.message.reply_text("Light is on")
    else:
        update.message.reply_text("Light was already on")


def lightoff(update: Update, context: CallbackContext) -> None:
    """Switch light off when the command /lighton is issued."""
    if __sauna.control.getPortValue("Light Sensor") == 1:
        __sauna.control.togglePortValue("Light Switch")
        update.message.reply_text("Light is off")
    else:
        update.message.reply_text("Light was already off")


def heatmore(update: Update, context: CallbackContext) -> None:
    """increase the heat when the command /heatmore is issued."""
    __sauna.control.increaseLimit("Temperature Sensor 2")

    str_list = []
    temp_str = str(__sauna.control.getPortValue("Temperature Sensor 2"))
    str_list.append('Sauna temp is currently ' + temp_str + ' C.\n')

    temp_str = str(__sauna.control.getUpperLimit("Temperature Sensor 2"))
    str_list.append('Sauna temp is going to ' + temp_str + ' C.\n')
    update.message.reply_text(''.join(str_list))


def heat(update: Update, context: CallbackContext) -> None:
    """Start heating of sauna when the command /heat is issued."""
    if __login.is_user_logged_in():
        if __sauna.control.getPortValue("Mains Sensor") == 1:

            if __sauna.control.getPortValue("Power Sensor") == 0:
                __sauna.control.togglePortValue("Power Switch")

            if __sauna.control.getPortValue("Light Sensor") == 0:
                __sauna.control.togglePortValue("Light Switch")

            if __sauna.control.is_below_lower_limit("Temperature Sensor 2"):
                if __sauna.control.getPortValue("Oven Sensor") == 0:
                    __sauna.control.togglePortValue("Oven Switch")
                    update.message.reply_text('Starting to heat.')
        else:
            update.message.reply_text('Main power is switched off. Needs to be set manually.')
    else:
        update.message.reply_text("You are not logged in. Log in!!")


def off(update: Update, context: CallbackContext) -> None:
    """Switch sauna of when the command /off is issued."""
    if __sauna.control.getPortValue("Light Sensor") == 1:
        __sauna.control.togglePortValue("Light Switch")

    if __sauna.control.getPortValue("Oven Sensor") == 1:
        __sauna.control.togglePortValue("Oven Switch")

    if __sauna.control.getPortValue("Power Sensor") == 1:
        __sauna.control.togglePortValue("Power Switch")

    __login.logout_user()

    str_list = []
    str_list.append('Sauna power is switched OFF.\n')
    str_list.append('Sauna oven is switched OFF.\n')
    str_list.append('Sauna light is switched OFF.\n')
    str_list.append('You are logged OUT.\n')
    temperature = __sauna.control.getPortValue("Temperature Sensor 2")
    str_list.append("Temp is " + str(temperature) + " C.\n")
    update.message.reply_text(''.join(str_list))


def status(update: Update, context: CallbackContext) -> None:
    """Send status of sauna when the command /status is issued."""
    str_list = ['Sauna main power is ']
    if __sauna.control.getPortValue("Mains Sensor") == 1:
        str_list.append('on.')
    else:
        str_list.append('OFF.')
    str_list.append('\n')

    str_list.append('Sauna power switch is ')
    if __sauna.control.getPortValue("Power Sensor") == 1:
        str_list.append('on.')
    else:
        str_list.append('OFF.')
    str_list.append('\n')

    str_list.append('Sauna oven is currently ')
    if __sauna.control.getPortValue("Oven Sensor") == 1:
        str_list.append('HEATING.')
    else:
        str_list.append('OFF.')
    str_list.append('\n')

    str_list.append('Sauna light is ')
    if __sauna.control.getPortValue("Light Sensor") == 1:
        str_list.append('on.')
    else:
        str_list.append('OFF.')
    str_list.append('\n')

    temp_str = str(__sauna.control.getPortValue("Temperature Sensor 2"))
    str_list.append('Sauna temp is currently ' + temp_str + ' C.\n')

    temp_str = str(__sauna.control.getUpperLimit("Temperature Sensor 2"))
    str_list.append('Sauna temp is going to ' + temp_str + ' C.\n')
    update.message.reply_text(''.join(str_list))


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    commands = ["/login <pwd>\n",
                "/status\n",
                "/heat\n",
                "/temp\n",
                "/off\n",
                "/help\n",
                "/set\n",
                "/unset\n",
                "/heatmore\n",
                "/lighton\n",
                "/lightoff\n"]

    cmd: str = " ".join(commands)
    update.message.reply_text('commands are:\n' + cmd)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def send_temp(context):
    """Send the sauna temp."""
    job = context.job
    text = str(__sauna.control.getPortValue("Temperature Sensor 2"))
    context.bot.send_message(job.context, text="Sauna temp is " + text + " Grad")


def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def add_job_timer(update: Update, context: CallbackContext) -> None:
    """handler telegram for reporting the temperature in the sauna"""
    chat_id = update.message.chat_id
    try:
        # args[0] = time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('the timer for temp report must be positive!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(send_temp, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' previous timer was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def remove_job_timer(update: Update, context: CallbackContext) -> None:
    """handler telegram"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def main():
    """Start the sauna bot."""
    # Create the Updater and pass it the token of your bot.
    updater = Updater("1276131699:AAHhrtxf6vv-bmFMCnwv2AsjYCn-Ji6zJMs",
                      use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(CommandHandler("lighton", lighton))
    dispatcher.add_handler(CommandHandler("lightoff", lightoff))
    # get current temperature
    dispatcher.add_handler(CommandHandler("temp", temp))
    # switch on oven
    dispatcher.add_handler(CommandHandler("heat", heat))
    # increase heat by until it flips to the lower limit again
    dispatcher.add_handler(CommandHandler("heatmore", heatmore))
    # switch everything off
    dispatcher.add_handler(CommandHandler("off", off))
    # get status
    dispatcher.add_handler(CommandHandler("status", status))
    # online help
    dispatcher.add_handler(CommandHandler("help", help_command))
    # set reporting interval for temperature reports
    dispatcher.add_handler(CommandHandler("set", add_job_timer))
    # delete reporting interval
    dispatcher.add_handler(CommandHandler("unset", remove_job_timer))
    # on a non-command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C in the shell or
    # the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()


if __name__ == '__main__':
    main()
