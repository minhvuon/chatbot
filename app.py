from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import levenshtein_distance
from chatterbot.comparisons import jaccard_similarity

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter", logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help me!',
            'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org'
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.50
        },
        {
		'import_path': 'chatterbot.comparisons.JaccardSimilarity'
		'statement_comparison_function'==jaccard_similarity
	}
    ])
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("./corpus/")
#trainer.train("./dataCSV/data.json")

# Train based on english greetings corpus
# trainer.train("chatterbot.corpus.english.greetings")

# Train based on the english convejsonrsations corpus
#trainer.train("chatterbot.corpus.english.conversations")
# trainer.train("chatterbot.corpus.english")

# Now we can export the data to a file
# trainer.export_for_training('./dataCSV/my_export.json')


@app.route("/")
def home():
    return render_template("newindex.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


if __name__ == "__main__":
    app.run()
