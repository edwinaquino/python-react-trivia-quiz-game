import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

import sys
            
"""
            Use this command to run this test
            $ python3 test_flaskr.py
"""  

#TUTORIAL VIDEO: https://youtu.be/0kTJd_BsFVo
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('edwin', 'test123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test."""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Prompt user to test each individual method or all
    #https://stackoverflow.com/questions/70797/how-to-prompt-for-user-input-and-read-command-line-arguments
    user_answer = input("Hi there! \nPlease Enter 1-15 to run a specific test individually \nor leave blank and hit enter to test all. [all] ")


    
    
   
    
###############################################################
#        T E S T   C A T E G O R I E S      
###############################################################     
    # Test to get all the available categories
    if  (user_answer=='1' or user_answer=='')  :
        def test_all_categories(self):
            
            # Send request and get results
            results = self.client().get('/categories')
            data = json.loads(results.data)

            # make assertions on the response data
            self.assertEqual(results.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['categories'])
            self.assertEqual(len(data['categories']), 6)
            
    # Test to get all questions in a category       
    if  (user_answer=='2' or user_answer=='')  :
        def test_category_questions(self):
            #test using Category Id # 3
            test_category_id = "3"
            test_category_type = "Geography"
            # Send request and get results
            results = self.client().get('/categories/' + test_category_id + '/questions')
            data = json.loads(results.data)

            # Create assertions
            self.assertEqual(results.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertNotEqual(len(data['questions']), 0)
            self.assertEqual(data['current_category'],test_category_type)
    
    # Test only an anvalid category id
    if  (user_answer=='3' or user_answer=='')  :
        def test_category_with_invalid_id(self):
            test_category_id = "1000"         
            results = self.client().get('/categories/' + test_category_id + '/questions')
            data = json.loads(results.data)

            # assertion - return 422 error
            self.assertEqual(results.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable entity') # GOT ERROR: AssertionError: 'Unprocessable entity' != 'Unprocessable etity'
          
                        
###############################################################
    #T E S T   S E A R C H
###############################################################   
    # Test to search for a keyword
    if  (user_answer=='4' or user_answer=='')  :
        def test_questions_search(self):
            search_data = {
                'searchTerm': 'royal palace',
            }
            # Send request and get results
            results = self.client().post('/questions/search', json=search_data)
            data = json.loads(results.data)

            # Create successful 200 assertions
            self.assertEqual(results.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(len(data['questions']), 1)
    
    # Test to search for empty search term        
    if  (user_answer=='5' or user_answer=='')  :
        def test_search_with_empty_term(self):
            search_data = {
                'searchTerm': '',
            }
            # Send request and get results
            results = self.client().post('/questions/search', json=search_data)
            data = json.loads(results.data)

            # Create assertions for error 422 Unprocessable entity
            self.assertEqual(results.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable entity')
    
    # test to search keyword that is not found        
    if  (user_answer=='6' or user_answer=='')  :
        def test_not_found_search_term(self):
            search_data = {
                'searchTerm': 'ThisDoesN0tExi5t',
            }
            # Send request and get results
            results = self.client().post('/questions/search', json=search_data)
            data = json.loads(results.data)

            # Create assertions for 404 error
            self.assertEqual(results.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Not Found')

###############################################################
    #T E S T   C R E A T E
###############################################################
    # Test to create a Geography question
    if  (user_answer=='7' or user_answer=='')  :
        def test_create_question(self):
            # mock data to use as payload for post request
            self.new_question = {
                'question': 'What is the capital of USA?',
                'answer': 'Washington DC',
                'difficulty': 1,
                'category': 3,
            }

            # Should Use patch() instead?
            results = self.client().post('/questions', json=self.new_question)
            data = json.loads(results.data)

            # asserions for 201 request
            self.assertEqual(results.status_code, 201)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['message'], 'Question successfully created!') # correct message is: Question successfully created!
    # Test form validation: to fail if submitted data is left empty        
    if  (user_answer=='8' or user_answer=='')  :
        def test_create_empty_question(self):
            search_data = {
                'question': "",
                'answer': "",
                'difficulty': 2,
                'category': 3,
            }

            # Send request and get results
            results = self.client().post('/questions', json=search_data)
            data = json.loads(results.data)

            # Create assertions for error 422
            self.assertEqual(results.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable entity')


###############################################################
    #T E S T   D E L E T E
###############################################################

    # Test delete question id that does not exist
    if  (user_answer=='9' or user_answer=='')  :
        def test_delete_invalid_question_id(self):
            test_question_id = "invalid789"
            results = self.client().delete('/questions/' + test_question_id)
            data = json.loads(results.data)
            # Create assertions for error 404
            self.assertEqual(results.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Not Found')



    # Test to a successful question deletion
    if  (user_answer=='10' or user_answer=='')  :
        def test_delete_question(self):

            # create mock question to avoid real database testing
            test_question = generate_question()

            # delete dummy question
            results = self.client().delete(
                '/questions/{}'.format(test_question))
            data = json.loads(results.data)

            # Create assertions for successful 200
            self.assertEqual(results.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['message'], "Question successfully deleted")
      
     # Test invalid question id       
    if  (user_answer=='11' or user_answer=='')  :
        def test_delete_question_with_invalid_id(self):
            # Create dummy question id we know it does not exists in the datbase
            test_question_id = "10000"
            response = self.client().delete('/questions/' + test_question_id)
            data = json.loads(response.data)

            # Create assertions for eror 422
            self.assertEqual(response.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable entity')  
             

###############################################################
    # T E S T   Q U E S T I O N S
###############################################################
    # Test all paginated questions
    if  (user_answer=='12' or user_answer=='')  :
        print("###  Testing test_get_paginated_questions ###")
        #TUTORIAL: https://youtu.be/z-3KvxWaQLs
        def test_get_paginated_questions(self):
            
            results = self.client().get('/questions') # get the endpoint
            data = json.loads(results.data) # load the data of the response

            #assertions for successful 200
            self.assertEqual(results.status_code, 200) # to make sure the status code is 200
            self.assertEqual(data['success'], True) # check that the success value of the body is true
            self.assertTrue(data['categories']) #asert there are categories
            self.assertTrue(data['total_questions']) #asert there are a total_questions
            self.assertTrue(data['questions']) #asert there are questions
            self.assertEqual(len(data['questions']), 10) #check to make sure there are questions in the list

    # Test 404 error for out of bound page
    if  (user_answer=='13' or user_answer=='')  :
        def test_404_sent_requesting_beyond_valid_page(self):
            # Send request and get results
            test_question_id = "10000"
            results = self.client().get('/questions?page=' + test_question_id)
            data = json.loads(results.data)

            #assertions
            self.assertEqual(results.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Not Found') # Kept getting error here. the R in Resource needs to be Capital
    # test playing quiz questions
    if  (user_answer=='14' or user_answer=='')  :
        def test_quiz_questions(self):
            # Generate dummy questions
            search_data = {
                'previous_questions': [5, 9],
                'quiz_category': {
                    'type': 'Geography',
                    'id': 4
                }
            }
            # Send request and get results
            results = self.client().post('/quizzes', json=search_data)
            data = json.loads(results.data)

            # Create assertions for successful 200
            self.assertEqual(results.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])

            # avoid getting the same questions
            self.assertNotEqual(data['question']['id'], 5)
            self.assertNotEqual(data['question']['id'], 9)

            # validate question is the correct category id
            self.assertEqual(data['question']['category'], 4)
            
    # Validation Test to test no empty data submitted -       
    if  (user_answer=='15' or user_answer=='')  :
        def test_quiz_with_no_data(self):
            # Send request and get results
            results = self.client().post('/quizzes', json={})
            data = json.loads(results.data)

            # Create assertions
            self.assertEqual(results.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Bad Request')


###############################################################
    # F U N C T I O N S
###############################################################

def generate_question():
    # Generate a dummy question
    question = Question(
        question='Test question for mock purpose',
        answer='Test Answer',
        difficulty=1,
        category='3')
    question.insert()
    return question.id


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()