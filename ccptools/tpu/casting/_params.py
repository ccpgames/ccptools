__all__ = [
    'Params',
    'parse_params',
]

from ccptools.tpu.structs import *

_KW_ARG_MATCHER = re.compile(r'(\w+)=(.+)')


class Params(object):
    __slots__ = ('args', 'kwargs', 'props')

    def __init__(self, args=None, kwargs=None, props=None):
        self.args = args or []
        self.kwargs = kwargs or {}
        self.props = props or {}

    def __repr__(self):
        return u'Params(args=%r, kwargs=%r, props=%r)' % (self.args, self.kwargs, self.props)

    def __unicode__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, Params):
            return all([self.args == other.args,
                        self.kwargs == other.kwargs,
                        self.props == other.props])
        return False


def parse_params(params: Union[List[str], str],
                 list_of_props: Optional[List[str]] = None,
                 props_as_kw_dict: Optional[Dict[str, List[str]]] = None,
                 matcher: Optional[Union[re.Pattern, str]] = None):
    """Takes a list of string parameters or a single string with multiple
    parameters (e.g. from command line input or template tag calls) and splits
    up into numbered arguments, keyword arguments and property flags.

    >>> parse_params(['foo', 'bar=7', 'debug'], ['debug', 'vocal'])
    Params(args=['foo'], kwargs={'bar': '7'}, props={'debug': True, 'vocal': False})

    Parameters that are in a key/val format determined by the given regex
    matcher (defaults to "(\\w+)=(.+)" or just "key=val") will populate the
    kwargs property of the returned Param object.

    Other parameters will either get passed into the args
    list (in order) of the returned Param object or trigger the value of the key
    in the props dict of the returned Param object to be true if that param
    value is in the given list_of_props.

    All other values in list_of_props will be represented as keys in the props
    dict with the value False.

    The props_as_kw_dict optionally takes in a dict of string keys and a list of
    string values that will be searched in the parameter list and if found, the
    value will be paired with the key in the `props_as_kw_dict` and added to the
    returned Param object as a `kwargs` pair.

    >>> parse_params('foo bar warning', props_as_kw_dict={'log_level': ['info', 'warning', 'error']})
    Params(args=['foo', 'bar'], kwargs={'log_level': 'warning'}, props={})

    :param params:
    :type params: list
    :param list_of_props:
    :type list_of_props: list | None
    :param props_as_kw_dict:
    :type props_as_kw_dict: dict | None
    :param matcher:
    :type matcher: re._pattern_type
    :return:
    :rtype: ccptools.tpu.casting.Params
    """
    from ccptools.tpu.string import dequote

    matcher = matcher or _KW_ARG_MATCHER
    if isinstance(matcher, str):
        matcher = re.compile(matcher)

    if isinstance(params, str):
        params = params.split()

    list_of_props = list_of_props or []
    props_as_kw_dict = props_as_kw_dict or {}
    if props_as_kw_dict:
        for p_list in props_as_kw_dict.values():
            list_of_props.extend(p_list)

    p = Params(props=dict(zip(list_of_props, [False]*len(list_of_props))))
    for a in params:
        m = matcher.match(a)
        if m:
            p.kwargs[m.group(1)] = dequote(m.group(2))
        else:
            if a in list_of_props:
                p.props[a] = True
            else:
                p.args.append(dequote(a))

    if props_as_kw_dict:
        for keyword, p_list in props_as_kw_dict.items():
            if keyword not in p.kwargs:
                p.kwargs[keyword] = None
                for p_name in p_list:
                    if p.props.pop(p_name, False):
                        p.kwargs[keyword] = p_name
    return p
