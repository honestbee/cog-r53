from r53.commands.base import Route53Base
import r53.util as util
import boto3
import os, json

class Record_create(Route53Base):
  def __init__(self):
    super().__init__()
    self.r53client = boto3.client('route53')

  def run(self):
    self.create_()

  def create_(self):
    type = self.request.options['TYPE']
    zone = self.request.options['ZONE']
    alias_zone = self.request.get_optional_option('ALIAS-TARGET-ZONE')
    name = self.request.args[0]
    values = self.request.args[1:]
    # populate changebatch
    changes = util.ChangeBatch()
    change_description = ''
    if alias_zone is None:
        ttl = self.request.get_optional_option('TTL')
        if ttl is None:
            ttl = 300
        else:
            ttl = int(ttl)
        change_description = 'upsert: basic %s record: %s -> %s' % (type, name, values)
        self.response.info(change_description)
        changes.add_upsert_basic(name,type,ttl, values)
    else:
        # only take first argument for aliases
        change_description = 'upsert: alias %s record: %s -> %s' % (type, name, values[0])
        self.response.info(change_description)
        changes.add_upsert_alias(name,type,alias_zone,values[0])
    # dump changebatch dict as json
    # self.response.debug(json.dumps(vars(changes)))
    r53response = self.r53client.change_resource_record_sets(
        HostedZoneId=zone,
        ChangeBatch=vars(changes)
    )
    transaction = self.parse_response_(r53response, change_description)
    self.response.content(transaction, template='record_create').send()

  def parse_response_(self, r53response, change_description):
    # r53response['ChangeInfo']['SubmittedAt'] is not json serializable
    # parse everything out..
    transaction = {
      'Request': change_description,
      'Response': {
        'HTTPStatusCode': r53response['ResponseMetadata']['HTTPStatusCode'],
        'ChangeInfo': {
            'Id': r53response['ChangeInfo']['Id'],
            'Status': r53response['ChangeInfo']['Status'],
            'SubmittedAt': str(r53response['ChangeInfo']['SubmittedAt'])
        }
      }
    }
    if 200 <= transaction['Response']['HTTPStatusCode'] < 300:
      transaction['Response']['Color'] = 'green'
    else: transaction['Response']['Color'] = 'red'
    return transaction

  def dump_all_(self):
    # dump environment
    self.response.info(json.dumps(dict(os.environ)))
    # dump arguments
    self.response.info('Arguments: %s' % self.request.args)
