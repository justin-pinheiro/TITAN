import json
import time

from phi.tools.toolkit import Toolkit

from pydantic import validate_call

class HevyTool(Toolkit):
    
    def __init__(self, mail, password):
        
        super().__init__(name="hevy_tool")
        
        self.register(self.get_trainings)
        
        self.hevy_web_scrapper = HevyWebScrapper(mail, password)
        self.owner = self.hevy_web_scrapper.owner
        
        self.update_data()

    def update_data(self, amount : int = 5) -> str :
        
        print(f"Retreiving {amount} more recent data ...")

        data_str = self.hevy_web_scrapper.get_n_trainings(amount)
        
        self.data = json.loads(data_str)

        for i in range(len(self.data)):
            
            workout_details = self.hevy_web_scrapper.get_workouts_details(
                self.data[i]["workout_link"]
            )
            
            self.data[i]["exercises"] = workout_details
    
        print(f"Successfully retrieved and processed {amount} workouts!")

    @validate_call
    def get_trainings(self, amount : int = 5) -> str :
        """
        Get from the user AND those he follows the recent workouts
        
        workout data :
            - username => The username of the person that did the workout
            - date => The date of the workout
            - workout_type => The title of the given workout
            - duration => The duration of the workout
            - volume => The volume of the workout
            - workout_link => The link of the workout on the hevy website
            - exercices => The details of all exercices
        
        Args :
            - amount (int) : the amount of training you want
            
        Returns:
            str : The more recent workouts
        """

        return json.dumps(self.data[:min(amount, len(self.data))], indent=4)
    
from src.services.web_browser import WebBrowser

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

URL = "https://hevy.com/"

MAIL_INPUT_LABEL = "Email or username"
PASSWORD_INPUT_LABEL = "Password"

PROFILE_IDENTIFIER = "See your profile"

# The main page description to prouve the fact the page is properly loaded
MAIN_PAGE_DESCRIPTION = "Track workouts, make progress"

# A text in each page that is in the same div as workouts div, to know where to find them
MAIN_WORKOUTS_DELIMITER = "Home"
PROFILE_WORKOUTS_DELIMITER = "Workouts"

# A text in each workouts that prove the fact the workout is loaded
WORKOUT_LOADED_TEXT_PROOF = "Workout"

