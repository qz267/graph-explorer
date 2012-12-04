from . import GraphTemplate
class CpuTemplate(GraphTemplate):
    '''
    only pass targets for total cpu metrics, not all cores individually
    http://www.linuxhowtos.org/System/procstat.htm documents all states, except guest and steal(?)
    everything is in percent, but note that e.g. a 16 core machine goes up to 1600%
    '''
    pattern_graph = "^servers\.([^\.]+)\.cpu\.total\.user$"
    target_types = {
        'cpu_state_pct': {
            'match': '^servers\.(?P<server>[^\.]+)\.cpu\.total\.(?P<type>.*)$',
            'default_group_by': 'server',
            'default_graph_options': {'state': 'stacked'}
        }
    }

    def configure_target(self, target):
        t = target['tags']['type']
        color_assign = {
            'idle': self.colors['green'][0],
            'user': self.colors['blue'][0],
            'system': self.colors['blue'][1],
            'nice': self.colors['purple'][0],
            'softirq': self.colors['red'][0],
            'irq': self.colors['red'][1],
            'iowait': self.colors['orange'][0],
            'guest': self.colors['white'],
            'steal': self.colors['white'] # i make these white cause i'm not sure if they're relevant
        }
        target['color'] = color_assign[t]
        return target

    def generate_graphs (self, match):
        return {}

# vim: ts=4 et sw=4:
