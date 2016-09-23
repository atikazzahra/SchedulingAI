import random, copy

class Jadwal:
	def __init__(self, kode, kelas, jam_mulai, jam_akhir, durasi, hari):
		self.kode = kode
		self.kelas = kelas
		self.jam_mulai = int(jam_mulai[:2])
		self.jam_akhir = int(jam_akhir[:2])
		self.durasi = int(durasi)
		self.hari = [int(h) for h in hari] 

class Ruangan:
	def __init__(self, kelas, jam_mulai, jam_akhir, hari):
		self.kelas = kelas
		self.jam_mulai = int(jam_mulai[:2])
		self.jam_akhir = int(jam_akhir[:2])
		self.hari = [int(h) for h in hari] 

class varMatkul:
	def __init__(self, jadwal, list_ruangan):
		self.kode = jadwal.kode
		if (jadwal.kelas == '-'):
			self.domain_kelas = [(list_ruangan[i].kelas) for i in range(len(list_ruangan))]
		else:
			self.domain_kelas = [jadwal.kelas]
		self.domain_jam_mulai = [(jadwal.jam_mulai+i) for i in range(jadwal.jam_akhir-jadwal.jam_mulai-jadwal.durasi+1)]
		self.domain_hari = jadwal.hari
		self.kelas = self.domain_kelas[random.randrange(0,len(self.domain_kelas))]
		self.jam_mulai = self.domain_jam_mulai[random.randrange(0,len(self.domain_jam_mulai))]
		self.hari = self.domain_hari[random.randrange(0,len(self.domain_hari))]
		self.durasi = jadwal.durasi
	def mutate(self, mutate_chance):
		if (int(random.random() * mutate_chance) == 1):
			if (int(random.random() * 2) == 1):
				self.kelas = self.domain_kelas[random.randrange(0,len(self.domain_kelas))]
			if (int(random.random() * 2) == 1):
				self.jam_mulai = self.domain_jam_mulai[random.randrange(0,len(self.domain_jam_mulai))]
			if (int(random.random() * 2) == 1):
				self.hari = self.domain_hari[random.randrange(0,len(self.domain_hari))]
	def print_jadwal(self):
		print self.kode, self.kelas, self. jam_mulai, self.jam_mulai+self.durasi, self.hari
					

def createSpecies(list_jadwal, list_ruangan):
	list_matkul = []
	for jadwal in list_jadwal:
		list_matkul.append(varMatkul(jadwal, list_ruangan))
	return list_matkul

def createPopulation(list_jadwal, list_ruangan):
	numSpecies = 100
	population = []
	for i in range(numSpecies):
		species = createSpecies(list_jadwal, list_ruangan)
		population.append([species,checkConstraint(species, list_ruangan)])
	return population

# Validasi conflict untuk nyari neighboor
def conflictHariMatkul(matkul1, matkul2):
	if (matkul1.hari == matkul2.hari):
		return True
	else:
		return False

def conflictJamMatkul(matkul1, matkul2):
	if (matkul1.jam_mulai >= matkul2.jam_mulai and matkul1.jam_mulai < matkul2.jam_mulai+matkul2.durasi) or (matkul2.jam_mulai >= matkul1.jam_mulai and matkul2.jam_mulai < matkul1.jam_mulai+matkul1.durasi):
		return True
	else:
		return False

def conflictHariRuangan(matkul, ruangan):
	if (matkul.hari not in ruangan.hari):
		return True
	else:
		return False

def conflictJamRuangan(matkul, ruangan):
	if (matkul.jam_mulai < ruangan.jam_mulai) or (matkul.jam_mulai+matkul.durasi > ruangan.jam_akhir):
		return True
	else:
		return False

