from sys import exit
from nonumpy import Factory as NonumpyFactory
from crelm import Factory as CrelmFactory

# todo foss: move this into John


def make_plotter(min: float, max: float, width: int):
    source = f'''
#include <stdio.h>

void plot(int x, float y)
{{
    char p = '*';

    float v = y - {min};
    v *= (float){width} / ({max} - {min});

    int j = (int)v;

    if (j < 0)
    {{
        j = 0;
        p = '<';
    }}
    else if (j >= {width})
    {{
        j = {width} - 1;
        p = '>';
    }}

    char s[{width + 1}];

    for (int i = 0; i < {width}; ++i)
    {{
        s[i] = j == i ? p : ({width} / 2 == i ? '|' : '.');    
    }}

    s[{width}] = 0;

    printf("(%3d, % f) %s\\n", x, y, s);
}}
    '''

    return CrelmFactory().create_Tube('plotter') \
        .add_source_text(source) \
        .squeeze()


def plot(filter, plotter):
    plotter.plot(0, filter.run(1))

    for x in range(1, 50):
        plotter.plot(x, filter.run(0))


if '__main__' == __name__:

    print('building plotter...')
    plotter = make_plotter(min=-0.1, max=0.1, width=60)

    filter_parms = {'cutoff_hz': 1, 'order': 2, 'sample_rate_hz': 25}

    print('building low pass Butterworth...')
    plot(NonumpyFactory().create_FilterLowPassButterworth(**filter_parms), plotter)

    print('building high pass Butterworth...')
    plot(NonumpyFactory().create_FilterHighPassButterworth(**filter_parms), plotter)

    print('building Exponential Moving Average...')
    plot(NonumpyFactory().create_EMA(alpha=0.1), plotter)

    exit(42)
