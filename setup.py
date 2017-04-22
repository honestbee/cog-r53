from distutils.core import setup

setup (
    name = "r53",
    version = "0.1.1",
    description = "Cog commands for AWS Route53",
    author = "Vincent De Smet",
    author_email = "vincent.desmet@honestbee.com",
    url = "https://github.com/honestbee/cog-r53",
    packages = ["r53", "r53.commands"],
    requires = ["pycog3 (>=0.1.25)", "boto3 (==1.4.0)"],
    keywords = ["cog", "aws", "route53", "bot", "devops", "chatops", "automation"],
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
