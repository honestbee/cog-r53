from r53.commands.base import Route53Base
import r53.util as util
import boto3

class Record(Route53Base):
  def __init__(self):
    super().__init__()
    client = boto3.client('route53')

  def run(self):
    handler = self.parse_subcommand_()
    handler()
