#Word recommdation system 


import re
from collections import defaultdict, Counter


class NextWordPredictor:
    def __init__(self):
        self.bigram_count_map = defaultdict(Counter)
        self.trigram_count_map = defaultdict(Counter)

    def load_corpus(self, file_path):
        """
        Processes a corpus file to extract bigrams and trigrams.
        """
        print(f"Processing corpus for n-grams: {file_path}")
        try:
            with open(file_path, 'r') as file:
                previous_word = ""
                second_previous_word = ""
                for line in file:
                    words = re.sub(r"[^a-zA-Z\s]", "", line.lower()).split()
                    for word in words:
                        if not word:
                            continue

                        # Build bigram
                        if previous_word:
                            self.bigram_count_map[previous_word][word] += 1

                        # Build trigram
                        if previous_word and second_previous_word:
                            key = f"{second_previous_word} {previous_word}"
                            self.trigram_count_map[key][word] += 1

                        # Shift words
                        second_previous_word = previous_word
                        previous_word = word
            print("N-gram processing completed.")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' does not exist.")

    def get_predictions(self, prefix, last_word=None, second_last_word=None):
        """
        Predicts the next word based on a prefix and context (bigram or trigram).
        """
        if second_last_word and last_word:
            predictions = self._get_trigram_predictions(prefix, second_last_word, last_word)
            if predictions:
                return predictions
        if last_word:
            predictions = self._get_bigram_predictions(prefix, last_word)
            if predictions:
                return predictions
        return self._get_unigram_predictions(prefix)

    def _get_unigram_predictions(self, prefix):
        """
        Suggests words based on the prefix, ignoring context.
        """
        suggestions = {word: 1.0 for word in self.bigram_count_map if word.startswith(prefix)}
        if not suggestions:
            print(f"No predictions available for prefix '{prefix}'.")
        return suggestions

    def _get_bigram_predictions(self, prefix, last_word):
        """
        Suggests words based on the last word (bigram context) and prefix.
        """
        candidates = self.bigram_count_map[last_word]
        total_count = sum(candidates.values())
        filtered_candidates = {word: count / total_count for word, count in candidates.items() if word.startswith(prefix)}

        if not filtered_candidates:
            print(f"No bigram predictions available for prefix '{prefix}' with last word '{last_word}'.")
        return filtered_candidates

    def _get_trigram_predictions(self, prefix, second_last_word, last_word):
        """
        Suggests words based on trigram context and prefix.
        """
        key = f"{second_last_word} {last_word}"
        candidates = self.trigram_count_map[key]
        total_count = sum(candidates.values())
        filtered_candidates = {word: count / total_count for word, count in candidates.items() if word.startswith(prefix)}

        if not filtered_candidates:
            print(f"No trigram predictions available for prefix '{prefix}' with last words '{second_last_word} {last_word}'.")
        return filtered_candidates


def main():
    # Initialize and load corpus
    predictor = NextWordPredictor()
    corpus_path = "check.txt"
    predictor.load_corpus(corpus_path)

    # Interactive Prediction
    while True:
        prefix = input("Enter a prefix for the next word: ").strip().lower()
        last_word = input("Enter the last word (optional): ").strip().lower()
        second_last_word = input("Enter the second last word (optional): ").strip().lower()

        predictions = predictor.get_predictions(prefix, last_word, second_last_word)
        if predictions:
            print(f"Predictions for prefix '{prefix}':")
            for word, probability in sorted(predictions.items(), key=lambda x: x[1], reverse=True):
                print(f"{word}: {probability:.2f}")
        else:
            print(f"No predictions available for prefix '{prefix}'.")

        # Exit condition
        cont = input("Do you want to continue? (y/n): ").strip().lower()
        if cont != 'y':
            break


if __name__ == "__main__":
    main()
