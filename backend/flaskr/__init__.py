import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS INFORMATION: https://classroom.udacity.com/nanodegrees/nd0044-ent/parts/573bef13-96dd-4f0f-9d47-afdd5f22ebc5/modules/b6930dbf-99c1-45a7-8372-3e43611dce21/lessons/5cf536d4-14ca-474c-b3c2-4e1ac9da2c0a/concepts/20503fe1-ec10-4138-9ecd-9737c280e18c
  # GOT ERROR: IndentationError [FIXED]
  CORS(app, resources={'/': {'origins': '*'}})


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # ADDS HEADERS TO THE RESPONSE
  # HELP CAN BE FOUND: https://r848940c899823xjupyteri5y8ngkd.udacity-student-workspaces.com/notebooks/flask-cors.ipynb
  @app.after_request
  def after_request(response):
      """Set Access Control."""

      response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type, Authorization, true')
      response.headers.add(
          'Access-Control-Allow-Methods',
          'GET, POST, PATCH, DELETE, OPTIONS')

      return response
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_all_categories():
        """Get categories endpoint.

        This endpoint returns all categories or status code 500 if there
        is a server error
        """

        try:
            # GET ALL CATEGORIES FROM DATABASE
            categories = Category.query.all()

            # Keep getting errors. Found categories do not match front-end, so add a new objects to match.
            categories_all = {}
            for category in categories:
                categories_all[category.id] = category.type

            # return a 200 server response
            return jsonify({
                'success': True,
                'categories': categories_all
            }), 200
        except Exception:
            abort(500)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
   # GOT ERROR: IndentationError [FIXED]
  @app.route('/questions')
  def get_questions():

      # paginate all categories and questions
      questions = Question.query.order_by(Question.id).all()
      total_questions = len(questions)
      categories = Category.query.order_by(Category.id).all()

      # paginate questions
      formated_questions = questions_page_numbers(
          request, questions,
          QUESTIONS_PER_PAGE)

      #  404 error if  no questions are available
      if (len(formated_questions) == 0):
          abort(404)

      categories_all = {}
      for category in categories:
          categories_all[category.id] = category.type

      # Successful Query
      return jsonify({
          'success': True,
          'total_questions': total_questions,
          'categories': categories_all,
          'questions': formated_questions
      }), 200

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

   # GOT ERROR: IndentationError [FIXED]
   # Delete Question Id
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      try:
          question = Question.query.get(id)
          question.delete()

          return jsonify({
              'success': True,
              'message': "Question successfully deleted"
          }), 200
      except Exception:
          abort(422)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

   # GOT ERROR: IndentationError [FIXED]
  # Submit and add question
  @app.route('/questions', methods=['POST'])
  def create_question():
      
      data = request.get_json()

      # Get JSON data
      question = data.get('question', '')
      answer = data.get('answer', '')
      difficulty = data.get('difficulty', '')
      category = data.get('category', '')

      # abort if question or answer are blank
      if ((question == '') or (answer == '')
              or (difficulty == '') or (category == '')):
          abort(422)

      try:
          # Success. Add question
          question = Question(
              question=question,
              answer=answer,
              difficulty=difficulty,
              category=category)

          # insert question into db
          question.insert()

          # Successful message
          return jsonify({
              'success': True,
              'message': 'Question successfully created!'
          }), 201

      except Exception:
          # return 422 status code if Exception
          abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  #Search for keyword
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
      data = request.get_json()
      searched_keyword = data.get('searchTerm', '')

      # if search term is empty return 422 status
      if searched_keyword == '':
          abort(422)

      try:
          # Query questions containing search term
          questions = Question.query.filter(
              Question.question.ilike(f'%{searched_keyword}%')).all()

          # Return 404 error if keyword is not found
          if len(questions) == 0:
              abort(404)

          # question pages
          paginated_questions = questions_page_numbers(
              request, questions,
              QUESTIONS_PER_PAGE)

          # Success 200
          return jsonify({
              'success': True,
              'questions': paginated_questions,
              'total_questions': len(Question.query.all())
          }), 200

      except Exception:
          # return 404 if Exception
          abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # Get specific category's questions
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):

      # Match category id number
      category = Category.query.filter_by(id=id).one_or_none()

      # if category is not found, return 422
      if (category is None):
          abort(422)

      questions = Question.query.filter_by(category=id).all()

      # paginate questions per page
      paginated_questions = questions_page_numbers(
          request, questions,
          QUESTIONS_PER_PAGE)

      # Success: return the JSON results
      return jsonify({
          'success': True,
          'questions': paginated_questions,
          'total_questions': len(questions),
          'current_category': category.type
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  # get question to Pla quiz
  @app.route('/quizzes', methods=['POST'])
  def play_quiz_question():
      
      data = request.get_json()
      previous_questions = data.get('previous_questions')
      quiz_category = data.get('quiz_category')

      # Check if quiz category is not found and return error
      if ((quiz_category is None) or (previous_questions is None)):
          abort(400)


      # get all questions if the default is equals to 0
      if (quiz_category['id'] == 0):
          questions = Question.query.all()
      else:
          questions = Question.query.filter_by(
              category=quiz_category['id']).all()

      # Generate a random question number
      def generate_random_question():
          return questions[random.randint(0, len(questions)-1)]

      # Get next question
      next_question = generate_random_question()

      # Asuume question is the same
      found = True

    # loop to find if the question is the same
      while found:
          if next_question.id in previous_questions:
              next_question = generate_random_question()
          else:
            # Not the same
              found = False

      return jsonify({
          'success': True,
          'question': next_question.format(),
      }), 200

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  # Error handler for Bad Request (400)
# Common Codes:

#     200: OK
#     201: Created
#     304: Not Modified
#     400: Bad Request
#     401: Unauthorized
#     404: Not Found
#     422: Unprocessable entity
#     405: Method Not Allowed
#     500: Internal Server Error

  # 400: Bad Request
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad Request'
      }), 400

  # 404: Not Found
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Not Found'
      }), 404
      
  # 422: Unprocessable entity
  @app.errorhandler(422)
  def unprocesable_entity(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable entity'
      }), 422
      
  # 500: Internal Server Error
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal Server Error'
      }), 500





# MUST IMPORT PAGINATION MODULE OR ELSE WILL GET 500 error on http://localhost:3001/questions?page=1
# TUTORIAL: https://youtu.be/sYDfHTT8DsM
  def questions_page_numbers(request, questions, num_of_questions):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * num_of_questions
      end = start + num_of_questions

      questions = [question.format() for question in questions]
      formated_questions = questions[start:end]

      return formated_questions


  return app   
    
''' common errors and how to fix them:
    
        flask.cli.NoAppException: Failed to find Flask application or factory in module "flaskr". Use "FLASK_APP=flaskr:name to specify one.
        [FIX] https://stackoverflow.com/questions/55199434/flask-cli-noappexception-failed-to-find-flask-application-or-factory-in-module/56213081
        ADD return app at the bottom of this script

        flask.cli.NoAppException: Could not import "flaskr".
        [fixed] pointing to the wrong folder where flaskr is
'''