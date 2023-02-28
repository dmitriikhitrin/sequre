from qiskit import QuantumCircuit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from math import pi
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_histogram, plot_state_city
import random

def binaryToDecimal(binary):
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

def createCircuit(numUsers, QECQubits, registers):
    users = QuantumRegister(numUsers, "user")
    ancillas = QuantumRegister(QECQubits, "ancilla")
    cr = ClassicalRegister(registers, 'c')
    qc = QuantumCircuit(users, ancillas, cr)
    return qc

numUsers = 3
QECQubits = 1
registers = 3
def initializeDialog(userIn):
    qc = createCircuit(numUsers, QECQubits, registers)
    qc.h(userIn)
    return qc

def enterDialog(userIn, userEn):
    qc = initializeDialog(userIn)
    qc.cnot(userIn, userEn)
    return qc

def closeDialog(qc, userIn, userEn):
    qc.reset(userIn)
    qc.reset(userEn)
    return qc

def errorX(qc, userIn, userEn):
    qc.rx(random.random()*pi/2, userIn) 
    qc.rx(random.random()*pi/2, userEn)
    return qc

def errorCorrection(qc, userIn, userEn, QECQubit):
    qc.cnot(userIn, QECQubit)
    qc.cnot(userEn, QECQubit)
    return qc

def getPrivateKeys(userIn, userEn, QECQubit, keyLength):
    qc = enterDialog(userIn, userEn)
    
    qc.barrier()
    qc = errorX(qc, userIn, userEn)
    qc.barrier()
    
    qc = errorCorrection(qc, userIn, userEn, QECQubit)
    qc.barrier()
    qc.measure([userIn, userEn, QECQubit], [0,1,2])
    
    lstIn = []
    lstEn = []
    counts = []
    
    
    while len(lstEn) <= keyLength:
        backend = Aer.get_backend('qasm_simulator')
        job_sim = execute(qc, backend, shots = 1)
        result = job_sim.result()
        count = result.get_counts(qc)
        counts.append(count)
        if (int(list(count.keys())[0][0]) == 0):
            lstIn.append(list(count.keys())[0][registers-userIn-1])
            lstEn.append(list(count.keys())[0][registers-userEn-1])

    
    if (len(lstIn) != 0 and len(lstEn) != 0):
        if lstIn[0] == 0:
            lstIn = lstIn[1:]
        if lstEn[0] == 0:
            lstEn = lstEn[1:]
        keyIn = binaryToDecimal(int("".join(lstIn)))
        keyEn = binaryToDecimal(int("".join(lstEn)))

    return keyIn, keyEn
    
    
#     qc.draw('mpl')
#     plot_histogram(count)
    return (keyIn, keyEn)

result = getPrivateKeys(0, 1, 3, 16)
print(result)
