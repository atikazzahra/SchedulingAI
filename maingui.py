import sys, random, copy, math, operator
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
						successor[i].hari = successor[i].domain_hari[random.randrange(0,len(successor[i].domain_hari))]
				elif conflictJamMatkul(list_matkul[i], list_matkul[j]):
					while (successor[i].jam_mulai == successor[j].jam_mulai):
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
						successor[i].hari = successor[i].domain_hari[random.randrange(0,len(successor[i].domain_hari))]
				else: 
					successor[i].kelas = successor[i].domain_kelas[random.randrange(0,len(successor[i].domain_kelas))]
			if conflictJamRuangan(successor[i], ruangan):
				if ruangan.jam_mulai in successor[i].domain_jam_mulai:
					while conflictJamRuangan(successor[i], ruangan):
						successor[i].jam_mulai = successor[i].domain_jam_mulai[random.randrange(0,len(successor[i].domain_jam_mulai))]
				else: 
					successor[i].kelas = successor[i].domain_kelas[random.randrange(0,len(successor[i].domain_kelas))]	
	return successor

#SA
def searchNeighbour(list_matkul,list_ruangan):
	successor = copySpecies(list_matkul)
	i = random.randrange(0,(len(list_matkul)))
	successor[i].kelas = successor[i].domain_kelas[random.randrange(0,len(successor[i].domain_kelas))]
	successor[i].hari = successor[i].domain_hari[random.randrange(0,len(successor[i].domain_hari))]
	successor[i].jam_mulai = successor[i].domain_jam_mulai[random.randrange(0,len(successor[i].domain_jam_mulai))]

	return successor

def SHC(list_matkul,list_ruangan):
	successor = copySpecies(list_matkul)
	i = random.randrange(0,(len(list_matkul)))
	j = random.randrange(0,(len(list_matkul)))
	while (i==j):
		i = random.randrange(1,(len(list_matkul)))
		j = random.randrange(1,(len(list_matkul)))
	if checkConstraintMatkul(list_matkul[i], list_matkul[j]) != 0:
		if conflictHariMatkul(list_matkul[i], list_matkul[j]):
				successor[i].hari = successor[i].domain_hari[random.randrange(0,len(successor[i].domain_hari))]
		elif conflictJamMatkul(list_matkul[i], list_matkul[j]):
					while (successor[i].jam_mulai == successor[j].jam_mulai):
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
					successor[i].hari = successor[i].domain_hari[random.randrange(0,len(successor[i].domain_hari))]
			else: 
				successor[i].kelas = successor[i].domain_kelas[random.randrange(0,len(successor[i].domain_kelas))]

		if conflictJamRuangan(successor[i], ruangan):
			if ruangan.jam_mulai in successor[i].domain_jam_mulai:
				while conflictJamRuangan(successor[i], ruangan):
					successor[i].jam_mulai = successor[i].domain_jam_mulai[random.randrange(0,len(successor[i].domain_jam_mulai))]
			else: 
				successor[i].kelas = successor[i].domain_kelas[random.randrange(0,len(successor[i].domain_kelas))]	

	return successor

def probability(E,Ei,T):
	p = math.exp(-(E-Ei)/T)
	p = abs(p)
	p=p*100
	if (p>100):
		p = 100
	return p

#GA
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
	nspecies1 = copySpecies(species1[:lenr]) + copySpecies(species2[lenr:])
	nspecies2 = copySpecies(species2[:lenr]) + copySpecies(species1[lenr:])
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
			if (line == 'Ruangan\n'):
				r = 1
			elif (line == 'Jadwal\n'):
				r = 2
			elif (line == '\n'):
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


