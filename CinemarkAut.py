from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

CINEMARK_URL = "https://www.cinemarkhoyts.com.ar/"

def setting_browser() -> webdriver.Edge:
    driver = webdriver.Edge()
    driver.minimize_window()

    driver.get(CINEMARK_URL)

    driver.implicitly_wait(0.5)

    driver.find_element(by=By.CLASS_NAME, value="cookies-btn").click()

    return driver

def get_movies() -> list[str]:
    try:

        driver = setting_browser()

        moviesDivElement = driver.find_elements(by=By.CLASS_NAME, value="SumoSelect")[1]
        moviesDivElement.click()
    
        moviesOptionElements = moviesDivElement.find_elements(by=By.TAG_NAME, value="option")

        movies = []

        for mOption in moviesOptionElements:
            movies.append(mOption.get_attribute("innerHTML"))
    
        movies.pop(0)
        driver.quit()
        return movies
    
    except Exception as e: 
        return "ERROR: " + str(e)
    
def get_cinemas() -> list[str]:
    try:

        driver = setting_browser()

        cinemasDivElement = driver.find_elements(by=By.CLASS_NAME, value="SumoSelect")[0]
        cinemasDivElement.click()
    
        cinemasOptionElements = cinemasDivElement.find_elements(by=By.TAG_NAME, value="option")

        cinemas = []

        for cOption in cinemasOptionElements:
            cinemas.append(cOption.get_attribute("innerHTML"))
    
        cinemas.pop(0)
        driver.quit()
        return cinemas
    
    except Exception as e: 
        return "ERROR: " + str(e) 

def get_cinemas_for_movie(movie: str) -> list[str]:

    try:

        driver = setting_browser()

        click_movie(driver, movie)
    
        cinemasDivElement = driver.find_elements(by=By.CLASS_NAME, value="SumoSelect")[0]
        cinemasDivElement.click()
    
        cinemasOptionElements = cinemasDivElement.find_elements(by=By.TAG_NAME, value="option")

        cinemas = []

        for cOption in cinemasOptionElements:
            cinemas.append(cOption.get_attribute("innerHTML"))

        cinemas.pop(0)
        driver.quit()
        return cinemas
    
    except Exception as e:
        return "ERROR: " + str(e)

def get_dates_for_movie_in_cinema(cinema: str, movie: str) -> list[str]:
    try:
        driver = setting_browser()
        
        click_cinema(driver, cinema)
        click_movie(driver, movie)
        
        dates = []
        datelineDivElement = driver.find_element(by=By.ID, value="ch-timeline")
        dateLabelElements = datelineDivElement.find_elements(by=By.TAG_NAME ,value="label")
    
        for dLabel in dateLabelElements:
            dateSpanElement = dLabel.find_elements(by=By.TAG_NAME, value="span")[2]
            dates.append(dateSpanElement.get_attribute("innerHTML"))
            
        return dates
    except Exception as e:
        return "ERROR: " + str(e)

def get_movies_for_cinema(cinema: str) -> list[str]:

    try:

        driver = setting_browser()

        click_cinema(driver, cinema)
    
        moviesDivElement = driver.find_elements(by=By.CLASS_NAME, value="SumoSelect")[1]
        moviesDivElement.click()
    
        moviesOptionElements = moviesDivElement.find_elements(by=By.TAG_NAME, value="option")

        movies = []

        for mOption in moviesOptionElements:
            movies.append(mOption.get_attribute("innerHTML"))

        movies.pop(0)
        driver.quit()
        return movies
    
    except Exception as e:
        return "ERROR: " + str(e)

def get_today_functions(cinema: str, movie: str) -> dict:

    try:
        driver = setting_browser()
        click_cinema(driver, cinema)
        click_movie(driver, movie)

        functionsLiElements = driver.find_elements(by=By.CLASS_NAME, value="list-group-item")
        
        functions = {}
        dateMovieKey = get_movie_date(driver, get_today_date())
        functions[dateMovieKey] = {}
        
        for fLi in functionsLiElements:
            functionH2Element = fLi.find_element(by=By.TAG_NAME, value="h2")
            functionLanguageSpanElements =  functionH2Element.find_elements(by=By.TAG_NAME, value="span")

            functionH2String = functionH2Element.get_attribute("innerHTML")
            functionLanguage = ""
            dboxText = ""

            if "DBOX" in functionH2String:
                dboxText = "DBOX"

            for fLangSpan in functionLanguageSpanElements:
                langText = fLangSpan.get_attribute("innerHTML").strip()
                functionLanguage += " " + langText
                if langText == "+":
                    functionLanguage += " " + dboxText

        
            functionSubKey = functionH2String[7:9] + functionLanguage
            functions[dateMovieKey][functionSubKey] = []

            functionDivElement = fLi.find_element(by=By.CLASS_NAME, value="ch-radio-group")
            functionsSpanElements = functionDivElement.find_elements(by=By.TAG_NAME, value="span")

            for fSpan in functionsSpanElements:
                functions[dateMovieKey][functionSubKey].append(fSpan.get_attribute("innerHTML"))

        driver.quit()
        return functions
    
    except Exception as e:
        return "ERROR: " + str(e)
    
