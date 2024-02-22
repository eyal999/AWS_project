import boto3
def update_cloudfront_distribution_with_oac(distribution_id, oac_id):
    client = boto3.client('cloudfront')

    # Step 2: Get the current distribution configuration
    dist_config_response = client.get_distribution_config(Id=distribution_id)
    distribution_config = dist_config_response['DistributionConfig']
    etag = dist_config_response['ETag']  # Required for the update operation

    # Step 3: Update the distribution configuration to include the OAC
    # Note: This example assumes you want to add the OAC to the first origin.
    # Adjust according to your specific needs.
    distribution_config['Origins']['Items'][0]['OriginAccessControlId'] = oac_id

    # Step 4: Update the distribution
    try:
        update_response = client.update_distribution(
            DistributionConfig=distribution_config,
            Id=distribution_id,
            IfMatch=etag  # Use the ETag to ensure the state hasn't changed
        )
        print(f"Update successful. Distribution ID: {distribution_id}")
    except Exception as e:
        print(f"An error occurred: {e}")