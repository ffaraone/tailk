DEFAULT_THEME = {
    'tailk._debug': 'cyan',
    'tailk._info': 'green',
    'tailk._warning': 'yellow',
    'tailk._error': 'red',
    'tailk._get': 'green',
    'tailk._post': 'orange4',
    'tailk._put': 'orange4',
    'tailk._patch': 'orange4',
    'tailk._delete': 'orange4',
    'tailk._options': 'blue',
    'tailk._head': 'blue',
    'tailk._trace': 'blue',
    'tailk._connect': 'blue',
    'tailk.p0': 'bold magenta',
    'tailk.p1': 'bold green',
    'tailk.p2': 'bold cyan',
    'tailk.p3': 'bold white',
    'tailk.p4': 'bold blue',
    'tailk.p5': 'bold dark_violet',
    'tailk.p6': 'bold turquoise2',
    'tailk.p7': 'bold slate_blue3',
    'tailk.p8': 'bold deep_pink2',
    'tailk.p9': 'bold salmon1',

}


LOG_LEVEL_PATTERNS = [
    r'(?P<_debug>DEBUG)',
    r'(?P<_info>INFO)',
    r'(?P<_warning>WARNING)',
    r'(?P<_error>ERROR)',
]

HTTP_VERB_PATTERNS = [
    r'(?P<_get>GET)',
    r'(?P<_post>POST)',
    r'(?P<_put>PUT)',
    r'(?P<_patch>PATCH)',
    r'(?P<_delete>DELETE)',
    r'(?P<_head>HEAD)',
    r'(?P<_trace>TRACE)',
    r'(?P<_options>OPTIONS)',
    r'(?P<_connect>CONNECT)',
]

DEFAULT_HIGHLIGHT_PATTERNS = LOG_LEVEL_PATTERNS + HTTP_VERB_PATTERNS


MAX_ANONYMOUS_PATTERNS = 10


RESERVED_GROUP_NAMES = {f'p{i}' for i in range(MAX_ANONYMOUS_PATTERNS)}