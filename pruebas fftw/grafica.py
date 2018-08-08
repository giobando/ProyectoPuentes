from scipy.fftpack import fft
import matplotlib.pyplot as plt

class test_fftw:
    dataFiles = None
    
    def __init__(self, nombreSensor):
        # archivo que se va leer las mediciones
        arch_acc = "sensor_"+nombreSensor + "_Aceleracion.txt"             
        self.dataFiles = arch_acc            
           
    def getArrayMediciones(self):       
        try:
            arch = open(self.dataFiles, 'r')
            graph_data = arch.read()
            lines = graph_data.split('\n')
            arch.close()
            ejeXs = []
            ejeYs = []
            ejeZs = []
            ejeRMS = []
            ejeTime = []
                
            for line in lines: # archivo para guardar una variable  
                if len(line) > 1:
                    x, y, z, rms, t = line.split(',')
                    ejeXs.append(x)
                    ejeYs.append(y)
                    ejeZs.append(z)
                    ejeTime.append(t)
                    ejeRMS.append(rms)                    
            return {"x":ejeXs, "y":ejeYs, "z":ejeZs, "rms":ejeRMS, "time":ejeTime}
        except IOError:
            print("error", IOError)
            

