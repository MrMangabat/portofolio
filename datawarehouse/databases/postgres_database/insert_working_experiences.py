## ----------------- Imports root path ----------------- ##
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # Adjust the path to include the root directory



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases.postgres_database.models import WorkingExperiences, Education  # Import your model
from datetime import datetime

from databases.postgres_database.create_database import Base, SQLALCHEMY_POSTGRES_URL
def format_date(date):
    return date.strftime("%B %Y")

engine = create_engine(SQLALCHEMY_POSTGRES_URL)
# Drop all tables inside the database
Base.metadata.drop_all(engine)

# Create the tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

# Create a list of WorkingExperiences instances to insert
experiences_to_insert = [
    WorkingExperiences(
        job_title='Mixologist',
        company_name='Klarbar I/S',
        job_description='Organised and executed classical and modern cocktail events',
        start_date=format_date(datetime(2016, 9, 2)),
        end_date=format_date(datetime(2021, 7, 29)),
        image_path='/src/assets/images/worklogos/klarbar.jpeg'
    ),
    WorkingExperiences(
        job_title='Project Manager',
        company_name='EnviroProcess Denmark A/S',
        job_description='Started off in a warehouse position and progressed to managing the warehouse operations. Managed various administrative duties, such as overseeing product delivery, maintaining project records, and ensuring project backup. Participated in the installation of water treatment systems for public pools and wellness centers, contributing to the adoption of a hybrid SCUM model and improving decision-making processes in medium to large projects using RACI. Assisted the executive team in driving the companys digital transformation by defining strategic objectives, establishing key performance indicators, and offering digital strategy advice.',
        start_date=format_date(datetime(2012, 2, 11)),
        end_date=format_date(datetime(2021, 8, 11)),
        image_path='/src/assets/images/worklogos/enviroprocess.jpeg'
    ),
    WorkingExperiences(
        job_title='Private Business Owner',
        company_name='MaSoul',
        job_description='Managed my own private company in industrial cleaning, project management in IT & Construction, and cocktail catering with a focus on small event and classical cocktail',
        start_date=format_date(datetime(2015, 10, 2)),
        end_date=format_date(datetime(2021, 8, 5)),
        image_path='empty string'
    ),
    WorkingExperiences(
        job_title='Business Process Improvement Intern',
        company_name='TDC Group',
        job_description='I was involved in the early stages of our companys legal separation into two distinct entities. My role included performing value stream analyses on COAX and VDSL technologies to pinpoint bottlenecks and evaluate possible capital benefits. I also supported project planning and led workshops for project leaders, emphasizing the importance of dependencies and key stakeholders in the initial phases of projects. To assist in analysis and decision-making, I employed various methodologies such as use case theory, MoSCoW prioritization, and user journey mapping, providing valuable insights to senior colleagues and management.',
        start_date=format_date(datetime(2019, 8, 1)),
        end_date=format_date(datetime(2019, 12, 29)),
        image_path='/src/assets/images/worklogos/tdc.jpeg'
    ),
    WorkingExperiences(
        job_title='Mixologist',
        company_name='Dining Six',
        job_description='Working as a mixologist at the restaurant, I specialized in crafting both traditional and contemporary cocktails, focusing particularly on classic recipes from the 1880 to 1954 era. My expertise lay in creating drinks with rum and gin, offering our guests a fusion of time-honored and modern tastes. This position demanded a thorough knowledge of cocktail history and the art of mixology, ensuring that every drink I prepared was not only delicious but also embodied the spirit of classic cocktail-making..',
        start_date=format_date(datetime(2016, 9, 17)),
        end_date=format_date(datetime(2019, 8, 29)),
        image_path='/src/assets/images/worklogos/diningsix.jpeg'
    ),
    WorkingExperiences(
        job_title='Test Manager',
        company_name='TDC Hosting',
        job_description='As a Test Manager, I led a corporate system update, focusing on prioritizing applications and allocating testing resources while working closely with super users. I managed the testing phase, navigating through complexities such as political agendas and initial research gaps. My role included leading international teams across India, Denmark, and England, which sharpened my cross-cultural communication and coordination abilities. Throughout this process, I gained substantial experience in project management and stakeholder engagement and analysis. Despite the challenges, I successfully executed the system update',
        start_date=format_date(datetime(2016, 10, 2)),
        end_date=format_date(datetime(2017, 1, 2)),
        image_path='/src/assets/images/worklogos/tdchosting.jpeg'
    ),
    WorkingExperiences(
        job_title='Mixologist',
        company_name='Scandic Webers',
        job_description='In my position as a mixologist at Scandic Webers, part of the Scandic Hotel chain, I focused on reimagining traditional cocktails with contemporary flair, particularly emphasizing gin and its rich history. Catering mainly to business clientele, I also played a key role in developing distinctive cocktails and beverage options for the entire hotel chain, thereby elevating the guest experience across the brand.',
        start_date=format_date(datetime(2015, 10, 5)),
        end_date=format_date(datetime(2016, 5, 27)),
        image_path='/src/assets/images/worklogos/scandic.jpeg'
    ),
    WorkingExperiences(
        job_title='Mixologist',
        company_name='Spring Street Social',
        job_description='As a mixologist at a premium live music venue, I excelled in crafting unique cocktails, focusing on enhancing the guest experience through techniques such as working flair, blazing cocktails, and the use of dry ice. My responsibilities extended to making homemade syrups, shrubs, and fresh juices. Additionally, I managed inventory and sourced high-quality ingredients, ensuring that every cocktail I served was not only innovative but also met the highest standards of quality',
        start_date=format_date(datetime(2015, 4, 18)),
        end_date=format_date(datetime(2015, 9, 25)),
        image_path='/src/assets/images/worklogos/springstreetsocial.jpeg'
    ),
    WorkingExperiences(
        job_title='Mixologist',
        company_name='Smoking Panda',
        job_description='Enriching the guest experience through my extensive knowledge of over 65 distinctive whiskeys and 50 rums. My responsibility involved delving into the unique histories, methods, and narratives of each distillery, thereby offering diners an educational and engaging exploration of the world of fine spirits.',
        start_date=format_date(datetime(2014, 12, 17)),
        end_date=format_date(datetime(2015, 4, 16)),
        image_path='/src/assets/images/worklogos/smokingpanda.jpeg'
    ),
    WorkingExperiences(
        job_title='Mixologist',
        company_name='Brooklyn Social',
        job_description='I oversaw a diverse collection of over 80 different gins, each with its own distinct backstory. My primary focus was on creating a variety of gin cocktails, both classic and innovative, which added a rich and distinctive flair to the overall dining atmosphere',
        start_date=format_date(datetime(2014, 9, 3)),
        end_date=format_date(datetime(2014, 12, 14)),
        image_path='/src/assets/images/worklogos/brooklynsocial.jpeg'
    ),
    WorkingExperiences(
        job_title='Mixologist',
        company_name='Remouladen',
        job_description='Emphasis on delivering customer service and sharing the unique story of Vejle Bryghus direct pipeline to our restaurant. I concentrated on engaging with guests, enriching their dining experience by underscoring the exclusive brewery-to-table aspect.',
        start_date=format_date(datetime(2013, 8, 27)),
        end_date=format_date(datetime(2014, 8, 15)),
        image_path='/src/assets/images/worklogos/remouladen.jpeg'
    ),
    WorkingExperiences(
        job_title='Bartender',
        company_name='Vinstuen',
        job_description='Focused on ensuring customer satisfaction and developed my communication skills with a varied clientele. This position offered me substantial experience in the basics of bartending and customer service',
        start_date=format_date(datetime(2011, 4, 17)),
        end_date=format_date(datetime(2014, 8, 11)),
        image_path='/src/assets/images/worklogos/vinstuen.jpeg'
    )
    # Add more instances as needed
]
education_to_insert = [
    Education(
        school_name='University of Southern Denmark',
        degree='Master of Science in Data Science',
        start_date=format_date(datetime(2021, 8, 10)),
        end_date=format_date(datetime(2023, 6, 30)),
        image_path='/src/assets/images/edulogo/SDU.jpeg'
    ),
    Education(
        school_name='Business Academy Aarhus',
        degree='Professional Bachelor of Economics & IT',
        start_date=format_date(datetime(2018, 9, 1)),
        end_date=format_date(datetime(2021, 1, 1)),
        image_path='/src/assets/images/edulogo/eaaa.jpeg'
    ),
    Education(
        school_name='The International Butler Academy',
        degree='Certified Butler & Household Manager',
        start_date=format_date(datetime(2018, 1, 15)),
        end_date=format_date(datetime(2028, 3, 17)),
        image_path='/src/assets/images/edulogo/tiba.jpeg'
    ),
    Education(
        school_name='European Bartender School',
        degree='Certified Mixologist',
        start_date=format_date(datetime(2011, 5, 13)),
        end_date=format_date(datetime(2011, 6, 13)),
        image_path='/src/assets/images/edulogo/ebs.jpeg'
    ),
    Education(
        school_name='School for Art & Design',
        degree='Preparatory Course',
        start_date=format_date(datetime(2013, 8, 1)),
        end_date=format_date(datetime(2021, 12, 28)),
        image_path='/src/assets/images/edulogo/kunstogdesign.jpeg'
    ),
]
# Add all instances to the session
session.add_all(experiences_to_insert)
session.add_all(education_to_insert)
# Commit the transaction to insert all records
session.commit()

# Close the session
session.close()