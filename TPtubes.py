import random
class Jadwal:
	def __init__(self, kode, kelas, jam_mulai, jam_akhir, durasi, hari):
		self.kode = kode
		self.kelas = kelas
		self.jam_mulai = jam_mulai
		self.jam_akhir = jam_akhir
		self.durasi = durasi
		self.hari = hari

class Ruangan:
	def __init__(self, kelas, jam_mulai, jam_akhir, hari):
		self.kelas = kelas
		self.jam_mulai = jam_mulai
		self.jam_akhir = jam_akhir
		self.hari = hari

class AssignedJadwal:
	def __init__(self, kode, kelas, durasi):
		self.kode = kode
		self.kelas = kelas
		self.durasi = durasi

def readFile(filename):
	listRuangan = []
	listJadwal = []
	with open(filename, 'r') as file:
		r = 0
		for line in file:
			line = line.strip()
			if "Ruangan" in line:
				r = 1
			elif "Jadwal" in line:
				r = 2
			elif (r == 1):
				ltemp = line.split(';')
				if len(ltemp) > 1:
					ruang = Ruangan(ltemp[0],ltemp[1],ltemp[2],ltemp[3].split(','))
					listRuangan.append(ruang)
			elif (r == 2):
				ltemp = line.split(';')
				if len(ltemp) > 1:
					jadwal = Jadwal(ltemp[0],ltemp[1],ltemp[2],ltemp[3],ltemp[4],ltemp[5].split(','))
					listJadwal.append(jadwal)
	file.close()
	return listRuangan, listJadwal

# HILL CLIMBING

def InitializedSchedule():
	ScheduleDay = []
	i = 0
	j = 0
	for i in range (0, 5):
		ScheduleTime = []
		for j in range (0, 12):
			ScheduleAssigned = []
			ScheduleTime.append(ScheduleAssigned)
			j = j + 1
		ScheduleDay.append(ScheduleTime)
		i = i + 1
	return ScheduleDay

def InitialRandom (listRuangan, listJadwal):
	ScheduleDay = InitializedSchedule()
	for jadwal in listJadwal:
		hari = random.randint(1, 5) - 1
		jam_mulai = (random.randint(7, 16)) - 7
		ruangkelas = listRuangan[random.randint(0, len(listRuangan)-1)].kelas
		Assign = AssignedJadwal(jadwal.kode, ruangkelas, 1)
		i = 0

		for i in range(0, int(jadwal.durasi)):
			(ScheduleDay[hari][jam_mulai + i]).append(Assign)
			i = i + 1
			Assign = AssignedJadwal(jadwal.kode, ruangkelas, 1 + i)
		
	return ScheduleDay

def Value (ScheduleTable, listRuangan, listJadwal):
	# menghitung banyaknya konstrain yang dilanggar, bentrok belum dihitung
	conflict = 0;

	i = 0
	j = 0
	for i in range (0, 5):
		for j in range (0, 12):
			if len(ScheduleTable[i][j]) > 1:
				for assign in ScheduleTable[i][j]:
					#cari index di ListJadwal dan ListRuangan
					p = 0
					q = 0
					while (assign.kode != listJadwal[p].kode and i < len(listJadwal)):
						p = p + 1;
					while (assign.kelas != listRuangan[q].kelas and j < len(listRuangan)):
						q = q + 1;

					if not ValidKodeRuangan(assign.kelas, listJadwal[p]):
						conflict = conflict + 1

					if assign.durasi == 1:
						if not ValidKodeJam (j+7, listJadwal[p]):
							conflict = conflict + assign.durasi
						if not ValidRuanganJam (j+7, listRuangan[q]):
							conflict = conflict + assign.durasi

					if not ValidKodeHari (i+1, listJadwal[p]):
						conflict = conflict + 1
					if not ValidRuanganHari (i+1, listRuangan[q]):
						conflict = conflict + 1
					print(assign.kode, assign.kelas, i, j)
					print(ValidKodeRuangan(assign.kelas, listJadwal[p]), ValidKodeJam (j+7, listJadwal[p]), ValidRuanganJam (j+7, listRuangan[q]), 
						ValidKodeHari (i+1, listJadwal[p]), ValidRuanganHari (i+1, listRuangan[q]))
			j = j + 1
		i = i + 1
	return conflict

def ValidKodeRuangan (Ruangan, Jadwal):
	if Jadwal.kelas == '-':
		return True
	if Jadwal.kelas == Ruangan:
		return True
	else: 
		return False

def ValidKodeJam (Jam_mulai, Jadwal):
	#print (Jadwal.jam_mulai)
	#Sprint (Jadwal.jam_akhir)
	print(Jam_mulai + int(Jadwal.durasi), int(Jadwal.jam_akhir))
	if (Jam_mulai < int(Jadwal.jam_mulai)) or (Jam_mulai > int(Jadwal.jam_akhir)):
		return False
	if Jam_mulai + int(Jadwal.durasi) <= int(Jadwal.jam_akhir):
		return True
	else:
		return False

def ValidKodeHari (Hari, Jadwal):
	if str(Hari) in Jadwal.hari:
		return True
	else: 
		return False

def ValidRuanganJam (Jam_mulai, Ruangan):
	if (Jam_mulai < int(Ruangan.jam_mulai)) or (Jam_mulai > int(Ruangan.jam_akhir)):
		return False
	else:
		return True

def ValidRuanganHari (Hari, Ruangan):
	#print (Hari)
	#print (Ruangan.hari)
	if str(Hari) in Ruangan.hari:
		return True
	else: 
		return False

def Collision (ScheduleDay):
	Coll = 0;
	i = 0
	j = 0
	for i in range (0, 5):
		for j in range (0, 12):
			if len(ScheduleDay[i][j]) > 1:
				print(i,j)
				x = 0
				for x in range(0, len(ScheduleDay[i][j])):
					print(ScheduleDay[i][j][x].kode, ScheduleDay[i][j][x].kelas, ScheduleDay[i][j][x].durasi)
					x = x + 1
				Coll = Coll + 1
			j = j + 1
		i = i + 1
	return Coll

# Driver
listRuangan, listJadwal = readFile("Testcase.txt")
ScheduleTable = InitialRandom(listRuangan, listJadwal)
print (Collision(ScheduleTable))
print(Value(ScheduleTable, listRuangan, listJadwal))

