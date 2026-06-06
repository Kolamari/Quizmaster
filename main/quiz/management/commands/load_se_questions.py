#!/usr/bin/env python
"""
Management command to load 50 Software Engineering questions into the database.
Usage: python manage.py load_se_questions
"""

from django.core.management.base import BaseCommand
from quiz.models import Course, Question, Option


class Command(BaseCommand):
    help = 'Load 50 Software Engineering questions into the database'

    def handle(self, *args, **kwargs):
        # Create the course
        course, created = Course.objects.get_or_create(
            code='SE101',
            defaults={
                'name': 'Software Engineering',
                'description': 'Introduction to Software Engineering principles, practices, and methodologies'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.name}'))
        else:
            self.stdout.write(f'Using existing course: {course.name}')
        
        # 50 Software Engineering Questions
        questions_data = [
            {
                'text': 'What is Software Engineering?',
                'difficulty': 'easy',
                'explanation': 'Software Engineering is the systematic application of engineering approaches to the development of software.',
                'options': [
                    'A systematic approach to developing, operating, maintaining, and retiring software',
                    'Writing code quickly without planning',
                    'Only testing software after development',
                    'A process of hardware design'
                ],
                'correct': 0
            },
            {
                'text': 'Which of the following is NOT a phase of the Software Development Life Cycle (SDLC)?',
                'difficulty': 'easy',
                'explanation': 'Hardware Manufacturing is not part of SDLC. The main phases are Planning, Analysis, Design, Implementation, Testing, and Maintenance.',
                'options': [
                    'Planning',
                    'Analysis',
                    'Hardware Manufacturing',
                    'Maintenance'
                ],
                'correct': 2
            },
            {
                'text': 'What does the acronym SRS stand for in Software Engineering?',
                'difficulty': 'easy',
                'explanation': 'SRS stands for Software Requirements Specification, which is a document that fully defines what the software will do.',
                'options': [
                    'Software Resource System',
                    'System Requirements Specification',
                    'Software Requirements Specification',
                    'System Resource Software'
                ],
                'correct': 2
            },
            {
                'text': 'Which SDLC model is also known as the linear sequential model?',
                'difficulty': 'easy',
                'explanation': 'The Waterfall model is known as the linear sequential model because each phase must be completed before the next phase begins.',
                'options': [
                    'Spiral Model',
                    'Waterfall Model',
                    'Agile Model',
                    'RAD Model'
                ],
                'correct': 1
            },
            {
                'text': 'What is the primary goal of requirement analysis?',
                'difficulty': 'easy',
                'explanation': 'The primary goal of requirement analysis is to understand and document what the customer needs from the software system.',
                'options': [
                    'To write code',
                    'To understand user needs and system requirements',
                    'To design the database',
                    'To test the application'
                ],
                'correct': 1
            },
            {
                'text': 'Which model emphasizes risk analysis and is represented as a spiral?',
                'difficulty': 'medium',
                'explanation': 'The Spiral model, developed by Barry Boehm, combines iterative development with systematic aspects of the waterfall model and emphasizes risk analysis.',
                'options': [
                    'Waterfall Model',
                    'V-Model',
                    'Spiral Model',
                    'Incremental Model'
                ],
                'correct': 2
            },
            {
                'text': 'What is a prototype in software development?',
                'difficulty': 'easy',
                'explanation': 'A prototype is a working model of a software system used to demonstrate concepts, try out design options, and find out more about the problem and its solution.',
                'options': [
                    'The final product',
                    'A preliminary working model of the software',
                    'The documentation',
                    'The test plan'
                ],
                'correct': 1
            },
            {
                'text': 'Which testing level focuses on individual units or components of software?',
                'difficulty': 'easy',
                'explanation': 'Unit testing focuses on testing individual units or components of a software system in isolation.',
                'options': [
                    'Integration Testing',
                    'System Testing',
                    'Unit Testing',
                    'Acceptance Testing'
                ],
                'correct': 2
            },
            {
                'text': 'What does UML stand for?',
                'difficulty': 'easy',
                'explanation': 'UML stands for Unified Modeling Language, which is a standardized general-purpose modeling language in software engineering.',
                'options': [
                    'Unified Modeling Language',
                    'Universal Modeling Language',
                    'Unified Modern Language',
                    'Universal Modern Language'
                ],
                'correct': 0
            },
            {
                'text': 'Which UML diagram is used to show the static structure of a system?',
                'difficulty': 'easy',
                'explanation': 'A class diagram shows the static structure of a system by displaying its classes, attributes, methods, and relationships.',
                'options': [
                    'Sequence Diagram',
                    'Use Case Diagram',
                    'Class Diagram',
                    'Activity Diagram'
                ],
                'correct': 2
            },
            {
                'text': 'What is cohesion in software design?',
                'difficulty': 'medium',
                'explanation': 'Cohesion measures how closely the elements within a module are related to each other. High cohesion means the elements work together for a single, well-defined purpose.',
                'options': [
                    'The degree of interdependence between modules',
                    'The measure of how closely elements in a module are related',
                    'The number of lines of code in a module',
                    'The complexity of the module'
                ],
                'correct': 1
            },
            {
                'text': 'What is coupling in software design?',
                'difficulty': 'medium',
                'explanation': 'Coupling is the degree of interdependence between software modules. Low coupling is desirable as it means modules are more independent.',
                'options': [
                    'The measure of how closely elements in a module are related',
                    'The degree of interdependence between modules',
                    'The number of functions in a module',
                    'The size of the module'
                ],
                'correct': 1
            },
            {
                'text': 'Which design principle suggests that classes should be open for extension but closed for modification?',
                'difficulty': 'medium',
                'explanation': 'The Open/Closed Principle (OCP) states that software entities should be open for extension but closed for modification.',
                'options': [
                    'Single Responsibility Principle',
                    'Open/Closed Principle',
                    'Liskov Substitution Principle',
                    'Dependency Inversion Principle'
                ],
                'correct': 1
            },
            {
                'text': 'What is the Agile Manifesto?',
                'difficulty': 'easy',
                'explanation': 'The Agile Manifesto is a declaration of the values and principles for agile software development, created in 2001 by 17 software developers.',
                'options': [
                    'A project management tool',
                    'A document that defines values and principles for agile development',
                    'A programming language',
                    'A testing framework'
                ],
                'correct': 1
            },
            {
                'text': 'Which agile framework uses sprints, typically 2-4 weeks long?',
                'difficulty': 'easy',
                'explanation': 'Scrum is an agile framework that uses time-boxed iterations called sprints, usually 2-4 weeks long.',
                'options': [
                    'Kanban',
                    'Extreme Programming',
                    'Scrum',
                    'Lean'
                ],
                'correct': 2
            },
            {
                'text': 'What is a user story in agile development?',
                'difficulty': 'easy',
                'explanation': 'A user story is an informal, natural language description of features from an end-user perspective, following the format: As a [user], I want [feature] so that [benefit].',
                'options': [
                    'A technical specification document',
                    'An informal description of a feature from an end-user perspective',
                    'A code comment',
                    'A test case'
                ],
                'correct': 1
            },
            {
                'text': 'What is refactoring in software development?',
                'difficulty': 'easy',
                'explanation': 'Refactoring is the process of restructuring existing code without changing its external behavior to improve nonfunctional attributes.',
                'options': [
                    'Writing new features',
                    'Restructuring code without changing its external behavior',
                    'Debugging code',
                    'Writing documentation'
                ],
                'correct': 1
            },
            {
                'text': 'Which version control system is distributed?',
                'difficulty': 'easy',
                'explanation': 'Git is a distributed version control system, meaning every developer has a full copy of the repository including its history.',
                'options': [
                    'SVN',
                    'CVS',
                    'Git',
                    'Perforce'
                ],
                'correct': 2
            },
            {
                'text': 'What is Continuous Integration (CI)?',
                'difficulty': 'medium',
                'explanation': 'Continuous Integration is the practice of frequently merging code changes into a central repository, followed by automated builds and tests.',
                'options': [
                    'Deploying code to production manually',
                    'Frequently merging code changes with automated builds and tests',
                    'Writing code continuously without breaks',
                    'A type of software testing'
                ],
                'correct': 1
            },
            {
                'text': 'What is the purpose of a Use Case diagram?',
                'difficulty': 'easy',
                'explanation': 'A Use Case diagram shows the interactions between actors (users or external systems) and the system, describing the functionality from the user perspective.',
                'options': [
                    'To show the database schema',
                    'To show interactions between actors and the system',
                    'To show the code structure',
                    'To show network topology'
                ],
                'correct': 1
            },
            {
                'text': 'What is black-box testing?',
                'difficulty': 'easy',
                'explanation': 'Black-box testing tests the functionality of software without knowing its internal code structure, implementation details, or internal paths.',
                'options': [
                    'Testing with knowledge of internal code structure',
                    'Testing functionality without knowledge of internal code',
                    'Testing only the user interface',
                    'Testing with automated tools only'
                ],
                'correct': 1
            },
            {
                'text': 'What is white-box testing?',
                'difficulty': 'easy',
                'explanation': 'White-box testing (also called clear-box or glass-box testing) tests internal structures and workings of an application.',
                'options': [
                    'Testing without knowledge of internal code',
                    'Testing internal code structures and logic',
                    'Testing only the database',
                    'Testing user acceptance'
                ],
                'correct': 1
            },
            {
                'text': 'What is regression testing?',
                'difficulty': 'medium',
                'explanation': 'Regression testing is re-testing software after changes to ensure that existing functionality still works correctly.',
                'options': [
                    'Testing new features only',
                    'Re-testing after changes to ensure existing functionality works',
                    'Testing the user interface',
                    'Testing database performance'
                ],
                'correct': 1
            },
            {
                'text': 'Which design pattern ensures only one instance of a class exists?',
                'difficulty': 'medium',
                'explanation': 'The Singleton pattern restricts the instantiation of a class to one single instance and provides a global point of access to it.',
                'options': [
                    'Factory Pattern',
                    'Observer Pattern',
                    'Singleton Pattern',
                    'Strategy Pattern'
                ],
                'correct': 2
            },
            {
                'text': 'What is the difference between verification and validation?',
                'difficulty': 'medium',
                'explanation': 'Verification checks whether the product is built correctly (conformance to specifications), while validation checks whether the right product is built (meets user needs).',
                'options': [
                    'They are the same thing',
                    'Verification: Are we building the product right? Validation: Are we building the right product?',
                    'Verification is testing, validation is documentation',
                    'Verification is for code, validation is for design'
                ],
                'correct': 1
            },
            {
                'text': 'What is technical debt?',
                'difficulty': 'medium',
                'explanation': 'Technical debt is the implied cost of additional rework caused by choosing an easy (limited) solution now instead of using a better approach that would take longer.',
                'options': [
                    'Money spent on hardware',
                    'The implied cost of rework from choosing quick solutions over better approaches',
                    'Cost of hiring developers',
                    'Licensing fees for software'
                ],
                'correct': 1
            },
            {
                'text': 'What is a software metric?',
                'difficulty': 'easy',
                'explanation': 'A software metric is a measure of software characteristics that are quantifiable or countable, used to assess software quality, cost, or progress.',
                'options': [
                    'A type of software tool',
                    'A quantitative measure of software characteristics',
                    'A programming language feature',
                    'A type of database'
                ],
                'correct': 1
            },
            {
                'text': 'What does COCOMO stand for?',
                'difficulty': 'medium',
                'explanation': 'COCOMO stands for Constructive Cost Model, a procedural software cost estimation model developed by Barry Boehm.',
                'options': [
                    'Complex Code Model',
                    'Constructive Cost Model',
                    'Comprehensive Coding Method',
                    'Computer Cost Measurement'
                ],
                'correct': 1
            },
            {
                'text': 'What is the purpose of a Gantt chart in project management?',
                'difficulty': 'easy',
                'explanation': 'A Gantt chart is a bar chart that illustrates a project schedule, showing start and finish dates of project elements.',
                'options': [
                    'To write code',
                    'To illustrate a project schedule with timelines',
                    'To design databases',
                    'To test software'
                ],
                'correct': 1
            },
            {
                'text': 'Which software development model is best suited for projects with unclear or changing requirements?',
                'difficulty': 'medium',
                'explanation': 'The Spiral model is best for projects with high risks and unclear requirements because it emphasizes risk analysis and iterative development.',
                'options': [
                    'Waterfall Model',
                    'V-Model',
                    'Spiral Model',
                    'RAD Model'
                ],
                'correct': 2
            },
            {
                'text': 'What is the primary purpose of a Data Flow Diagram (DFD)?',
                'difficulty': 'medium',
                'explanation': 'A Data Flow Diagram shows how data flows through a system, including inputs, outputs, data stores, and processes.',
                'options': [
                    'To show the user interface design',
                    'To show how data moves through a system',
                    'To write test cases',
                    'To manage project schedules'
                ],
                'correct': 1
            },
            {
                'text': 'What is the difference between functional and non-functional requirements?',
                'difficulty': 'easy',
                'explanation': 'Functional requirements specify what the system should do, while non-functional requirements specify how the system should behave (performance, security, usability).',
                'options': [
                    'Functional requirements are more important',
                    'Functional: what the system does; Non-functional: how the system performs',
                    'There is no difference',
                    'Non-functional requirements are optional'
                ],
                'correct': 1
            },
            {
                'text': 'What is a software design pattern?',
                'difficulty': 'easy',
                'explanation': 'A design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design.',
                'options': [
                    'A specific piece of code',
                    'A reusable solution to a common software design problem',
                    'A type of programming language',
                    'A testing methodology'
                ],
                'correct': 1
            },
            {
                'text': 'Which SOLID principle states that a class should have only one reason to change?',
                'difficulty': 'medium',
                'explanation': 'The Single Responsibility Principle (SRP) states that a class should have only one reason to change, meaning it should have only one job or responsibility.',
                'options': [
                    'Open/Closed Principle',
                    'Single Responsibility Principle',
                    'Liskov Substitution Principle',
                    'Interface Segregation Principle'
                ],
                'correct': 1
            },
            {
                'text': 'What is the purpose of a Sequence Diagram?',
                'difficulty': 'easy',
                'explanation': 'A Sequence Diagram shows interactions between objects in a time-ordered sequence, displaying the messages passed between objects.',
                'options': [
                    'To show class hierarchies',
                    'To show interactions between objects in time sequence',
                    'To show database schemas',
                    'To show project timelines'
                ],
                'correct': 1
            },
            {
                'text': 'What is DevOps?',
                'difficulty': 'easy',
                'explanation': 'DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the systems development life cycle.',
                'options': [
                    'A programming language',
                    'A combination of development and operations practices for faster delivery',
                    'A type of database',
                    'A testing framework'
                ],
                'correct': 1
            },
            {
                'text': 'What is Docker used for in software development?',
                'difficulty': 'medium',
                'explanation': 'Docker is a containerization platform that packages applications with their dependencies into containers for consistent deployment.',
                'options': [
                    'To write code',
                    'To containerize applications with their dependencies',
                    'To design user interfaces',
                    'To manage databases'
                ],
                'correct': 1
            },
            {
                'text': 'What is the difference between alpha and beta testing?',
                'difficulty': 'medium',
                'explanation': 'Alpha testing is done by developers/internal teams, while beta testing is done by end-users in a real-world environment.',
                'options': [
                    'Alpha is done by users, beta by developers',
                    'Alpha is done internally, beta by external users',
                    'They are the same type of testing',
                    'Alpha is automated, beta is manual'
                ],
                'correct': 1
            },
            {
                'text': 'What is an API?',
                'difficulty': 'easy',
                'explanation': 'An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other.',
                'options': [
                    'A programming language',
                    'A set of protocols for building software applications',
                    'A type of database',
                    'A user interface'
                ],
                'correct': 1
            },
            {
                'text': 'What is the MVC architecture pattern?',
                'difficulty': 'medium',
                'explanation': 'MVC (Model-View-Controller) separates an application into three components: Model (data), View (UI), and Controller (logic).',
                'options': [
                    'A database design pattern',
                    'An architecture pattern separating Model, View, and Controller',
                    'A testing methodology',
                    'A programming language'
                ],
                'correct': 1
            },
            {
                'text': 'What is the purpose of a state diagram?',
                'difficulty': 'medium',
                'explanation': 'A state diagram (or state machine diagram) describes the states an object can be in and the transitions between those states.',
                'options': [
                    'To show database relationships',
                    'To model states and transitions of an object',
                    'To show project timelines',
                    'To document code'
                ],
                'correct': 1
            },
            {
                'text': 'What is load testing?',
                'difficulty': 'easy',
                'explanation': 'Load testing evaluates system behavior under a specific expected load, typically measuring response times and resource utilization.',
                'options': [
                    'Testing with no data',
                    'Testing system behavior under expected load conditions',
                    'Testing individual functions',
                    'Testing the user interface'
                ],
                'correct': 1
            },
            {
                'text': 'What is the primary advantage of the Agile methodology over Waterfall?',
                'difficulty': 'easy',
                'explanation': 'Agile allows for iterative development with frequent feedback and adaptation to changing requirements, unlike the rigid sequential Waterfall approach.',
                'options': [
                    'It requires less documentation',
                    'It allows for flexibility and adaptation to changing requirements',
                    'It is faster to implement',
                    'It requires fewer developers'
                ],
                'correct': 1
            },
            {
                'text': 'What is a software framework?',
                'difficulty': 'easy',
                'explanation': 'A software framework is a platform for developing software applications that provides a foundation and reusable components.',
                'options': [
                    'A programming language',
                    'A reusable platform with pre-built components for application development',
                    'A type of database',
                    'A testing tool'
                ],
                'correct': 1
            },
            {
                'text': 'What is the purpose of a ER Diagram?',
                'difficulty': 'easy',
                'explanation': 'An ER (Entity-Relationship) Diagram is used to design databases by showing entities, their attributes, and relationships between entities.',
                'options': [
                    'To show user interfaces',
                    'To design databases by showing entities and relationships',
                    'To write code',
                    'To test applications'
                ],
                'correct': 1
            },
            {
                'text': 'What is incremental development?',
                'difficulty': 'medium',
                'explanation': 'Incremental development breaks the development process into smaller increments, delivering functionality in portions.',
                'options': [
                    'Developing the entire system at once',
                    'Developing the system in small, incremental portions',
                    'Developing without any planning',
                    'Developing only the user interface'
                ],
                'correct': 1
            },
            {
                'text': 'What is the main purpose of software configuration management?',
                'difficulty': 'medium',
                'explanation': 'Software Configuration Management (SCM) tracks and controls changes in software, including version control, change management, and release management.',
                'options': [
                    'To write code faster',
                    'To track and control changes in software throughout its lifecycle',
                    'To design user interfaces',
                    'To test software'
                ],
                'correct': 1
            },
            {
                'text': 'What is a build tool in software development?',
                'difficulty': 'easy',
                'explanation': 'A build tool automates the process of compiling source code, running tests, and packaging applications.',
                'options': [
                    'A tool for writing code',
                    'A tool that automates compilation, testing, and packaging',
                    'A tool for designing interfaces',
                    'A tool for managing databases'
                ],
                'correct': 1
            },
            {
                'text': 'What is the difference between a compiler and an interpreter?',
                'difficulty': 'easy',
                'explanation': 'A compiler translates the entire source code to machine code before execution, while an interpreter translates and executes code line by line.',
                'options': [
                    'They are the same thing',
                    'Compiler translates all code at once; Interpreter translates line by line',
                    'Compiler is for web, interpreter is for desktop',
                    'Compiler is faster than interpreter always'
                ],
                'correct': 1
            },
            {
                'text': 'What is a software requirement?',
                'difficulty': 'easy',
                'explanation': 'A software requirement is a condition or capability needed by a user to solve a problem or achieve an objective.',
                'options': [
                    'A programming language feature',
                    'A condition or capability needed by a user',
                    'A type of software license',
                    'A hardware specification'
                ],
                'correct': 1
            },
            {
                'text': 'What is risk management in software engineering?',
                'difficulty': 'medium',
                'explanation': 'Risk management in software engineering involves identifying, analyzing, and responding to risks that could affect project success.',
                'options': [
                    'Avoiding all risks completely',
                    'Identifying, analyzing, and responding to project risks',
                    'Only financial planning',
                    'Hiring more developers'
                ],
                'correct': 1
            },
            {
                'text': 'What is the purpose of a test plan?',
                'difficulty': 'easy',
                'explanation': 'A test plan documents the scope, approach, resources, and schedule of testing activities for a software project.',
                'options': [
                    'To write code',
                    'To document the scope, approach, and schedule of testing',
                    'To design the user interface',
                    'To manage project budget'
                ],
                'correct': 1
            },
            {
                'text': 'Which UML diagram shows the flow of control from activity to activity?',
                'difficulty': 'easy',
                'explanation': 'An Activity Diagram models the workflow or business and operational step-by-step activities of a system.',
                'options': [
                    'Class Diagram',
                    'Activity Diagram',
                    'Sequence Diagram',
                    'State Diagram'
                ],
                'correct': 1
            },
            {
                'text': 'What is modular programming?',
                'difficulty': 'easy',
                'explanation': 'Modular programming is a technique that separates the functionality of a program into independent, interchangeable modules.',
                'options': [
                    'Writing all code in one file',
                    'Separating functionality into independent, interchangeable modules',
                    'Using only one programming language',
                    'Writing code without functions'
                ],
                'correct': 1
            },
            {
                'text': 'What is the main purpose of software testing?',
                'difficulty': 'easy',
                'explanation': 'The main purpose of software testing is to identify defects and ensure the software meets requirements and works as expected.',
                'options': [
                    'To prove there are no bugs',
                    'To identify defects and ensure the software meets requirements',
                    'To write better code',
                    'To reduce development time'
                ],
                'correct': 1
            },
        ]
        
        # Clear existing questions for this course
        existing_count = Question.objects.filter(course=course).count()
        if existing_count > 0:
            self.stdout.write(f'Found {existing_count} existing questions. Adding new questions...')
        
        added = 0
        skipped = 0
        
        for q_data in questions_data:
            # Check if question already exists
            if Question.objects.filter(course=course, text=q_data['text']).exists():
                skipped += 1
                continue
            
            question = Question.objects.create(
                course=course,
                text=q_data['text'],
                difficulty=q_data['difficulty'],
                explanation=q_data['explanation']
            )
            
            for i, opt_text in enumerate(q_data['options']):
                Option.objects.create(
                    question=question,
                    text=opt_text,
                    is_correct=(i == q_data['correct'])
                )
            
            added += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {added} new questions! (Skipped {skipped} duplicates)'
        ))
        self.stdout.write(f'Total questions in database: {Question.objects.filter(course=course).count()}')
