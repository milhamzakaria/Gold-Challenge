import re
def lowercase(text):
    return text.lower()

def remove_unnecessary_char(text):
    text = re.sub('\n',' ',text) # membuang semua '\n'
    text = re.sub('rt',' ',text) # membuang semua simbol retweet
    text = re.sub('user',' ',text) # membuang semua username
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # membuang semua URL
    text = re.sub('  +', ' ', text) # membuang ekstra spasi
    return text
    
def remove_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
    return text