def checkConstraintMatkul(matkul1, matkul2):
	constraintBroken = 0
	if (matkul1.hari == matkul2.hari and matkul1.kelas == matkul2.kelas):
		if (matkul1.jam_mulai >= matkul2.jam_mulai and matkul1.jam_mulai < matkul2.jam_mulai+matkul2.durasi):
			constraintBroken = 1
		if (matkul2.jam_mulai >= matkul1.jam_mulai and matkul2.jam_mulai < matkul1.jam_mulai+matkul1.durasi):
			constraintBroken = 1
	return constraintBroken	

def checkConstraintRuang(matkul, list_ruangan):
	constraintBroken = 0
	ruangan = 0
	for ruang in list_ruangan:
		if (ruang.kelas == matkul.kelas):
			ruangan = ruang
			break
	if (matkul.hari not in ruangan.hari):
		constraintBroken = 1
	else:
		if (matkul.jam_mulai < ruangan.jam_mulai):
			constraintBroken = 1
		if (matkul.jam_mulai+matkul.durasi > ruangan.jam_akhir):
			constraintBroken = 1
	return constraintBroken

def checkConstraint(list_matkul, list_ruangan):
	totalConstraintBroken = 0
	for i in range(len(list_matkul)):
		totalConstraintBroken += checkConstraintRuang(list_matkul[i],list_ruangan)
		for j in range(i+1, len(list_matkul)):
			totalConstraintBroken += checkConstraintMatkul(list_matkul[i],list_matkul[j])
	return totalConstraintBroken

def copySpecies(species):
	new_species = []
	for i in range(len(species)):
		new_species.append(copy.copy(species[i]))
	return new_species
	
#HILL CLIMBING
def highestValueNeighboor(list_matkul, list_ruangan):
	successor = copySpecies(list_matkul)
	for i in range(len(list_matkul)):
		for j in range(i+1, len(list_matkul)):
			if checkConstraintMatkul(list_matkul[i], list_matkul[j]) != 0:
				if conflictHariMatkul(list_matkul[i], list_matkul[j]):
					while (successor[i].hari == successor[j].hari):
						print ("a")
						successor[i].hari = successor[i].domain_hari[random.randrange(0,len(successor[i].domain_hari))]
				elif conflictJamMatkul(list_matkul[i], list_matkul[j]):
					while (successor[i].jam_mulai == successor[j].jam_mulai):
						print successor[i].domain_jam_mulai
						print successor[i].kode
						print ("b", successor[i].jam_mulai)
						successor[i].jam_mulai = successor[i].domain_jam_mulai[random.randrange(0,len(successor[i].domain_jam_mulai))]
		
		if checkConstraintRuang(successor[i], list_ruangan) != 0:
			ruangan = 0
			for ruang in list_ruangan:
				if (ruang.kelas == list_matkul[i].kelas):
					ruangan = ruang
					break

			if conflictHariRuangan(list_matkul[i], ruangan):
				if sameValueinLists(ruangan.hari, successor[i].domain_hari):
					while (successor[i].hari not in ruangan.hari):
						print successor[i].domain_hari
						print successor[i].kode
						print ("c", successor[i].hari)
						successor[i].hari = successor[i].domain_hari[random.randrange(0,len(successor[i].domain_hari))]
				else: 
					successor[i].kelas = successor[i].domain_kelas[random.randrange(0,len(successor[i].domain_kelas))]
			if conflictJamRuangan(successor[i], ruangan):
				if ruangan.jam_mulai in successor[i].domain_jam_mulai:
					while conflictJamRuangan(successor[i], ruangan):
						print successor[i].domain_jam_mulai
						print successor[i].kode
						print ("d", successor[i].jam_mulai, ruangan.jam_mulai)
						successor[i].jam_mulai = successor[i].domain_jam_mulai[random.randrange(0,len(successor[i].domain_jam_mulai))]
				else: 
					successor[i].kelas = successor[i].domain_kelas[random.randrange(0,len(successor[i].domain_kelas))]	
	return successor

def sameValueinLists(list1, list2):
	for x in list1:
		if x in list2:
			return True
	return False

