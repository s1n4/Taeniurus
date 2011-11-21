#!/usr/bin/env python
#Filename: nospam.py
#Author: s1n4
#Project: Taeniurus
#No Spam Module to detecing spammer

def DetectSpammer(*spam) :
	if not spam[0] or not spam[1] : return False; exit(0)
	spam = ' '.join(spam)
	KickSpammer = False

	def TmpRead() :
		try :
			tmp = file('/tmp/DetectS-taeniurus').read()
			spam_tmp = tmp.splitlines()[0]
			counter = tmp.splitlines()[1]

		except IOError :
			spam_tmp = ''
			counter = '0'

		return spam_tmp, int(counter)

	def TmpWrite(c) :
		tmp = file('/tmp/DetectS-taeniurus', 'w')
		tmp.write(spam)
		tmp.write('\n')
		tmp.write(str(c))
		tmp.write('\n')
		tmp.close()


       	spam_tmp, counter = TmpRead()

       	if spam == spam_tmp :
       		counter += 1

       		if counter == 5 :
			KickSpammer = True
			counter = 0

	else :
		counter = 0

	TmpWrite(counter)

	return KickSpammer

