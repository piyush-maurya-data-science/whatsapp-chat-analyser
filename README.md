# Social Media Chat Analyzer

This project is a social media chat analyzer built with Python and Streamlit. The application provides various analyses on a chat log, including top statistics, activity timelines, activity maps, word cloud, most common words, emoji analysis, and sentiment analysis. The analysis can be done for a specific user or for the overall chat.

## Features

1. **Top Statistics**: Displays the total number of messages, total words, media shared, and links shared.
<img width="770" alt="Screenshot 2024-12-14 at 5 35 42 PM" src="https://github.com/user-attachments/assets/5a32e26e-b0ee-41a8-ad0e-a9b76cf15776" />



2. **Activity Timelines**: Shows the monthly and daily activity timelines.

<img width="910" alt="Screenshot 2024-12-14 at 5 39 53 PM" src="https://github.com/user-attachments/assets/9032258c-81c7-4e95-954a-bad2626dbbad" />
<img width="910" alt="Screenshot 2024-12-14 at 5 40 46 PM" src="https://github.com/user-attachments/assets/59511d01-1a86-47a1-95da-30bef6114ccb" />

3. **Activity Maps**: Visualizes the most busy day and month.
<img width="898" alt="Screenshot 2024-12-14 at 5 46 36 PM" src="https://github.com/user-attachments/assets/e5572a37-4540-428c-b48b-e63c3155e3f4" />
<img width="900" alt="Screenshot 2024-12-14 at 5 47 04 PM" src="https://github.com/user-attachments/assets/4385b7f1-e80d-490b-b17c-b55bd4c9bf88" />
<img width="914" alt="Screenshot 2024-12-14 at 5 47 29 PM" src="https://github.com/user-attachments/assets/0b4a7a77-2e7d-4399-964a-a4d8faa6eba1" />


5. **Word Cloud**: Generates a word cloud for frequent words.

<img width="914" alt="Screenshot 2024-12-14 at 5 50 02 PM" src="https://github.com/user-attachments/assets/33cc5e02-391b-464f-8d86-602b37a22022" />


7. **Most Common Words**: Lists the most common words used in the chat.
<img width="916" alt="Screenshot 2024-12-14 at 5 50 19 PM" src="https://github.com/user-attachments/assets/728c018a-ceae-41c0-b883-f8ab5e5630f3" />


8. **Emoji Analysis**: Analyzes the usage of emojis in the chat.
<img width="916" alt="Screenshot 2024-12-14 at 5 50 41 PM" src="https://github.com/user-attachments/assets/25015c5c-8abb-4f11-bf4f-01ecb92f19a4" />


9. **Sentiment Analysis**: Performs sentiment analysis based on the text and emojis used in the messages.
<img width="916" alt="Screenshot 2024-12-14 at 5 50 58 PM" src="https://github.com/user-attachments/assets/baaf00a2-9d21-45f0-bb3b-415cd97dcbd8" />

## Project Structure

- `app.py`: The main Streamlit application.

- `preprocessor.py`: Contains the `preprocess` function for preprocessing the chat log.

- `helper.py`: Contains various helper functions for the analyses.

- `stop_hinglish.txt`: A text file containing common hindi and english stopwords to be excluded from the word cloud and most common words analysis.

