# campfireify
Group project for the Bitcamp 2025 Hackathon.

Focused on learning how to use Python, HTML/CSS/JS, and the Spotify API for various implementations with a goal in mind: "What can we show the user in unique ways or unique data analysis?"

Inspired by Icebergify, Receiptify, other similar websites, and past Spotify Wrappeds.

See our submission to Devpost for Bitcamp 2025 -> https://devpost.com/software/campfireify?ref_content=user-portfolio

Current implementations:
- Log in page (allows for authorization to use user data per Spotify's OAuth2 protocol)
- Currently playing track - does not update with song updates yet
- User's top artists and top tracks
- Global top artists and tracks

Other intended goals:
-  "The S'more" --> Using an average of each characterstic value of the user's top 50 songs in the past 6 months to find "Your representative song (S'more)"
Note: songs have characteristics such as "danceability," "acoustic," etc. such that we could take the averages and find a song with similar attributes to those averages
- Create better website design

Other notes:
- Currently only locally hosted since 25 user limit to access our project through the Spotify API log-in
