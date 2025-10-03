import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt  # Aseguramos tener plt importado

def interpol(x, p, nx):
    FI = InterpolatedUnivariateSpline(x[::-1], p[::-1])
    X = np.linspace(x[-1], x[0], nx)
    P = FI(X)
    return X[::-1], P[::-1]

def normalizador(in_file, out_file, dcp_min, dcp_max):
    M = np.loadtxt(f"{in_file}")
    py = np.array([])
    
    for i in range(len(M)):
        if i == 0:
            py = np.append(py, M[i,1])
        else:
            if M[i,1] != py[-1]:
                py = np.append(py, M[i,1])
                
    px = []
    pdcp = []
    Mx = M.copy()
    for j in range(len(py)):
        i=0
        pxy = np.array([])
        ppy = np.array([])
        while(1==1):
            if i == 0:
                pxy = np.append(pxy, Mx[i,0])
                ppy = np.append(ppy, Mx[i,2])
                i += 1
            else:
                if Mx[i,0] < pxy[-1]:
                    pxy = np.append(pxy, Mx[i,0])
                    ppy = np.append(ppy, Mx[i,2])
                    i += 1
                elif Mx[i,0] == pxy[-1]:
                    i += 1
                else:
                    break
            if i == len(Mx):
                break
        px.append(pxy)
        pdcp.append(ppy)
        Mx = np.delete(Mx, np.arange(i), axis=0)
    
    nx = 20
    
    XX = np.empty((0,nx))
    PP = np.empty((0,nx))
    
    for j in range(len(px)):
        X, P = interpol(px[j], pdcp[j], nx)  
        XX = np.row_stack((XX, X))
        PP = np.row_stack((PP, P))
    
    def scaler(W, wmin, wmax):
        Ws = (W-wmin)/(wmax-wmin)
        return Ws
    
    XN = np.empty((0, nx))
    
    for j in range(len(px)):
        Xs = scaler(XX[j], XX[j,-1], XX[j,0])
        XN = np.row_stack((XN, Xs))
    
    YN = np.empty((len(py), 0))
    
    for i in range(nx):
        Ys = scaler(py, py[0], py[-1])
        YN = np.column_stack((YN, Ys))
        
    #%%
    # Generar y guardar la imagen en formato PNG
    '''
    fig = plt.figure(1, figsize=(2, 2))
    ax = fig.add_subplot(111)
    ms = ax.pcolormesh(XN, YN, PP, vmin=-1.64, vmax=0, cmap='gray')
    plt.colorbar(ms)
    fig.tight_layout()
    '''
    # Guardar la figura en formato PNG
    fig = plt.figure(1, figsize=(2, 2))
    ax = fig.add_subplot(111)
    ms = ax.contourf(XN, YN, PP, vmin=dcp_min, 
                     vmax=dcp_max, levels=75, cmap='gray')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout()  
    ax.axis('off')
    ax.tick_params(labelbottom=False,
                    bottom=False,
                    labelleft=False,
                    left=False)
    fig.tight_layout()    
    fig.subplots_adjust(bottom = 0)
    fig.subplots_adjust(top = 1)
    fig.subplots_adjust(right = 1)
    fig.subplots_adjust(left = 0)
    
    fig.savefig(out_file, format='png', dpi=128)
    
    
    
    
    print(f"Imagen guardada exitosamente como: {out_file}")
    
    # Si también quieres mostrar la imagen (opcional)
   # plt.show()
    
