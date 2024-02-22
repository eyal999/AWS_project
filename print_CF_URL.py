import boto3

def get_cf_distro_url(distro_id):
    cf = boto3.client('cloudfront')
    try:
        # Fetch the distribution details using the provided distribution ID
        dist_response = cf.get_distribution(Id=distro_id)
        
        # Extracting the DomainName which is the URL of the distribution
        dist_url = dist_response['Distribution']['DomainName']
        return dist_url
    except Exception as e:
        # Handle exceptions, such as if the distribution ID does not exist
        return f"An error occurred: {e}"

# Example usage
# distro_id = 'EE0ASSXU3XX8P'  # Replace this with your actual distribution ID
# distro_url = get_cf_distro_url(distro_id)
# print(distro_url)
