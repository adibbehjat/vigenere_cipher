# Brute Force Tutorial

# We need regex for checking purposes
import re
from itertools import combinations_with_replacement

# Step 1
## Develop a list, called letters, which contains all letters from A to Z in capitalized format
letters = "abcdefghijklmnopqrstuvwxyz"
letters = map(lambda x: x.upper(),letters)

# Step 2
## Develop a way to find the letters in a key, and reorganize them in a way where the key starts first, and the letters later
alpha_key = "thanks"

# Transform the key into upper case
alpha_key = map(lambda x: x.upper(),alpha_key)

# Letter List will hold the letters for our set that we will manipulate later
letter_list = list(letters)

# Will help the alphabets map for vigenere
alpha_map = []

# Loop through the key letters
for character in alpha_key:

	# Make sure it's a valid character
	if character in letters:

		# Pluck the letter from the letter_list
		if character in letter_list:

			# Locate the location of the letter
			i = letter_list.index(character)

			# Pop it from the letter list and add it into the alpha map
			alpha_map.append(letter_list.pop(i))

# Combine what is remaining from the letter list to the alpha map
alpha_map += letter_list

# Test the result
# print alpha_map

# Retrieve Media/Prose
passphrase = "WE COME FROM THE ERIDANUS SUPERVOID"

# Create a regex that only accepts non-alphabets and spaces
# How it's build is by building the condition for alphabets and spaces
# And then using the NOT element '^' which means all characters BUT NOT
# a-z and A-Z and space.
regex = re.compile('[^ a-zA-Z]')

# Strip out all non-alphabet characters using regex substitution
# In essence, substitute characters that match our regex above with
# '' (or blank)
passphrase = regex.sub('', passphrase)

# Ensure each word is listed individually and uppercased
passphrase = map(lambda x: x.upper(), passphrase.split(" "))

### TUTORIAL
# VIGENERE CIPHER METHOD
# ENCODING:
# Given key 'THANKS' and passphrase 'HELLO' and message 'ZOOLOGY'
# The output would be 'TZKABIC'
#
# How?
# Facts:

# The alphamap is our new letter mapping, which is listed as:
# ['T', 'H', 'A', 'N', 'K', 'S', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'L', 'M', 'O', 'P', 'Q', 'R', 'U', 'V', 'W', 'X', 'Y', 'Z']
# H is the 2nd (1st in list) letter of the alphabet in alphamap
# Z is the 26th (25th in the list) letter of the alphabet in alphamap
# 
# H + Z = ?
# print alpha_map.index("H")
# print alpha_map.index("Z")
# 1 + 25 = 26
# Since there are only 26 letters, we find the modulo:
# 26 % 26 = 0 (position of letter T in alphamap)
# But the first character is supposed to be T, which is 7 steps ahead.

