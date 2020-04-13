
if __name__ == "__main__":
    import os
    import pickle
    import csv
    import requests, re
    from bs4 import BeautifulSoup


def process_car_blocks(soup):
    car_blocks = soup.find_all('div', class_='car_block')
    data = []
    my_dict={}
    for car_block in car_blocks:
        my_dict = extract_data(car_block)
        data.append(my_dict)
        # print(my_dict)
    with open('car_data.csv','w') as csvfile:
        print("hi")
        writer = csv.DictWriter(csvfile,fieldnames=my_dict.keys())
        writer.writeheader()
        writer.writerows(data)
    # return data


def extract_data(car_block):
    name = car_block.find('span', class_='car_name').text
    cylinder = car_block.find('span', class_='cylinders').text
    weight = int(car_block.find('span', class_='weight').text.replace(',', ''))
    year, country = car_block.find('span', class_='from').text.strip('()').split(',')
    year = int(year.strip())
    country = country.strip()
    acceleration = float(car_block.find('span', class_='acceleration').text)
    try:
        mpg = float(car_block.find('span', class_='mpg').text.split()[0])
    except ValueError:
        mpg = "NULL"
    try:
        hp = float(car_block.find('span', class_='horsepower').text)
    except ValueError:
        hp = "NULL"
    try:
        displacement = float(re.findall(r'.* (\d+.\d+) cubic inches ', car_block.text)[0])
    except ValueError:
        displacement = "NULL"
    my_dict = dict(
        name=name,
        cylinder=cylinder,
        weight=weight,
        year=year,
        country=country,
        acceleration=acceleration,
        mpg=mpg,
        hp=hp,
        displacement=displacement
    )
    return my_dict


if __name__ == "__main__":

    file_name = 'data.pickle'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as soup_file:
            result = pickle.load(soup_file)
    else:
        result = requests.get('http://0.0.0.0:8000/auto_mpg.html')
        with open(file_name, 'wb') as soup_file:
            pickle.dump(result, soup_file)

    source = result.text
    soup = BeautifulSoup(source, 'html.parser')
    process_car_blocks(soup)