def get_functions_for_date(cinema: str, movie: str, date: str):

    try:
        driver = setting_browser()
        click_cinema(driver, cinema)
        click_movie(driver, movie)
        click_date(driver, date)

        functionsLiElements = driver.find_elements(by=By.CLASS_NAME, value="list-group-item")
        functions = {}
        dateMovieKey = get_movie_date(driver, get_movie_date(driver, date))
        functions[dateMovieKey] = {}
        
        for fLi in functionsLiElements:
            functionH2Element = fLi.find_element(by=By.TAG_NAME, value="h2")
            functionLanguageSpanElements =  functionH2Element.find_elements(by=By.TAG_NAME, value="span")

            functionH2String = functionH2Element.get_attribute("innerHTML")
            functionLanguage = ""
            dboxText = ""

            if "DBOX" in functionH2String:
                dboxText = "DBOX"

            for fLangSpan in functionLanguageSpanElements:
                langText = fLangSpan.get_attribute("innerHTML").strip()
                functionLanguage += " " + langText
                if langText == "+":
                    functionLanguage += " " + dboxText

        
            functionSubKey = functionH2String[7:9] + functionLanguage
            functions[dateMovieKey][functionSubKey] = []

            functionDivElement = fLi.find_element(by=By.CLASS_NAME, value="ch-radio-group")
            functionsSpanElements = functionDivElement.find_elements(by=By.TAG_NAME, value="span")

            for fSpan in functionsSpanElements:
                functions[dateMovieKey][functionSubKey].append(fSpan.get_attribute("innerHTML"))

        return functions
    
    except Exception as e:
        return "ERROR: " + str(e) 

def click_movie(driver: webdriver.Edge, movie: str) -> None:
    existMovie = False
    movie = movie.replace("_", " ")
    moviesDivElement = driver.find_elements(by=By.CLASS_NAME, value="SumoSelect")[1]
    moviesDivElement.click()

    driver.implicitly_wait(0.5)

    moviesLabelElements = moviesDivElement.find_elements(by=By.TAG_NAME, value="label")
    for mLabel in moviesLabelElements:
        if(mLabel.get_attribute("innerHTML") == movie):
            mLabel.click()
            existMovie = True
            break

    if(not existMovie):
        raise Exception("Movie not found")

def click_cinema(driver: webdriver.Edge, cinema: str) -> None:
    existCinema = False
    cinema = cinema.replace("_", " ")
    cinemasDivElement = driver.find_elements(by=By.CLASS_NAME, value="SumoSelect")[0]
    cinemasDivElement.click()

    driver.implicitly_wait(0.5)
    
    cinemasLabelElements = cinemasDivElement.find_elements(by=By.TAG_NAME, value="label")
    for cLabel in cinemasLabelElements:
        if(cLabel.get_attribute("innerHTML") == cinema):
            cLabel.click()
            existCinema = True
            break

    if(not existCinema):
        raise Exception("Cinema not found")

def click_date(driver: webdriver.Edge, date: str) -> None:
    datelineDivElement = driver.find_element(by=By.ID, value="ch-timeline")
    datesLabelElements = datelineDivElement.find_elements(by=By.TAG_NAME ,value="label")
    
    for dLabel in datesLabelElements:
        dateSpanElement = dLabel.find_elements(by=By.TAG_NAME, value="span")[2]
        if(dateSpanElement.get_attribute("innerHTML") == date):
            dateSpanElement.click()
            break

def get_movie_date(driver: webdriver.Edge, date: str) -> str:
    datelineDivElement = driver.find_element(by=By.ID, value="ch-timeline")
    dateLabelElements = datelineDivElement.find_elements(by=By.TAG_NAME ,value="label")
    
    for dLabel in dateLabelElements:
        dateSpanElement = dLabel.find_elements(by=By.TAG_NAME, value="span")[2]
        if(dateSpanElement.get_attribute("innerHTML") == date):
            return date
       
    raise Exception("Date not found")
        
def get_today_date() -> str:
    return datetime.now().strftime('%d/%m')

def main() -> None:
    print(get_functions_for_date("Hoyts_Abasto", "LA_SIRENITA", "14/06"))
    
if __name__ == "__main__":
    main()