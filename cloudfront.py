import time
import boto3
from delete_distro import Delete_cf_distro
import logging
from botocore.exceptions import ClientError
from config import generate_callerReference
from config import generate_an_OAC_name

def Create_OAC():
    oac = boto3.client('cloudfront')
    try:
        response = oac.create_origin_access_control(
            OriginAccessControlConfig={
                'Name': f'{generate_an_OAC_name()}',
                'OriginAccessControlOriginType': 's3',
                'SigningBehavior': 'always',
                'SigningProtocol': 'sigv4'
            }
        )
    except ClientError as e:
        logging.error(e)
        return False
    oac_id = response['OriginAccessControl']['Id']
    print('Origin Access Control created succesfully')
    return oac_id
    


def create_cf_distro(bucket_name,distro_CR):
    cf = boto3.client('cloudfront')
    distribution_config = {
        'CallerReference': f'{distro_CR}',
        'Comment': 'my cloudfront trial distro',
        'Enabled': True,
        'DefaultRootObject': 'index.html',
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'myS3Origin',
                    'DomainName': f'{bucket_name}.s3.amazonaws.com',
                    'S3OriginConfig': {
                        'OriginAccessIdentity': ''
                    },
                    'ConnectionAttempts': 3,
                    'ConnectionTimeout': 10,
                    'OriginShield': {
                        'Enabled': False,
                    },
                    # 'OriginAccessControlId': f'{Create_OAC()}',
                    
                },
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'myS3Origin',
            'ViewerProtocolPolicy': 'redirect-to-https',
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {'Forward': 'none'}
            },
            'TrustedSigners': {
                'Enabled': False,
                'Quantity': 0
            },
            'MinTTL': 3600,
            'DefaultTTL': 43200
        },
        'ViewerCertificate': {
            'CloudFrontDefaultCertificate': True
        },
        'PriceClass': 'PriceClass_100'
    }
    try:
        response=cf.create_distribution(DistributionConfig=distribution_config)
    except Exception as e:
        logging.error(e)
        return False
    distro_id= response['Distribution']['Id']
    print ('Distro Created succesfully')
    print ('waiting for the Cloud Front Distribution to deploy')
    while True:
        dist = cf.get_distribution(Id=distro_id)
        if dist['Distribution']['Status'] == 'Deployed':
            print('distro deployed succesfully')
            return distro_id,
        time.sleep(30)
        print ('waiting for the Cloud Front Distribution to deploy')



# bucket = "{bucket_name}"
# distro_CR = generate_callerReference()
# print_cf_distro()
# Delete_cf_distro('{distro_id})