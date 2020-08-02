file=open(input(), "r")
info=file.readlines()
file.close()

for x in range(len(info)):
	if "HF=" in info[x]:
		line=info[x].strip() + info[x+1].strip()
		break

energy=""
count = line.find("HF=")+3
while line[count] != "\\":
	energy=energy+line[count]
	count=count+1
print(energy)