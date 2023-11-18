import os

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

def suggest_corrections(trie, word):
    suggestions = set()
    for key in trie.root.children:
        suggestions.update(suggest_corrections_helper(trie.root.children[key], key, word, 1))
    return suggestions

def suggest_corrections_helper(node, current_word, target_word, edits):
    suggestions = set()

    if node.is_end_of_word and edits <= 2:
        suggestions.add(current_word)

    if edits > 2 or len(target_word) <= len(current_word):
        return suggestions

    for key in node.children:
        next_word = current_word + key
        next_edits = edits + (len(target_word) > len(next_word) and target_word[len(next_word) - 1] != key)
        suggestions.update(suggest_corrections_helper(node.children[key], next_word, target_word, next_edits))

    return suggestions

def main():
    # Initialize Trie and load dictionary
    trie = Trie()
    with open('dictionary.txt', 'r') as file:
        for line in file:
            word = line.strip()
            trie.insert(word)

    # User input
    user_input = input("Enter a potentially misspelled word: ").lower()

    if trie.search(user_input):
        print(f'{user_input} is a valid word.')
    else:
        corrections = suggest_corrections(trie, user_input)
        print(f'Did you mean: {corrections} ')

class AutocorrectApp:
    def __init__(self):
        self.trie = Trie()
        self.dictionary_file = 'dictionary.txt'
        self.load_dictionary()

    def load_dictionary(self):
        if os.path.exists(self.dictionary_file):
            with open(self.dictionary_file, 'r') as file:
                for line in file:
                    word = line.strip()
                    self.trie.insert(word)

    def save_dictionary(self):
        with open(self.dictionary_file, 'w') as file:
            # Save each word in a new line
            for word in self.get_dictionary_words():
                file.write(word + '\n')

    def get_dictionary_words(self):
        words = set()

        def get_words_helper(node, current_word):
            if node.is_end_of_word:
                words.add(current_word)

            for key in node.children:
                next_word = current_word + key
                get_words_helper(node.children[key], next_word)

        get_words_helper(self.trie.root, '')
        return words

    def add_to_dictionary(self, word):
        self.trie.insert(word.lower())
        self.save_dictionary()

    def display_suggestions(self, word):
        corrections = suggest_corrections(self.trie, word)
        print(f'Did you mean: {corrections} ?')

    def run(self):
        while True:
            print("\n----- Autocorrect App -----")
            print("1. Check word")
            print("2. Add word to dictionary")
            print("3. Exit")

            choice = input("Enter your choice (1/2/3): ")

            if choice == '1':
                user_input = input("Enter a potentially misspelled word: ").lower()
                if self.trie.search(user_input):
                    print(f'{user_input} is a valid word.')
                else:
                    self.display_suggestions(user_input)

            elif choice == '2':
                new_word = input("Enter the word to add to the dictionary: ").lower()
                if new_word.isalpha():
                    self.add_to_dictionary(new_word)
                    print(f'{new_word} added to the dictionary.')
                else:
                    print("Invalid input. Only alphabetic characters are allowed.")

            elif choice == '3':
                print("Exiting Autocorrect App.")
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    app = AutocorrectApp()
    app.run()
