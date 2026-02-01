def stutter(word):
	word_part = word[:2]
	stuttered_word =  f"{word_part}... {word_part}... {word}?"
	return stuttered_word
print(stutter("incredible"))