import argparse, requests, csv, json, os
from requests import HTTPError
from config import service_access_token, api_version, domain
# запускать прогу с аргументами
# username в вк
# если запущена без аргументов, то просить ввести юзернейм чьих друзей мы хотим получить

"""
assert user_id > 0, 'USER_ID must be greater or equal to 1'
assert isinstance(user_id, int), 'USER_ID must be integer'
"""

def get_user_friends(user_id):
    try:
        response = requests.get(f"{domain}/friends.get?access_token={service_access_token}&v={api_version}&user_id={user_id}\
                                &fields=city,country,bdate,sex&order=name")
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            print(data['error']['error_msg'])
            return None
    except HTTPError as error:
        print(f'An error occured')
    return data['response']['items']


def get_user_id(username):
    """
    Функция для получения user_id, при условии что был введен никнейм или ссылка на страницу 
    """
    user_id = requests.get(f'{domain}/users.get?user_ids={username}&access_token={service_access_token}&v={api_version}')
    return user_id.json()


def dump(data, file_format='csv', file_path='', filename='report', column_order=['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']):
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
                    if isinstance(item.get(col), dict):
                        row[col] = item[col].get('title', '')
                    else:
                        row[col] = item.get(col, '')
                writer.writerow(row)
        else:
            json.dump(data, f)

    
dump(get_user_friends(2), file_format='csv')
#print(get_user_friends(417459713))

"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    dump()"""
