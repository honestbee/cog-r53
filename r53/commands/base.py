from cog.command import Command

class Route53Base(Command):
  def __init__(self):
    super().__init__()
    self.aws_access_key_id = None
    self.aws_secret_access_key = None
    self.aws_region = None
    self.aws_zone_id = None

  def prepare(self):
    self.aws_access_key_id = self.config("AWS_ACCESS_KEY_ID")
    if self.aws_access_key_id == None:
      self.fail("Missing dynamic configuration variable 'AWS_ACCESS_KEY_ID'.")

    self.aws_secret_access_key = self.config("AWS_SECRET_ACCESS_KEY")
    if self.aws_secret_access_key == None:
      self.fail("Missing dynamic configuration variable 'AWS_SECRET_ACCESS_KEY'.")

    self.aws_region = self.config("AWS_REGION")
    if self.aws_region == None:
      self.fail("Missing dynamic configuration variable 'AWS_REGION'.")

    # zone id is optional
    self.aws_zone_id = self.config("AWS_ZONE_ID")