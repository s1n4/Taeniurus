#!/usr/bin/env python

#Project: Taeniurus irc bot  https://github.com/s1n4/Taeniurus
#No Spam module for detecing spammer

def detect_spammer(*spam):
    if not spam[0] or not spam[1]: return False; exit(0)
    spam = ' '.join(spam)
    kick_spammer = False

    def tmp_read():
        try:
            tmp = file('/tmp/DetectS-taeniurus').read()
            spam_tmp = tmp.splitlines()[0]
            counter = tmp.splitlines()[1]

        except IOError:
            spam_tmp = ''
            counter = '0'

        return spam_tmp, int(counter)

    def tmp_write(c):
        tmp = file('/tmp/DetectS-taeniurus', 'w')
        tmp.write(spam)
        tmp.write('\n')
        tmp.write(str(c))
        tmp.write('\n')
        tmp.close()


    spam_tmp, counter = tmp_read()

    if spam == spam_tmp:
        counter += 1

        if counter == 5:
            kick_spammer = True
            counter = 0

    else:
        counter = 0

    tmp_write(counter)

    return kick_spammer