# Main Graphic User Interface
class MainWindow(QWidget):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		
		# Layout Type
		grid = QGridLayout()
		grid.setSpacing(10)
		
		# Font
		font = QFont()
		font.setPointSize(8)
		
		# Open File Button (TBD)
		self.fopenbut = QPushButton('Open File...')
		grid.addWidget(self.fopenbut, 1, 0)
		QObject.connect(self.fopenbut, SIGNAL("clicked()"), self.choose_file)

		# Label Misc.
		self.choosealg = QLabel('Choose Method:')
		self.choosealg.setFont(font)
		grid.addWidget(self.choosealg, 1, 1)
		self.consbroken = QLabel('Constraint Broken:')
		self.consbroken.setFont(font)
		grid.addWidget(self.consbroken, 5, 2)
		
		# Define Main Table
		self.table = QTableWidget()
		self.table.setRowCount(11)
		self.table.setColumnCount(5)
		self.table.setHorizontalHeaderLabels(['Senin','Selasa','Rabu','Kamis','Jumat'])
		self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.table.verticalHeader().setResizeMode(QHeaderView.Stretch)
		self.table.setVerticalHeaderLabels(['07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00'])
		grid.addWidget(self.table, 0, 0, 1, 3)
		
		# Run Push Button
		self.runbut = QPushButton('Run!')
		grid.addWidget(self.runbut, 5, 1)
		
		# Radio Button
		self.rb1 = QRadioButton('Hill Algorithm')
		self.rb1.setFont(font)
		self.rb1.setChecked(True)
		grid.addWidget(self.rb1, 2, 1)
		self.rb2 = QRadioButton('Simulated Annealing')
		self.rb2.setFont(font)
		grid.addWidget(self.rb2, 3, 1)
		self.rb3 = QRadioButton('Genetic Algorithm')
		self.rb3.setFont(font)
		grid.addWidget(self.rb3, 4, 1)
		
		# Window Layout Modifier
		self.setLayout(grid)
		self.setGeometry(300, 100, 800, 600)
		self.setWindowTitle("Scheduling Mata Kuliah")
		self.show()
		
		self.checkRadioState()

	# Check Radio Button Checked, prepare to Run Button Pushed
	def checkRadioState(self):
		if self.rb1.isChecked():
			print "BUTTON 1"
			self.runbut.clicked.connect(self.setTableContentGA)
		elif self.rb2.isChecked():
			print "BUTTON 2"
			self.runbut.clicked.connect(self.setTableContentGA)
		elif self.rb3.isChecked():
			print "BUTTON 3"
			self.runbut.clicked.connect(self.setTableContentGA)

	# Fill the Table with Data according to Algorithm selected
	def setTableContentGA(self):
		varMatkul = geneticAlgorithm()
		self.table.clear()
		for i in range (len(varMatkul[0])):
			jammulai = varMatkul[0][i].jam_mulai
			start = abs(7-jammulai) #biar indexnya pas
			lama = varMatkul[0][i].durasi #banyaknya pengulangan buat nyetak
			if (varMatkul[0][i].hari == 1):
				for j in range (0, lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 0, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 2):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 1, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 3):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 2, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 4):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 3, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 5):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 4, QTableWidgetItem(soda))
					start = start+1

	def setTableContentSA(self):
		varMatkul = simulatedAnnealing()
		self.table.clear()
		for i in range (len(varMatkul[0])):
			jammulai = varMatkul[0][i].jam_mulai
			start = abs(7-jammulai) #biar indexnya pas
			lama = varMatkul[0][i].durasi #banyaknya pengulangan buat nyetak
			if (varMatkul[0][i].hari == 1):
				for j in range (0, lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 0, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 2):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 1, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 3):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 2, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 4):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 3, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 5):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 4, QTableWidgetItem(soda))
					start = start+1

	def setTableContentHill(self):
		varMatkul = hillAlgorithm()
		self.table.clear()
		for i in range (len(varMatkul[0])):
			jammulai = varMatkul[0][i].jam_mulai
			start = abs(7-jammulai) #biar indexnya pas
			lama = varMatkul[0][i].durasi #banyaknya pengulangan buat nyetak
			if (varMatkul[0][i].hari == 1):
				for j in range (0, lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 0, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 2):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 1, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 3):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 2, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 4):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 3, QTableWidgetItem(soda))
					start = start+1
			elif (varMatkul[0][i].hari == 5):
				for j in range (0,lama):
					soda = varMatkul[0][i].kode + '  -  ' + varMatkul[0][i].kelas
					self.table.setItem(start, 4, QTableWidgetItem(soda))
					start = start+1

	# File Open Window Dialogue	
	def choose_file(self):
		file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Text document (*.txt)")

# GA Selected, return varMatkul		
def geneticAlgorithm():
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
	return fittestSpecies

# Hill Selected, return
def hillAlgorithm():
	problem = createSpecies(listJadwal, listRuangan)
	current = copySpecies(problem)
	neighboor = highestValueNeighboor(current, listRuangan)
	while(checkConstraint(current, listRuangan) > checkConstraint(neighboor, listRuangan)):
		current = copySpecies(neighboor)
		neighboor = highestValueNeighboor(current, listRuangan)
	problem = copySpecies(current)
	for i in range(len(problem)):
		problem[i].print_jadwal()
	print 'constraintBroken: ' + str(checkConstraint(problem, listRuangan))
	print('\n')
	return problem

# SA Selected, return
def simulatedAnnealing():
	T = 100
	current = createSpecies(listJadwal, listRuangan)
	neighbour = searchNeighbour(current, listRuangan)
	if (checkConstraint(current,listRuangan)>=checkConstraint(neighbour,listRuangan)):
			best = copySpecies(neighbour)
			current = copySpecies(neighbour)
	else:
		best = copySpecies(current)

	#mulai SA algorithm
	#Random Walk
	while (T>0.0001) and (checkConstraint(best,listRuangan)!=0):
		neighbour=searchNeighbour(current,listRuangan)
		E = checkConstraint(current,listRuangan)
		Ei = checkConstraint(neighbour,listRuangan)
		if (E>=Ei):
			if (checkConstraint(best,listRuangan)>=checkConstraint(neighbour,listRuangan)):		
				best = copySpecies(neighbour)
			current = copySpecies(neighbour)
		elif(T!=0):																				#kalo bad move
			p = probability(E,Ei,T)
			r = operator.div(100,p)
			if (r!=1):
				r = random.randrange(1,r)
			if (r==1):
				current = copySpecies(neighbour)
		T = T-0.01

	#memulai Stochastic Hill Climbing
	if (checkConstraint(best,listRuangan)>0):
		neighbour = SHC(best,listRuangan)
		while (checkConstraint(best,listRuangan)>(checkConstraint(neighbour,listRuangan))):
			best = copySpecies(neighbour)
			neighbour = SHC(best,listRuangan)

	for i in range(len(best)):
		best[i].print_jadwal()
	print 'constraintBroken: ' + str(checkConstraint(best,listRuangan))
	return best


# Main Program
def main():	
	#Window
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
