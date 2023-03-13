import argparse, requests, csv, json, os, re, datetime
import logging
from requests import HTTPError


API_VERSION = 5.131
DOMAIN = 'https://api.vk.com/method'


def get_user_id(username):
    response = requests.get(f'{DOMAIN}/users.get', params={
        'user_ids': username,
        'access_token': os.environ.get('VK_SERVICE_ACCESS_TOKEN'),
        'v': API_VERSION,
    })
    data = response.json()
    if len(data['response']) == 0:
        logging.error(f"Error occurred while getting user ID for {username}")
    elif 'response' in data:
        return data['response'][0]['id']
    elif 'error' in data:
        logging.error(f"Error occurred while getting user ID for {username}: {data['error']['error_msg']}")
    return None
    

def get_user_friends(user_id):
    try:
        response = requests.get(f'{DOMAIN}/friends.get', params={
            'user_id': user_id,
            'access_token': os.environ.get('VK_SERVICE_ACCESS_TOKEN'),
            'v': API_VERSION,
            'fields': 'city,country,bdate,sex',
            'order': 'name',
        })
        response.raise_for_status()
        data = response.json()
        if 'response' in data:
            return data['response']['items']
        elif 'error' in data:
            logging.error(f"Error occurred while getting friends for user ID {user_id}: {data['error']['error_msg']}")
    except HTTPError as error:
        print(f'An error occured')
    return None


def dump(data, file_format, file_path, filename):
    # Determine file extension based on file format
    if file_format == "csv":
        file_ext = ".csv"
        writer_class = csv.DictWriter
        kwargs = {'delimiter': ','}
    elif file_format == "tsv":
        file_ext = ".tsv"
        writer_class = csv.DictWriter
        kwargs = {'delimiter': '\t'}
    elif file_format == "json":
        file_ext = ".json"
        writer_class = None
        kwargs = {}
    else:
        raise ValueError("Invalid file format specified. Must be 'csv', 'tsv', or 'json'.")

    # Create output file path
    output_file = os.path.join(file_path, f"{filename}{file_ext}")
    
    # If column order is not determined, just get all keys from first dict and use as columns
    column_order = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
    if column_order is None:
        if isinstance(data, list) and isinstance(data[0], dict):
            column_order = list(data[0].keys())
        else:
            column_order = None
    
    with open(output_file, 'w', newline='') as f:
        if writer_class is not None:
            writer = writer_class(f, fieldnames=column_order, **kwargs)
            writer.writeheader()
            for item in data:
                row = {}
                for col in column_order:
                    # Sorry for hardcode with bdates, but I did my best.
                    if col == 'bdate':
                        bdate = item.get(col, '')
                        if bdate:
                            bdate_parts = bdate.split('.')
                            if len(bdate_parts) >= 2:
                                row[col] = '-'.join(reversed(bdate_parts))
                    elif isinstance(item.get(col), dict):
                        row[col] = item[col].get('title', '')
                    else:
                        row[col] = item.get(col, '')
                writer.writerow(row)
        else:
            json.dump(data, f)


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='Link to profile page or user id(without "id" part)')
    parser.add_argument('-f', '--file', help='Specify the file', default='report.csv')
    args = parser.parse_args()

    # Extract the file_path, filename, and file_format from --file argument.
    file_path, filename = os.path.split(args.file)
    filename, file_ext = os.path.splitext(filename)
    file_format = file_ext[1:]

    # Check whether 'user' argument is link or user_id  
    user = args.user
    if user.isdigit():
        user_id = int(user)
    elif re.match(r'^(https?:\/\/)?(?:www\.)?(vk\.com\/)?([A-Za-z0-9_-]+)$', user):
        username = user.split('/')[-1] # maybe use the capturing groups of regexes?
        user_id = get_user_id(username) # add some checks
    else:
        raise ValueError(f"{user} is not a valid username or user ID")

    # Retrieve friends list and dump to file
    friends_json = get_user_friends(user_id)
    if friends_json is not None:
        dump(friends_json, file_format=file_format, file_path=file_path, filename=filename)
    

if __name__ == '__main__':
    main()
