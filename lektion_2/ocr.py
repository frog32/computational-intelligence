from numpy import tanh, array
from scipy import optimize

VERDECKTE_NODES = 5
EINGAENGE = 64
AUSGAENGE = 10


tra = arra


data_x_mean = data_x.mean(0)
data_x_std = maximum(data_x.std(0), 1)
data_x = ((data_x-tile(Xmean, (n,1)))/tile(Xstd,(n,1))).T

def my_ocr(weights, inputs):
    output_verdeckt = [
                tanh(sum([weights[i + j * EINGAENGE] * inputs[j]
            for j in EINGAENGE]))
        for i in xrange(VERDECKTE_NODES)]
    return [tanh(sum(
                output_verdeckt[i] * weights[i + number * AUSGAENGE + VERDECKTE_NODES * EINGAENGE]
            for i in xrange(VERDECKTE_NODES)
            ))
        for number in range(AUSGAENGE)
        ]

error = lambda weights, x, y: array(my_ocr(weights, x)) - array([y == i and 1 or -1 for i in range(AUSGAENGE)])   

start_weights = randn(VERDECKTE_NODES * EINGAENGE + VERDECKTE_NODES * AUSGAENGE)

optimize.leastsq(my_ocr, start_weights, args=(X, Y), xtol=1e-2)
