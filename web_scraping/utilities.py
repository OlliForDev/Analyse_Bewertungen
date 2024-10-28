'''
########################################################
    helper functions to parse data from website
########################################################
'''
from bs4 import BeautifulSoup

'''
    collects important information about the provider by given soup object
    returns a dictonary containing all information
'''
def get_provider_details(soup):
    name = soup.find('h1', class_='carrier-provider-name').text.partition(':')[0]
    post_code = soup.find('div', class_='carrier-address').text.split('\n')[3].split(' ')[1].replace(' ', '')
    # get provider details
    owner, year_of_foundation, number_of_employees, number_of_customer, revenue = '', '', '', '', ''
    details = soup.find('div', class_='carrier-details')
    for info_html in details.find_all('p'):
        if get_subheadline_of_provider_details(info_html) == 'Eigentümer':
            owner = get_info(info_html)
        elif get_subheadline_of_provider_details(info_html) == 'Gründung':
            year_of_foundation = get_info(info_html)
        elif get_subheadline_of_provider_details(info_html) == 'Mitarbeiter 2020':
            number_of_employees = get_info(info_html)
        elif get_subheadline_of_provider_details(info_html) == 'Kunden 2020':
            number_of_customer = get_info(info_html)
        elif get_subheadline_of_provider_details(info_html) == 'Umsatz 2020':
            revenue = info_html.text.split('\n')[2]
        else:
            None
    
    return {'name': name, 
            'post_code': post_code, 
            'owner': owner, 
            'year_of_foundation': year_of_foundation, 
            'number_of_employees': number_of_employees,
            'number_of_customer': number_of_customer,
            'revenue': revenue}

'''
    collects information from all costumer ratings by given soup object
    returns a list of dictonaries containing all information
'''
def get_all_ratings(soup):
    all_ratings_html = soup.find_all('div', class_='customer-ratings-container')
    all_ratings = []
    for rating in all_ratings_html:
        # Scrape title of rating
        title = rating.find('div', class_='customer-rating-headline').find('h3').text  # Assuming titles are inside <h3> tag
        # Scrape scoring of each criteria
        rating_price, rating_service, rating_provider_change = 0, 0, 0
        criteria = rating.find('div', class_='carrier-rating-criteria').find_all('div', class_='rating-details-row')
        for scoring in criteria:
            if scoring.find('p').text == 'Service':
                scoring_service = get_rating(scoring)
            elif scoring.find('p').text == 'Preis':
                scoring_price = get_rating(scoring)
            elif scoring.find('p').text == 'Anbieterwechsel':
                scoring_provider_change = get_rating(scoring)
            else:
                print('keine Kriterien gefunden!') 
        # Scrape Dates from rating footer
        footer = rating.find('div', class_='comment-footer').find('div', class_='comment-metadata')
        provider_change_timetable = footer.get_text(strip='True')
        date_of_order = provider_change_timetable.split(' ')[6] + ' ' + provider_change_timetable.split(' ')[7][0:4]
        date_of_change = provider_change_timetable.split(' ')[0] + ' ' + provider_change_timetable.split(' ')[1]
        all_ratings.append({'title': title,
                            'scoring_price': scoring_price,
                            'scoring_service': scoring_service,
                            'scoring_provider_change': scoring_provider_change,
                            'date_of_order':date_of_order,
                            'date_of_change': date_of_change})
    return all_ratings

'''
    extracts information about provider from given text by string operations
'''
def get_info(info_html):
    return info_html.text.split('\n')[2].replace(' ', '')

'''
    extracts information about provider from given text by string operations
'''
def get_rating(scoring):
    rating_stars_elem = scoring.find('div', class_='rating-stars-active')['style']
    return rating_stars_elem.split(' ')[1].replace('%', '')

def get_subheadline_of_provider_details(info):
    return info.find('span', class_='subheadline').get_text(strip=True)


'''
########################################################
    helper functions to interacte with MySQL Database
########################################################
'''
import mysql.connector
from mysql.connector import Error
from settings import DB_PORT, DATABASE_NAME, PASSWORD, USER, HOST

def insert_ratings(title, scoring_price, scoring_provider_change, scoring_service, date_of_order, date_of_change, provider):
    connection = None
    try:
        # Establish a database connection
        print(HOST, DB_PORT, DATABASE_NAME, USER, PASSWORD)
        connection = mysql.connector.connect(
            host=HOST,
            port=DB_PORT,   # Replace with your MySQL host
            database=DATABASE_NAME,  # Replace with your database name
            user=USER,  # Replace with your MySQL username
            password=PASSWORD  # Replace with your MySQL password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Calling the stored procedure
            stored_procedure = "call insert_ratings(%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(stored_procedure, (title, scoring_price, scoring_provider_change, scoring_service, date_of_order, date_of_change, provider))
            
            # Commit the transaction
            connection.commit()
            
            print(f"rating inserted successfully.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed - insert rating executed")


def insert_provider(provider_name, foundation_year, number_of_employees, number_of_customer, revenue, post_code):
    connection = None
    try:
        # Establish a database connection
        connection = mysql.connector.connect(
            host=HOST,
            port=DB_PORT,   # Replace with your MySQL host
            database=DATABASE_NAME,  # Replace with your database name
            user=USER,  # Replace with your MySQL username
            password=PASSWORD  # Replace with your MySQL password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Calling the stored procedure
            stored_procedure = "call insert_provider(%s, %s, %s, %s, %s, %s);"
            print(stored_procedure, (provider_name, foundation_year, number_of_employees, number_of_customer, revenue, post_code))
            cursor.execute(stored_procedure, (provider_name, foundation_year, number_of_employees, number_of_customer, revenue, post_code))
            
            # Commit the transaction
            connection.commit()
            
            print(f"Customer {provider_name} inserted successfully.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed - insert provider executed")