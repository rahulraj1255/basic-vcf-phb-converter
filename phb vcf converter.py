import os
from sys import argv
inpf,outf=argv[1:]
fread=open(inpf)
fprint=open(outf,'w')
cvt='phb'
for i in fread:
	if i[0:-2] == "BEGIN:VCARD":
		print "Converting a VCF file to PHB format"
		cvt='vcf'		
	else :
		print "Converting a PBP file to VCF format"
	break
fread.close()
fread=open(inpf)
print "Contacts in the file, "+inpf+" :\r\n"
if cvt== 'vcf' :
	for i in fread :
		if i[0:2]=='FN':
			name=''
			bool1=False
			for char in i :
				if bool1 :
					name=name+char
				if char==':' :
					bool1=True 
			print name+"\n"
			fprint.write(name)
		elif i[0:3]=='TEL' :
			fprint.write(i)
else :
	run=False
	lastend=False
	for line in fread :
		if len(line)>2 :
			if line[0:3]!='TEL':
				if run :
					fprint.write("END:VCARD\r\n")
				run=True
				lastend=True
				fprint.write("BEGIN:VCARD\r\nVERSION:2.1\r\n")
				print line[:-4]
				splitted=line.split()
				start,end=['','']
				if len(splitted) >1 :
					start=splitted[-1]
					if splitted[0] in ['Mr','Mrs','Dr'] :
						end =splitted[0]
					middle=''
					for i in range(0,len(splitted)-1) :
						if i==0 and end != '' :
							continue 
						if middle == '' :
							middle=splitted[i]
							continue
						middle=middle+' '+splitted[i]
					if end !='' :
						fprint.write('N:'+start+';'+middle+';'+end+'\r\n')
					else :
						fprint.write('N:'+start+';'+middle+'\r\n')
				fprint.write('FN:'+line)
			else :
				fprint.write(line)
	if lastend :
		fprint.write("END:VCARD\r\n")
fprint.close()
fread.close()
