#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word manipulation library

Jolyon Bloomfield, January 2018
"""

# Import the wordlist
with open("words.txt") as f:
    words = f.readlines()
words = [i.strip().lower() for i in words]
wordset = set(words)

def is_a_word(word):
    """Is word in the dictionary?"""
    return word in wordset

def contains_all_letters_in_word(word, contains):
    """Does word contain all of the letters in contains?"""
    word_set = set(word)
    for char in contains:
        if char not in word_set:
            return False
    return True

def find_words(text, minlength=3):
    """
    Look through text, and find all words contained inside.
    Eg, "AREDFG" contains the word "red".
    Only words with length minlength or more are reported.
    """
    results = []
    text = text.lower()
    for start in range(len(text) - 1):
        substring = text[start:]
        for end in range(minlength, len(substring)):
            test = substring[:end]
            if is_a_word(test):
                results.append(test)
    return results