class Vigenere:

	def __init__(self):
		self.LETTERS = "abcdefghijklmnopqrstuvwxyz"
		self.LETTERS = map(lambda x: x.upper(),self.LETTERS)

	# Develop Alpha Map
	def generateAlphaMap(self,key):

		# Transform the key into upper case
		alpha_key = map(lambda x: x.upper(),key)

		# Letter List will hold the letters for our set that we will manipulate later
		letter_list = list(self.LETTERS)

		# Will help the alphabets map for vigenere
		alpha_map = []

		# Loop through the key letters
		for character in alpha_key:

			# Make sure it's a valid character
			if character in self.LETTERS:

				# Pluck the letter from the letter_list
				if character in letter_list:

					# Locate the location of the letter
					i = letter_list.index(character)

					# Pop it from the letter list and add it into the alpha map
					alpha_map.append(letter_list.pop(i))

		# Combine what is remaining from the letter list to the alpha map
		alpha_map += letter_list

		# Return the result
		return alpha_map

	# A module that cleans up non-alphabet characters
	def cleanUp(self,element):
		# Create a regex that only accepts non-alphabets and spaces
		# How it's build is by building the condition for alphabets and spaces
		# And then using the NOT element '^' which means all characters BUT NOT
		# a-z and A-Z and space.
		regex = re.compile('[^ a-zA-Z]')

		# Strip out all non-alphabet characters using regex substitution
		# In essence, substitute characters that match our regex above with
		# '' (or blank)
		element = regex.sub('', element)

		return element

	# Develop Encryption Module
	def encrypt(self, message, key, passphrase, method = "Normal"):
		
		# Clean up passphrase
		passphrase = self.cleanUp(passphrase)

		# Record message into a new var
		message = message.upper()

		# Without spaces
		message_stripped = message.replace(" ","")

		# Get the length of the message
		length_of_message = len(message_stripped)

		# For keyed and normal vigenere, do special stuff
		if method == "Keyed" or method == "Autokey":
			
			# Generate an alphamap
			alphamap = self.generateAlphaMap(key)

		# With some math, repeat the passphrase over the course of the letter
		if method == "Keyed" or method == "Normal":
			if length_of_message > len(passphrase):
				size = length_of_message/len(passphrase)
				passphrase = size * passphrase + passphrase[:(length_of_message%len(passphrase))]

		# Setup for encryption
		encrypted_message = []

		# For looping purposes
		i = 0

		# Go through the index of each letter in the message
		for l in message:

			# If it's part of the alphabets, let's work on it
			if l in self.LETTERS:

				# Collect the information
				msg_letter = message_stripped[i].upper()
				pass_letter = passphrase[i].upper()

				# Do vig calculations
				if method == "Normal":

					# Normal vigenere
					vigIndex = (self.LETTERS.index(msg_letter) + self.LETTERS.index(pass_letter)) % 26
					
					# Find the letter based on vigIndex result
					msg_letter = self.LETTERS[vigIndex]

				elif method == "Keyed":
					# Keyed vigenere
					vigIndex = (alphamap.index(msg_letter) + alphamap.index(pass_letter)) % 26

					# Find the letter based on vigIndex result
					msg_letter = alphamap[vigIndex]

				elif method == "Autokey":
					# Autokey vigenere
					vigIndex = (alphamap.index(msg_letter) + alphamap.index(pass_letter)) % 26

					# Append message to the passphrase
					passphrase += msg_letter

					# Find the letter based on vigIndex result
					msg_letter = alphamap[vigIndex]

				# Push it as encrypted message
				encrypted_message.append(msg_letter)

				# Increment letter shifts
				i += 1

			else:
				# If it's non-alphabetical character, simply append
				encrypted_message.append(l)

		return "".join(encrypted_message)

	# Develop Decryption Module
	def decrypt(self, message, key, passphrase, method = "Normal"):
		
		# Clean up passphrase
		passphrase = self.cleanUp(passphrase)

		# Record message into a new var
		message = message.upper()

		# Without spaces
		message_stripped = message.replace(" ","")

		# Get the length of the message
		length_of_message = len(message_stripped)

		# For keyed and normal vigenere, do special stuff
		if method == "Keyed" or method == "Autokey":
			
			# Generate an alphamap
			alphamap = self.generateAlphaMap(key)

		# With some math, repeat the passphrase over the course of the letter
		if method == "Keyed" or method == "Normal":
			if length_of_message > len(passphrase):
				size = length_of_message/len(passphrase)
				passphrase = size * passphrase + passphrase[:(length_of_message%len(passphrase))]

		# Setup for encryption
		decrypted_message = []

		# For looping purposes
		i = 0

		# Go through the index of each letter in the message
		for l in message:

			# If it's part of the alphabets, let's work on it
			if l in self.LETTERS:

				# Collect the information
				msg_letter = message_stripped[i].upper()
				pass_letter = passphrase[i].upper()

				# Do vig calculations
				if method == "Normal":
					# Normal vigenere
					vigIndex = (self.LETTERS.index(msg_letter) - self.LETTERS.index(pass_letter)) % 26
					
					# Find the letter based on vigIndex result
					msg_letter = self.LETTERS[vigIndex]

				elif method == "Keyed":
					# Keyed vigenere
					vigIndex = (alphamap.index(msg_letter) - alphamap.index(pass_letter)) % 26

					# Find the letter based on vigIndex result
					msg_letter = alphamap[vigIndex]

				elif method == "Autokey":
					# Autokey vigenere
					vigIndex = (alphamap.index(msg_letter) - alphamap.index(pass_letter)) % 26

					# Find the letter based on vigIndex result
					msg_letter = alphamap[vigIndex]

					# Append the new letter to the passphrase
					passphrase += msg_letter

				# Push it as encrypted message
				decrypted_message.append(msg_letter)

				# Increment letter shifts
				i += 1

			else:
				# If it's non-alphabetical character, simply append
				decrypted_message.append(l)

		return "".join(decrypted_message)

	# Brute Force Decrypt
	def bruteForce(self, message, potential_passphrase, potential_answer, method = "Normal"):

		# Split into an array
		potential_passphrase = potential_passphrase.split()

		# Clean out any non-alphabetical characters
		potential_passphrase = map(self.cleanUp,potential_passphrase)

		# Strip out repeated words
		# "This sorts the set of all the (unique) words in your string by the word's index in the original list of words."
		# Source: https://stackoverflow.com/questions/7794208/how-can-i-remove-duplicate-words-in-a-string-with-python
		potential_passphrase = sorted(set(potential_passphrase), key = potential_passphrase.index)

		# Develop combination
		potential_combinations = combinations_with_replacement(potential_passphrase,5)

		# Potential Answer fix and upper
		potential_answer = self.cleanUp(potential_answer).upper()

		# Clean up encoded message
		message = self.cleanUp(message).upper()

		# # Brute force
		# # Develop combination of words
		for combination in potential_combinations:

			# At which step?
			step = 0

			# For each new combo, reset the message
			encoded_message = message

			# Go through each word in the combination
			for word in combination:

				# Pull the decoded message
				decoded = vig.decrypt(encoded_message,"t",word, method = method)

				if potential_answer == decoded:
					return combination, step
					break
				else:
					encoded_message = decoded

				step += 1

# # Check Code
# vig = Vigenere()
# new_msg = vig.encrypt("ZOOLOGY IS AWESOME","thanks","hello", method = "Autokey")
# print new_msg
# org_msg = vig.decrypt(new_msg,"thanks","hello", method = "Autokey")
# print org_msg

#### BRUTE FORCE MECHANISM ####

# Capture potential passphrase
vig = Vigenere()
potential_passphrase = "WE COME FROM THE ERIDANUS SUPERVOID"
potential_answer = "trialists"
message = "ydhjerbbp"
method = "Autokey"

result = vig.bruteForce(message,potential_passphrase,potential_answer, method = method)

print "The combination that works is {}, it terminated at work {}".format(result[0], result[0][result[1]])