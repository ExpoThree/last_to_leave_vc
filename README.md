# 🎮 Pick a Corner! Discord Bot

A fun elimination game bot for Discord voice channels. Users are randomly assigned to voice channels and eliminated if they are in the wrong one. Moderators can check participants, eliminate users, and add participants.

## 🚀 Features

- **$checkvc**: Eliminates users who are not in a voice channel.
- **$elim [color]**: Eliminates users in the specified voice channel (red or blue).
- **$addparticipant**: Adds the participant role to all members (except eliminated ones).
- **$hello**: Sends a simple hello message.

## 📦 Requirements

- Python 3.8+
- `discord.py` (v2.0+)
- `python-dotenv` (for loading environment variables)