class HevyWebScrapper:
    
    def __init__(self, mail, password):
        
        self.web_service : WebBrowser = WebBrowser()

        self.driver = self.web_service.driver

        self.mail = mail
        self.password = password
        
        self.driver.get(URL)

        self.web_service.findElementByAttribute("input", "label", MAIL_INPUT_LABEL).send_keys(self.mail)
        self.web_service.findElementByAttribute("input", "label", PASSWORD_INPUT_LABEL).send_keys(self.password)  

        submit_button = self.web_service.findElementByAttribute("button", "type", "submit")
        self.driver.execute_script("arguments[0].click();", submit_button)

        self.web_service.waitUntilAttributeAppears("meta", "name", "description", MAIN_PAGE_DESCRIPTION)

        self.owner: str = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//p[contains(text(), "{PROFILE_IDENTIFIER}")]/ancestor::*[2]//*[text()[normalize-space()]]'))
        ).text

    def get_n_personal_trainings(self, amount : int = 5) -> str :
        """
        Get from the user the n more recent workouts following informations 
        
        - username
        - date
        - workout_type
        - duration
        - volume
        - workout_link
        
        For more precise information, use the function get_workouts_details, with the workout_link of the workout which is return in this function
        
        Args :
            - n (int) : the amount of training you want
            
        Returns:
            str : The n more recent workouts as json
        """
        
        self.driver.get(URL + "/profile")
        self.waitPageIsReady()

        workout_p = WebDriverWait(self.driver, 20).until(
            lambda d: d.find_elements(By.XPATH, f'//p[contains(text(), "{PROFILE_WORKOUTS_DELIMITER}")]')
            if len(d.find_elements(By.XPATH, f'//p[contains(text(), "{PROFILE_WORKOUTS_DELIMITER}")]')) >= 3
            else None
        )

        workout_delimiter = workout_p[2]

        WebDriverWait(self.driver, 20).until(
            lambda d: workout_delimiter.find_elements(
                By.XPATH, f'./following-sibling::*[.//*[contains(text(), "{WORKOUT_LOADED_TEXT_PROOF}")]]'
            )
        )

        workout_index : int = 0        
        result : list[str] = []
        workouts : list[WebElement] = []

        count_try = 0
        max_try = amount * 5

        while (len(result) < amount) and count_try < max_try :
            
            count_try += 1

            if(workout_index >= len(workouts)) :
                
                scrollable = self.driver.execute_script('''
                    const scrollable = Array.from(document.querySelectorAll('div')).find(
                        element => window.getComputedStyle(element).overflowY === 'scroll'
                    );
                    if (scrollable) {
                        scrollable.scrollTo(0, scrollable.scrollHeight);
                        return scrollable;
                    }
                    return null;
                ''')
            
                if scrollable:
                    
                    try:
                        WebDriverWait(self.driver, 2).until(
                            lambda d: len(workout_delimiter.find_elements(
                                By.XPATH, './following-sibling::*[.//*[contains(text(), "Workout")]]'
                            )) > len(workouts)
                        )
                    except Exception:
                        pass
            
            else :

                workout = workout_delimiter.find_element(
                    By.XPATH, f'./following-sibling::*[.//*[contains(text(), "Workout")][{workout_index}]]'
                )
                
                workout_index += 1

                all_text_elements = workout.find_elements(By.XPATH, ".//*[text()[normalize-space()]]")
                
                secondary_elements = workout.find_elements(By.XPATH, './/p[@type="secondary"]')

                if(len(all_text_elements) < 5) : continue

                workout_data = {}

                workout_data['username'] = all_text_elements[0].text
                workout_data['date'] = all_text_elements[1].text
                workout_data['workout_type'] = all_text_elements[2].text
                
                if(secondary_elements) : 
                    workout_data['description'] = all_text_elements[3].text
                    workout_data['duration'] = all_text_elements[5].text
                    workout_data['volume'] = all_text_elements[7].text
                    
                else :
                    workout_data['description'] = ""
                    workout_data['duration'] = all_text_elements[4].text
                    workout_data['volume'] = all_text_elements[6].text
                    
                path_div = workout.find_element(By.XPATH, ".//a[contains(@href, 'workout/')]")

                workout_data['workout_link'] = path_div.get_attribute("href")

                result.append(workout_data)
                
        self.driver.get(URL)
        self.waitPageIsReady()

        return json.dumps(result, indent=4)

    def get_n_trainings(self, amount : int = 5) -> str : 
        """
        Get from the user's friends the n more recent workouts following informations 
        
        - username
        - date
        - workout_type
        - duration
        - volume
        - workout_link
        
        For informations about exercices and sets, please use the get_workouts_details with the workout_link returned by this function
        
        Args :
            - n (int) : the amount of training you want
            
        Returns:
            str : The n more recent workouts as json
        """

        workout_delimiter = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, f'//h1[contains(text(), "{MAIN_WORKOUTS_DELIMITER}")]'))
        )
        
        WebDriverWait(self.driver, 20).until(
            lambda d: workout_delimiter.find_elements(
                By.XPATH, './following-sibling::*[.//*[contains(text(), "Workout")]]'
            )
        )
        

        workout_index : int = 0        
        result : list[str] = []
        workouts : list[WebElement] = []

        count_try = 0
        max_try = amount * 5

        while (len(result) < amount) and count_try < max_try :
            
            count_try += 1

            if(workout_index >= len(workouts)) :
                
                scrollable = self.driver.execute_script('''
                    const scrollable = Array.from(document.querySelectorAll('div')).find(
                        element => window.getComputedStyle(element).overflowY === 'scroll'
                    );
                    if (scrollable) {
                        scrollable.scrollTo(0, scrollable.scrollHeight);
                        return scrollable;
                    }
                    return null;
                ''')
            
                if scrollable:
                    try:
                        WebDriverWait(self.driver, 0.1).until(
                            lambda d: len(workout_delimiter.find_elements(
                                By.XPATH, './following-sibling::*[.//*[contains(text(), "Workout")]]'
                            )) > len(workouts)
                        )
                    except Exception:
                        pass

                workouts = workout_delimiter.find_elements(
                    By.XPATH, './following-sibling::*'
                )
            
            else :

                workout = workouts[workout_index]
                workout_index += 1

                all_text_elements = workout.find_elements(By.XPATH, ".//p[text()[normalize-space()]]")
                
                if(len(all_text_elements) < 5) : continue

                workout_data = {}

                workout_data['username'] = all_text_elements[0].text
                workout_data['date'] = all_text_elements[1].text
                workout_data['workout_type'] = all_text_elements[2].text
                workout_data['duration'] = all_text_elements[3].text
                workout_data['volume'] = all_text_elements[4].text

                path_div = workout.find_element(By.XPATH, ".//a[contains(@href, 'workout/')]")

                workout_data['workout_link'] = path_div.get_attribute("href")

                result.append(workout_data)

        return json.dumps(result, indent=4)
    
    def get_workouts_details(self, link : str = None) -> str :
        """
        Get the data from a given hevy workout link
        
        This can be used in combination of get_n_trainings and get_n_personal_trainings that can get the link for the workouts
        
        Args :
            - link (str) : the hevy workout link you wan't data from
            
        Returns:
            str : The data with a json format
        """
        
        if(not link) : raise Exception("Workout link should not be equals to None")
        if(link[:24] != "https://hevy.com/workout") : raise Exception("Workout URL is not valid : Should begin with 'https://hevy.com/workout'")

        self.driver.get(link)
        self.web_service.waitPageIsReady()
        
        if(len(self.driver.find_elements(By.XPATH, f'//h1[contains(text(), "Workout not found")]')) > 0):
            raise Exception("Workout URL is not valid : " + link[24:] + " is not an existing workout")

        workout = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//p[contains(text(), "Duration")]/ancestor::div[4]'
            ))
        )

        workout_parts = workout.find_elements(
            By.XPATH, 
            './child::div'
        )
        
        workout_details = workout_parts[0]
        workout_reactions = workout_parts[1]
        workout_exercices = workout_parts[2]
        
        result : list[str] = []
        
        all_text_elements = workout_details.find_elements(By.XPATH, ".//p[text()[normalize-space()]]")
        secondary_elements = workout.find_elements(By.XPATH, './/p[@type="secondary"]')
        
        workout_data = {}

        workout_data['username'] = all_text_elements[0].text
        workout_data['date'] = all_text_elements[1].text
        workout_data['workout_type'] = all_text_elements[2].text
        
        if(secondary_elements) : 
            workout_data['description'] = all_text_elements[3].text
            workout_data['duration'] = all_text_elements[5].text
            workout_data['volume'] = all_text_elements[7].text
            workout_data['records'] = all_text_elements[8].text
            
        else :
            workout_data['description'] = ""
            workout_data['duration'] = all_text_elements[4].text
            workout_data['volume'] = all_text_elements[6].text
            workout_data['records'] = all_text_elements[8].text

        exercices = {}
        
        exercices_div = workout_exercices.find_elements(By.XPATH, './child::div')
        
        exercice_index = 1

        for exercice_div in exercices_div :
            
            exercice_div_children : list[WebElement] = exercice_div.find_elements(By.XPATH, "./child::div")
            
            if(len(exercice_div_children) <= 2) : continue

            exercice = {}
            exercice["name"] = exercice_div_children[0].find_element(By.XPATH, ".//*[text()[normalize-space()]]").text

            sets = {}
            set_index = 1
            
            for i in range(2, len(exercice_div_children)) :
                
                texts_div = exercice_div_children[i].find_elements(By.XPATH, ".//*[text()[normalize-space()]]")
                
                if(len(texts_div) < 2) : continue

                set = {}
                
                set["set_id"] = texts_div[0].text
                set["content"] = texts_div[1].text
                
                sets[set_index] = set
                set_index += 1
                
            exercice["sets"] = sets
            
            exercices[exercice_index] = exercice
            exercice_index += 1
        
        workout_data["exercices"] = exercices

        result.append(workout_data)
                
        self.driver.get(URL)
        self.web_service.waitPageIsReady()

        return json.dumps(result, indent=4)