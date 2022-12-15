import bot
import scheduledtasks as st

if __name__ == '__main__':
    st.store_new_potd()
    bot.run_bot()
