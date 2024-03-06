# https://jneuroengrehab.biomedcentral.com/articles/10.1186/s12984-015-0090-9?report=reader
# https://github.com/siva82kb/SPARC/blob/master/scripts/smoothness.py

import numpy as np
from FeatureClass import DataPreparation, Features
import matplotlib.pyplot as plt

FilteredData = DataPreparation()
DataFeatures = Features(FilteredData)
SAMPLE_FREQ = FilteredData.Sample_Freq

SAMPLE_FREQ = 104


def sparc(movement, fs, padlevel=4, fc=10.0, amp_th=0.05):
    """
    Calcualtes the smoothness of the given speed profile using the modified
    spectral arc length metric.

    Parameters
    ----------
    movement : np.array
               The array containing the movement speed profile.
    fs       : float
               The sampling frequency of the data.
    padlevel : integer, optional
               Indicates the amount of zero padding to be done to the movement
               data for estimating the spectral arc length. [default = 4]
    fc       : float, optional
               The max. cut off frequency for calculating the spectral arc
               length metric. [default = 10.]
    amp_th   : float, optional
               The amplitude threshold to used for determing the cut off
               frequency upto which the spectral arc length is to be estimated.
               [default = 0.05]

    Returns
    -------
    sal      : float
               The spectral arc length estimate of the given movement's
               smoothness.
    (f, Mf)  : tuple of two np.arrays
               This is the frequency(f) and the magntiude spectrum(Mf) of the
               given movement data. This spectral is from 0. to fs/2.
    (f_sel, Mf_sel) : tuple of two np.arrays
                      This is the portion of the spectrum that is selected for
                      calculating the spectral arc length.

    Notes
    -----
    This is the modfieid spectral arc length metric, which has been tested only
    for discrete movements.
    """
    # Number of zeros to be padded.
    nfft = int(pow(2, np.ceil(np.log2(len(movement))) + padlevel))

    # Frequency
    f = np.arange(0, fs, fs / nfft)
    # Normalized magnitude spectrum
    Mf = abs(np.fft.fft(movement, nfft))
    Mf = Mf / max(Mf)

    # Indices to choose only the spectrum within the given cut off frequency
    # Fc.
    # NOTE: This is a low pass filtering operation to get rid of high frequency
    # noise from affecting the next step (amplitude threshold based cut off for
    # arc length calculation).
    fc_inx = ((f <= fc) * 1).nonzero()
    f_sel = f[fc_inx]
    Mf_sel = Mf[fc_inx]

    # Choose the amplitude threshold based cut off frequency.
    # Index of the last point on the magnitude spectrum that is greater than
    # or equal to the amplitude threshold.
    inx = ((Mf_sel >= amp_th) * 1).nonzero()[0]
    fc_inx = range(inx[0], inx[-1] + 1)
    f_sel = f_sel[fc_inx]
    Mf_sel = Mf_sel[fc_inx]

    # Calculate arc length
    new_sal = -sum(np.sqrt(pow(np.diff(f_sel) / (f_sel[-1] - f_sel[0]), 2) +
                           pow(np.diff(Mf_sel), 2)))

    plt.subplot(2, 1, 1)
    plt.plot(f, Mf)
    plt.xlim(-1, 20)
    plt.subplot(2, 1, 2)
    plt.plot(f_sel, Mf_sel)
    plt.xlim(-1, 20)
    plt.show()

    # print(f"Arc Length {new_sal}, Frequ {f}, Magn. {Mf}")
    return [new_sal, (f, Mf), (f_sel, Mf_sel)]


plt.plot(DataFeatures.trimmed_axis, DataFeatures.GyroX, label='X')
plt.plot(DataFeatures.trimmed_axis, DataFeatures.GyroY, label='Y')
plt.plot(DataFeatures.trimmed_axis, DataFeatures.GyroZ, label='Z')
plt.legend()
plt.show()

SparcX = sparc(DataFeatures.GyroX, fs=104)
SparcY = sparc(DataFeatures.GyroY, fs=104)
SparcZ = sparc(DataFeatures.GyroZ, fs=104)
SPARC_RMS = (SparcZ[0] + SparcX[0] + SparcY[0]) / 3

print(f"Total = {SPARC_RMS}, X = {SparcX[0]}, Y = {SparcY[0]}, Z = {SparcZ[0]}")
