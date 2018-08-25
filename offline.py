import os

word = 'This is the earth'
translation = os.popen('dict -d fd-eng-deu ' + word).read()
print(translation)
