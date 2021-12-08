import os
from pathlib import Path

from sepal_ui.translator import Translator

# the sepal_ui allows you to create a translation interface
# at the moment this variable is not yet available but it's a good practice to build your app translatio-ready

# first select the language env variable to load the destination locale
# it will default to en
lang = "en"
if "CUSTOM_LANGUAGE" in os.environ:
    lang = os.environ["CUSTOM_LANGUAGE"]

# create a ms object that will be used to translate all the messages
# the base language is english and every untranslated messages will be fallback to the english key
# complete the json file the add keys in the app
# avoid hard written messages at all cost
cm = Translator(Path(__file__).parent, lang)
