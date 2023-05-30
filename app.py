from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templates', static_folder='static')

def scrape_jobsNepal():
    url = "https://www.jobsnepal.com/category/information-technology-jobs"  # URL of jobsNepal
  
    # Send a GET request to the URL
    response = requests.get(url)
   
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    job_listings = soup.find_all('div', class_='card-inner')

    # Initialize empty lists for titles, companies, and apply links
    titles = []
    companies = []
    apply_links = []
    
    # Iterate over each job listing
    for listing in job_listings:
        # Extract the title
        title = listing.find('h2', class_='job-title').text.strip()
        titles.append(title)
        company = listing.find('p', class_='mb-0').text.strip()
        companies.append(company)
        apply_link = listing.find('a', class_='btn-info').get('href')
        apply_links.append(apply_link)

   # Combine the lists into a list of tuples
    job_data = list(zip(titles, companies, apply_links))

    # Return the combined data
    return job_data
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-info.html')

@app.route('/browse_jobs')
def index():
    # Scrape the job listings from jobsNepal.com
    job_data = scrape_jobsNepal()
    #print(job_data)

    # Render the template with the scraped data
    return render_template('index.html', job_data=job_data)

if __name__ == '__main__':
    app.run(debug=True)
