###############################################################################
# DESCRIPTION: plots the sky cover of the old TSI software and the newly
#              developed software and compares the two.
#
#
#
# AUTHOR: Job Mos	                            # EMAIL: jobmos95@gmail.com
#
###############################################################################

# import libraries
import numpy as np
from matplotlib import pyplot as plt


def plot():
    data = np.genfromtxt('data.csv', delimiter='\t',
                         names=['filename', 'altitude', 'azimuth', 'thinskycover', 'opaqueskycover', 'totalskycover',
                                'thinskycoverTSI', 'opaqueskycoverTSI', 'totalskycoverTSI', 'energy', 'entropy',
                                'contrast', 'homogeneity'])

    fig, ((ax1), (ax2), (ax3), (ax4)) = plt.subplots(4, 1, sharex=True)

    ax1.plot(data['azimuth'], data['thinskycoverTSI'] * 100,
             color='tab:red', label='thin (TSI)', linewidth=2.0)
    ax1.plot(data['azimuth'], data['thinskycover'] * 100,
             color='tab:green', label='thin', linewidth=2.0)
    ax2.plot(data['azimuth'], data['opaqueskycoverTSI'] * 100,
             color='tab:red', label='opaque (TSI)', linewidth=2.0)
    ax2.plot(data['azimuth'], data['opaqueskycover'] * 100,
             color='tab:green', label='opaque', linewidth=2.0)
    ax3.plot(data['azimuth'], data['totalskycoverTSI'] * 100,
             color='tab:red', label='total (TSI)', linewidth=2.0)
    ax3.plot(data['azimuth'], data['totalskycover'] * 100,
             color='tab:green', label='total', linewidth=2.0)
    ax4.plot(data['azimuth'], abs((data['totalskycover'] - data['totalskycoverTSI']) * 100),
             color='black', linewidth=2.0, label='abs(new-old)')
    ax4.plot(data['azimuth'], (data['totalskycover'] - data['totalskycoverTSI']) * 100,
             color='tab:blue', linewidth=2.0,label='new-old')

    ax1.set_ylabel('thin fraction (%)')
    ax2.set_ylabel('opaque fraction (%)')
    ax3.set_ylabel('total cloud cover (%)')
    ax4.set_ylabel('total cloud cover difference (%)')

    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()

    ax1.set_ylim([-5, 105])
    ax2.set_ylim([-5, 105])
    ax3.set_ylim([-5, 105])

    ax1.legend(loc='upper center')
    ax2.legend(loc='lower center')
    ax3.legend(loc='lower center')
    ax4.legend(loc='lower center')

    # plt.tight_layout()

    ax4.set_xlabel('azimuth (deg)')

    plt.show()

    plt.close()

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, sharex=True)

    ax1.plot(data['azimuth'], data['altitude'] * 100, linewidth=2.0)
    ax2.plot(data['azimuth'], data['totalskycover'], linewidth=2.0)
    ax3.plot(data['azimuth'], data['energy'], linewidth=2.0)
    ax4.plot(data['azimuth'], data['entropy'], linewidth=2.0)
    ax5.plot(data['azimuth'], data['contrast'], linewidth=2.0)
    ax6.plot(data['azimuth'], data['homogeneity'], linewidth=2.0)

    ax1.set_ylabel('altitude')
    ax2.set_ylabel('cloud cover')
    ax3.set_ylabel('energy')
    ax4.set_ylabel('entropy')
    ax5.set_ylabel('contrast')
    ax6.set_ylabel('homogeneity')

    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax5.grid()
    ax6.grid()

    ax4.set_xlabel('azimuth (deg)')
    ax5.set_xlabel('azimuth (deg)')
    ax6.set_xlabel('azimuth (deg)')

    plt.show()

    plt.close()