def fitnessTest(populasi):
	fitSpecies = []
	populasi.sort(key=lambda x: x[1])
	for i in range(10):
		species = [copySpecies(populasi[i][0]),populasi[i][1]]
		fitSpecies.append(species)
	return fitSpecies

def crossing(species1, species2):
	lenr = random.randrange(0, len(species1))
	nspecies1 = copySpecies(species1[lenr:]) + copySpecies(species2[:lenr])
	nspecies2 = copySpecies(species2[lenr:]) + copySpecies(species1[:lenr])
	return nspecies1, nspecies2

def mutation(population, list_ruangan):
	mutation_chance = len(population)
	for i in range(len(population)):
		for j in range(len(population[i][0])):
			population[i][0][j].mutate(mutation_chance)
		population[i][1] = checkConstraint(population[i][0], list_ruangan)
	
def readFile(filename):
	listRuangan = []
	listJadwal = []
	with open(filename) as file:
		r = 0
		for line in file:
			if (line == 'Ruangan\r\n'):
				r = 1
			elif (line == 'Jadwal\r\n'):
				r = 2
			elif (line == '\r\n'):
				pass
			elif (r == 1):
				ltemp = line[:-1].split(';')
				ruang = Ruangan(ltemp[0],ltemp[1],ltemp[2],ltemp[3].split(','))
				listRuangan.append(ruang)
			elif (r == 2):
				ltemp = line[:-1].split(';')
				jadwal = Jadwal(ltemp[0],ltemp[1],ltemp[2],ltemp[3],ltemp[4],ltemp[5].split(','))
				listJadwal.append(jadwal)
	return listRuangan, listJadwal

def main():
	print("GA")
	listRuangan, listJadwal = readFile('Testcase.txt')
	fitSpecies = []
	for i in range(50):
		population = createPopulation(listJadwal, listRuangan)
		population += fitSpecies
		fitSpecies = fitnessTest(population)
		fittestSpecies = [copySpecies(fitSpecies[0][0]),fitSpecies[0][1]]
		population = []
		for i in range(len(fitSpecies)):
			for j in range(i,len(fitSpecies)):
				tempSpecies1, tempSpecies2 = crossing(fitSpecies[i][0],fitSpecies[j][0])
				population.append([tempSpecies1, checkConstraint(tempSpecies1, listRuangan)]) 
				population.append([tempSpecies2, checkConstraint(tempSpecies2, listRuangan)])
		population.append(fittestSpecies)
		population.sort(key=lambda x: x[1])
		fittestSpecies = [copySpecies(population[0][0]),population[0][1]]
		mutation(population, listRuangan)
		population.append(fittestSpecies)
		population.sort(key=lambda x: x[1])
		fittestSpecies = [copySpecies(population[0][0]),population[0][1]]
		fitSpecies = fitnessTest(population)
	for i in range(len(fittestSpecies[0])):
		fittestSpecies[0][i].print_jadwal()
	print 'Constraint broken: ' + str(fittestSpecies[1])
	print 'Constraint broken: ' + str(checkConstraint(fittestSpecies[0], listRuangan))

	print("HILL")
	problem = createSpecies(listJadwal, listRuangan)
	current = copySpecies(problem)
	neighboor = highestValueNeighboor(current, listRuangan)
	print "current:", checkConstraint(current, listRuangan), "neighboor:", checkConstraint(neighboor, listRuangan)
	while(checkConstraint(current, listRuangan) > checkConstraint(neighboor, listRuangan)):
		print "current:", checkConstraint(current, listRuangan), "neighboor:", checkConstraint(neighboor, listRuangan)
		current = copySpecies(neighboor)
		neighboor = highestValueNeighboor(current, listRuangan)
	problem = copySpecies(current)
	for i in range(len(problem)):
		problem[i].print_jadwal()
	print 'constraintBroken: ' + str(checkConstraint(problem, listRuangan))

if __name__ == '__main__':
	main()
