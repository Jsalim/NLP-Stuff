import sys, os
import nltk
from collections import defaultdict


def simp_tag(tag):
    '''Simplifies tags to brown-style'''
    return nltk.tag.simplify_brown_tag(tag)
