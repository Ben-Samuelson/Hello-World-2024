happyEmojis = ["🙂","😃","😀","😄","😆","😸","😺","😊","😂","🤣"
               ,"😁"]
sadEmojis = ["😢", "😞","😔","😟" ,"😣","😩","😭","😿","😓","😥","🥺","😥","😖","😫"]
angryEmojis= ["😡","💢", "🔥","😤", "😾"]
disgustEmojis = ["😖", "🤢","🤮","😷","🤧"]
fearEmojis= ["😨", "😱", "😰", "😥", "😧", "😬"]
excitementEmojis = ["🥳", "🎊", "🌟", "✨","🎈","🎉","😁","🤩"]



exampleMessages = ["Hey! 🎉 How's your day going? 🌞",
            "Just finished my workout! 💪😅 Now time for a smoothie! 🥤",
            "Can’t wait for the weekend! 🎊 Any plans? 🗓️",
            "Just saw the cutest puppy! 🐶❤️ Wish you were here!",
            "Movie night tonight? 🍿🎬 I’ll bring the snacks! 🍫",
            "Feeling a bit under the weather 🤒. Any recommendations? 🤔",
            "Happy birthday! 🎂🎈 Hope your day is as amazing as you are!",
            "Just got back from the beach! 🏖️☀️ So much fun!",
            "OMG, did you see that new show? 😱📺 We need to discuss!",
            "Lunch time! 🍕 What are you having? 😋"]

messages2 = ["Just got some great news! 🎉😊",
"Can’t wait for our trip! 🥳✈️🌴",
"Had an amazing day with friends! 😄❤️",
"Feeling so grateful today! 🌟🙏💖",
"Just finished a great book! 📚✨😊",
"Dinner was delicious! 🍽️😋🤤",
"Weekend vibes are here! 🎈😎✨",
"So proud of you! You did amazing! 🎊👏😄"]

happyCounter = 0
sadCounter = 0
angerCounter = 0
disgustCounter = 0
fearCounter = 0
excitementCounter = 0
emojiBoard = {"Happiness": happyEmojis, "disgust": disgustEmojis,
                "Sadness": sadEmojis,"Fear": fearEmojis,
                "Anger": angryEmojis, "Excitement": excitementEmojis}
counterBoard = {"Happiness": happyCounter, "disgust": disgustCounter,
                "Sadness": sadCounter,"Fear": fearCounter,
                "Anger": angerCounter, "Excitement": excitementCounter}

for message in exampleMessages:
    for emotion in emojiBoard:
        for emoji in emojiBoard[emotion]:
            if message.find(emoji) != -1:
                counterBoard[emotion] += 1


print(counterBoard)

