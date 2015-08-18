import click
import sys
import os
import json
SRC_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/src'
sys.path.append(SRC_DIR)
from aggregator import AggregationJobsManager

@click.group()
def aggregate_metrics():
    pass


@click.command()
@click.argument('dir', type=click.Path(exists=True))
def create_index(dir):
    """Create an index of the datasets found in DIR"""
    agg = AggregationJobsManager()
    agg.createIndex(dir)

@click.command()
@click.argument('dir', type=click.Path(exists=True))
@click.option('--api_key', help='CartoDB API key', default=None)
@click.option('--offset', help='skip the first number of datasets', default=0, type=int)
@click.option('--limit', help='only aggregate LIMIT number of datasets', default=None, type=int)
def aggregate(dir, api_key, offset, limit):
    """Aggregate data in DIR"""
    agg = AggregationJobsManager()
    agg.aggregate(dir, api_key=api_key, minindex=offset, limit=limit)

aggregate_metrics.add_command(create_index)
aggregate_metrics.add_command(aggregate)


if __name__ == '__main__':
    aggregate_metrics()