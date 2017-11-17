import glob

def params2name(params):
    params_str = []
    for k, v in params.items():
        try:
            param_str = '{0}-{1:g}'.format(k,v)
        except ValueError:
            param_str = '{0}-{1}'.format(k,v)
        params_str.append(param_str)
    return '_'.join(params_str)

def name2params(name):
    params = {}
    params_str = name.split('_')
    for param_str in params_str:
        param = param_str.split('-',maxsplit=1)
        key = param[0]
        try:
            params[key] = float( param[1] )
        except ValueError:
            params[key] = param[1]
    return params

def paramlist(extension):
    init = False
    for file_name in glob.glob('*{}'.format(extension)):
        flame = file_name[:file_name.find(extension)]
        params = name2params(flame)

        if not init:
            param_list = {}
            for k in params.keys():
                param_list[k] = []
            init = True

        for k, v in params.items():
            param_list[k].append(v)

    for k, v in param_list.items():
        param_list[k] = sorted(list(set(v)))

    return param_list

def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)
