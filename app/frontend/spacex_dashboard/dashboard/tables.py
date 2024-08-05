import django_tables2 as tables

class LaunchTable(tables.Table):
    avg_launches_per_year = tables.Column(verbose_name='Avg Launches Per Year', orderable=False)
    failed_launches = tables.Column(verbose_name='Failed Launches', orderable=False)
    most_used_rocket = tables.Column(verbose_name='Most Used Rocket', orderable=False)
    successful_launches = tables.Column(verbose_name='Successful Launches', orderable=False)
    total_launches = tables.Column(verbose_name='Total Launches', orderable=False)

    class Meta:
        attrs = {'class': 'table'}

class RocketTable(tables.Table):
    avg_diameter = tables.Column(verbose_name='Avg Diameter', orderable=False)
    avg_height = tables.Column(verbose_name='Avg Height', orderable=False)
    avg_success_rate = tables.Column(verbose_name='Avg Success Rate', orderable=False)
    total_cost_per_launch = tables.Column(verbose_name='Total Cost Per Launch', orderable=False)
    total_rockets = tables.Column(verbose_name='Total Rockets', orderable=False)

    class Meta:
        attrs = {'class': 'table'}

class StarlinkTable(tables.Table):
    active_satellites = tables.Column(verbose_name='Active Satellites', orderable=False)
    decayed_satellites = tables.Column(verbose_name='Decayed Satellites', orderable=False)
    total_satellites = tables.Column(verbose_name='Total Satellites', orderable=False)

    class Meta:
        attrs = {'class': 'table'}