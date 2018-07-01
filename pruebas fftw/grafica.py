from scipy.fftpack import fft
import matplotlib.pyplot as plt

class test_fftw:
    dataFiles = None
    
    def __init__(self, nombreSensor):
        # archivo que se va leer las mediciones
        arch_acc = nombreSensor + "_Aceleracion.txt"             
        self.dataFiles = arch_acc            
           
    def getArrayMediciones(self):       
        try:
            arch = open(self.dataFiles, 'r')
            graph_data = arch.read()
            lines = graph_data.split('\n')
            arch.close()
            ejeXs = []
            ejeZs = []

            #archivo para guardar una variable
                  
            for line in lines:
                if len(line) > 1:
                    x, y, z, t = line.split(',')
##                    ejeXs.append(x)
                    ejeZs.append(z)
            return ejeZs #ejeXs
        
        except IOError:
            print("error grfica", IOError)

    def graficarfftw(self):
        # Number of sample points
        array = self.getArrayMediciones()
        N = len(array)
        print(N)
        return array
        
        # sample spacing
##        T = 1.0 / 800.0
##        x = np.linspace(0.0, N*T, N)
##        y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
##        yf = fft(y)
##        xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
##        
##        plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
##        plt.grid()
##        plt.show()
            
## PARA CORRER!!!
##x = test_fftw("sensor1")
##x.graficarfftw()

