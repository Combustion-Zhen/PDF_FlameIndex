
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from counterflow_file import *


# In[2]:


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')


# In[17]:


Z_st = 0.055

models = ['IEM','IEMHYB','EMST','EMSTHYB']
modeln = ['IEM','IEM-FI','EMST','EMST-FI']
mix_res_ratio = [0.02, 0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]

time_res = 1.e-2
equiv_ratio_f = 4.76
equiv_ratio = 1.0
Zf_variance = 0.1
dtmix = 0.01

params = {}
params['MIX'] = None
params['tmix'] = 0.2
params['var'] = 'C'
params['statics'] = None


# In[18]:


# obtain data
file_name = 'cond-CT_eqv-{:g}.csv'.format(equiv_ratio)
data = pd.read_csv(file_name)


# In[26]:


# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.3
margin_right  = 0.2
margin_bottom = 1.0
margin_top    = 0.1
space_width   = 3.5
space_height  = 0.5
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 2
num_rows = 1

colors = ['tab:orange','tab:blue','tab:green','tab:red']
lines = [':','-','-.','--']

mft = ['o','s']
mfc = ['w',None]

dst = '.'

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.9

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)


# In[55]:


# plot against tmix
fig, ax = plt.subplots(num_rows,num_cols,sharex=True,
                       figsize=cm2inch(plot_width,plot_height))

for i, model in enumerate(models):
    params['MIX'] = model
    
    params['statics'] = 'avg'
    y = data[params2name(params)].values
    ax[0].plot(
        data['Z'], y,
        c = colors[i], ls = lines[i], lw = 1.,
        label=modeln[i])
    
    params['statics'] = 'var'
    y = data[params2name(params)].values
    yhat = savitzky_golay(y, 7,3)
    ax[1].plot(
        data['Z'], yhat,
        c = colors[i], ls = lines[i], lw = 1.,
        label=modeln[i])

# legend
ax[0].legend(frameon=False)

# limits
ax[0].set_xlim([0, 0.5])
ax[0].set_ylim([0, 0.3])
ax[1].set_ylim([0, 0.008])
ax[1].set_yticks(np.arange(0, 0.009, 0.001))
ax[1].set_yticklabels(np.arange(0, 9))

# notes
ax[0].text(
        0.32,0.1,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=\,$',
            '{:g}'.format(time_res),
            '$\;\mathrm{s}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=\,$',
            '{:g}'.format(time_res*params['tmix']*1000),
            '$\;\mathrm{ms}$',
            '\n',
            r'$\varphi\quad\;\!=\,$',
            '{:g}'.format(equiv_ratio),
            '\n',
            r'$\eta_{Z,r}\!\!\:=\,$',
            '{:g}'.format(Zf_variance)]))

# labels
ax[0].set_xlabel(r'$Z$')
ax[1].set_xlabel(r'$Z$')
ax[0].set_ylabel(r'$\langle c\vert Z \rangle$')
ax[1].set_ylabel(r'$\langle c^{\prime\prime 2}\vert Z \rangle\times 10^{3}$')

# figure layout
fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )


# In[44]:


fig.savefig('{0}/fig_C_tmix-{1:g}_eqv-{2:g}.pdf'.format(dst,params['tmix'],equiv_ratio))

