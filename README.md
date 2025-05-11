# 🎮 Last to Leave VC Discord Bot

A fast-paced elimination game for Discord voice channels! This bot lets moderators manage participants, track who's in voice chat, and run custom elimination rounds — including a unique red-blue four-corner challenge. Designed for events that last less than an hour with no limit on the number of participants.

## 🚀 Features

- **$startcheck / $stopcheck**: Enable or disable automatic elimination when users leave a VC.
- **$checkvc**: Manually eliminate users who are not currently in any voice channel.
- **$elim [color]**: Eliminates all users in the specified voice channel (`red` or `blue`), then runs `$checkvc` to clean up.
- **$addparticipant**: Adds the participant role to all eligible users and removes the eliminated role if present.
- **$hello**: Sends a simple hello message.

## ⚙️ How It Works

- Users with the **participant role** are monitored.
- If a participant leaves the VC (and they’re not a moderator), they’re marked as **eliminated**.
- Custom roles and channels (like red and blue corners) are used in event-specific eliminations.
- A moderator-only command system ensures fair control.

## 🛠 Requirements

- Python 3.8+
- [`discord.py`](https://pypi.org/project/discord.py/) (v2.0+)
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) (for loading environment variables)

## 📝 Notes

- Role and channel IDs are pre-configured in the code.
- Moderators must have the assigned moderator role to use commands.

[Description given by OpenAI]
