CREATE TABLE joblistings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    requirements TEXT,
    expected_experience VARCHAR(100),
    last_chance TIMESTAMP,
    listing TEXT,
    link VARCHAR(255),
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(255),
    country VARCHAR(100)
);



-- dummies
INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Software Developer',
    'Innovatech',
    'Proficiency in JavaScript, Node.js, and React. Experience with cloud platforms (AWS or Azure) is preferred.',
    'Entry-Level',
    '2024-12-01',
    'About the Job: As an Entry-Level Software Developer at Innovatech, you will have the unique opportunity to work with a dynamic and innovative team that is dedicated to developing top-notch solutions for various industries. Our clients come from diverse sectors, and we pride ourselves on building scalable, efficient, and secure software that meets their evolving needs.You will start your career working closely with experienced developers, learning the best practices in software engineering, including agile methodologies, version control, and automated testing. We believe in nurturing talent, and you will be mentored by senior developers who will help you grow into your role. You will be working with modern JavaScript technologies such as Node.js for backend services, and React for building user interfaces. You will also have the opportunity to work on cloud platforms such as AWS and Azure to deploy scalable applications.At Innovatech, we embrace innovation and continuous learning. You will be encouraged to explore new technologies, participate in coding challenges, and attend tech talks and workshops. Our collaborative culture ensures that you will be part of a team that values feedback, encourages new ideas, and celebrates technical excellence. Responsibilities: You will be responsible for developing and maintaining web applications, implementing new features, and collaborating with the design team to ensure a seamless user experience. You will also work on fixing bugs and optimizing performance for various projects. With time, you will take ownership of small to medium-sized projects, working independently under the guidance of senior team members. Career Growth: As an entry-level developer, you will have the opportunity to grow within the company. After a successful probation period, you will be given more responsibility, including the chance to lead small teams and contribute to critical decisions regarding the company’s technology stack. Our goal is to see you become a full-stack developer with strong expertise in backend and frontend technologies. We Offer: A competitive salary, comprehensive benefits package, and a flexible working environment, allowing for a healthy work-life balance. Innovatech also offers remote work options and regular team-building activities to foster a sense of community. If you are a passionate coder looking to start your career in software development, we would love to hear from you!',
    'https://www.innovatech.com/jobs/software-developer-entry',
    'San Francisco, CA',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Software Developer',
    'CodeWorks',
    'Proficiency in Python, Django, and RESTful APIs. Experience with frontend frameworks (React or Vue).',
    'Mid-Level',
    '2024-12-10',
    'About the Job: CodeWorks is looking for a Mid-Level Software Developer to join our fast-growing team. Our company provides innovative solutions to small and medium-sized businesses, helping them scale their operations and enhance productivity through technology. As a Mid-Level Developer, you will play a pivotal role in building robust web applications that solve complex problems for our clients. At CodeWorks, we believe in building full-stack developers, and you will work on both the backend (Python, Django) and the frontend (React, Vue.js) of our projects. You will collaborate with product managers and designers to bring client requirements to life, ensuring that our solutions are intuitive, scalable, and maintainable. Key Responsibilities: In this role, you will develop and maintain RESTful APIs using Django, integrate with third-party services, and write clean, modular, and testable code. You will also build user interfaces that offer seamless user experiences. As a Mid-Level Developer, you will mentor junior developers, participate in code reviews, and contribute to the company’s technical roadmap. Collaboration is at the heart of everything we do at CodeWorks. You will be part of an agile team that works closely with clients to iterate quickly and deliver high-quality software. We value creativity and problem-solving, and you will have the freedom to explore new tools and frameworks that could benefit our projects. Growth Opportunities: CodeWorks provides numerous growth opportunities. We support continuous learning, offering access to online courses and conferences. As you grow in your role, you will have the opportunity to take on leadership positions, such as becoming a technical lead for projects or managing a small team of developers. We Offer: A competitive salary, health benefits, and flexible working hours. We also provide a supportive environment that encourages work-life balance, with options for remote work. Join us and make a difference by developing software that helps businesses succeed!',
    'https://www.codeworks.com/jobs/software-developer-mid',
    'Austin, TX',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Software Developer',
    'TechNova',
    'Experience with C#, .NET, and cloud technologies (Azure). Strong knowledge of database systems (SQL Server).',
    'Senior-Level',
    '2024-11-30',
    'About the Job: TechNova is looking for a Senior Software Developer with expertise in C#, .NET, and cloud platforms to join our development team. You will be responsible for leading the design and implementation of software solutions that support critical business functions. Our company specializes in providing enterprise-level software solutions for industries such as finance, healthcare, and manufacturing. As a Senior Developer, you will take ownership of large-scale projects, working closely with stakeholders to understand business requirements and translating them into technical solutions. You will also mentor junior developers, ensuring that they follow best practices and stay up to date with the latest industry trends. Your work will involve developing both backend services using C# and .NET Core, as well as frontend interfaces when necessary. In this role, you will collaborate with DevOps teams to ensure that all applications are built with scalability and reliability in mind. You will leverage cloud technologies, specifically Microsoft Azure, to build and deploy solutions that can handle high levels of traffic and data processing. Responsibilities: As the Senior Software Developer, you will lead the software development lifecycle for assigned projects, including requirements gathering, system design, coding, testing, and deployment. You will also provide technical guidance to the team, conduct code reviews, and ensure that all software adheres to company standards for security and performance. Growth Opportunities: At TechNova, we believe in fostering leadership. As a senior member of the team, you will have the opportunity to grow into roles such as Technical Lead or Software Architect, overseeing larger teams and contributing to the strategic direction of our technology stack. We Offer: A highly competitive salary, performance-based bonuses, and a comprehensive benefits package. We also provide opportunities for career development through internal training programs and external conferences. If you are an experienced developer looking to take on a leadership role in a dynamic company, we invite you to apply.',
    'https://www.technova.com/jobs/software-developer-senior',
    'New York, NY',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Software Developer',
    'BrightCode Solutions',
    'Proficiency in Java, Spring Boot, and microservices architecture. Experience with Kubernetes is a plus.',
    'Mid-Level',
    '2024-12-05',
    'About the Job: BrightCode Solutions is looking for a Mid-Level Software Developer to help us build and scale cutting-edge microservices-based applications. We specialize in providing cloud-native solutions to clients across multiple industries, including finance, healthcare, and logistics. In this role, you will work closely with our engineering and product teams to deliver high-quality software solutions that meet the unique needs of our clients. As a Software Developer at BrightCode Solutions, you will be responsible for designing, developing, and deploying microservices using Java and Spring Boot. You will also work with Kubernetes for container orchestration, ensuring that our services are scalable, resilient, and maintainable. We are looking for a developer who is passionate about technology and enjoys solving complex problems in a collaborative environment. Key Responsibilities: In this role, you will work on building distributed systems, developing RESTful APIs, and integrating with third-party services. You will also collaborate with other engineers to implement best practices in software development, including code reviews, testing, and continuous integration/continuous deployment (CI/CD). Your day-to-day tasks will involve writing clean, modular, and maintainable code, as well as troubleshooting and debugging applications in production. At BrightCode, we believe in fostering a culture of learning and growth. You will have the opportunity to work with modern tools and technologies, such as Docker, Kubernetes, and cloud platforms like AWS and Google Cloud. Our team is committed to continuous improvement, and you will be encouraged to contribute to our evolving development processes. Growth Opportunities: As a Mid-Level Developer, you will have the opportunity to take on more responsibility as you gain experience. You will work closely with senior developers and architects, learning about software architecture, design patterns, and scaling applications in the cloud. Over time, you can grow into a senior role, where you will lead projects and mentor junior developers. We Offer: A competitive salary, comprehensive health and dental benefits, and a flexible work environment. We provide opportunities for career advancement, professional development, and work-life balance. At BrightCode Solutions, we believe that investing in our employees is key to delivering great software. Join us and help shape the future of cloud-native development!',
    'https://www.brightcodesolutions.com/jobs/software-developer-mid',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Software Developer',
    'GreenTech Solutions',
    'Experience with Ruby on Rails, JavaScript, and PostgreSQL. Familiarity with CI/CD pipelines and testing frameworks.',
    'Entry-Level',
    '2024-12-15',
    'About the Job: GreenTech Solutions is seeking an Entry-Level Software Developer to join our growing team. We are a company focused on developing sustainable technology solutions to help combat climate change. Our software solutions are used by businesses and governments to reduce carbon footprints, manage renewable energy resources, and track environmental impact. As part of our team, you will have the opportunity to work on meaningful projects that make a positive impact on the environment. In this role, you will work primarily with Ruby on Rails for backend development and JavaScript for frontend applications. You will also gain experience with PostgreSQL databases and CI/CD pipelines. Your main responsibility will be to develop new features, fix bugs, and maintain our existing applications, which are critical to helping our clients meet their sustainability goals. You will work alongside experienced developers who will provide guidance and mentorship as you grow in your role. We believe in nurturing talent and offering opportunities for continuous learning and development. Whether you are just starting your career or have a few years of experience, we provide the resources and support to help you succeed. Key Responsibilities: As an Entry-Level Software Developer, you will be responsible for writing clean and efficient code, developing new features, and optimizing our applications for performance. You will also participate in code reviews, testing, and debugging processes. Your work will involve collaborating with cross-functional teams, including product managers, UX/UI designers, and DevOps engineers. Career Growth: At GreenTech Solutions, we offer a clear path for career advancement. After a successful probation period, you will have the opportunity to take on more responsibilities, including leading small projects, mentoring interns, and contributing to the architectural decisions of our software. We Offer: A supportive work environment, competitive salary, comprehensive benefits, and the opportunity to work on projects that make a real difference. We also offer flexible working hours and remote work options. If you are passionate about software development and sustainability, this is the perfect opportunity to grow your career while making a positive impact on the planet.',
    'https://www.greentechsolutions.com/jobs/software-developer-entry',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Data Scientist',
    'DataWorld',
    'Proficiency in Python, R, SQL, and data visualization tools. Experience with machine learning algorithms is required.',
    'Entry-Level',
    '2024-11-20',
    'About the Job: DataWorld is a leading company in the data analytics space, working with businesses to harness the power of data for informed decision-making. As an Entry-Level Data Scientist, you will be part of a cutting-edge team that works on solving real-world problems using data. Whether it’s predicting customer behavior or optimizing supply chains, your contributions will have a direct impact on our clients’ success. You will work with large datasets, cleaning and preprocessing data to ensure it is ready for analysis. You will then apply machine learning algorithms and statistical techniques to uncover trends and patterns. You will have the opportunity to work with tools such as Python, R, and SQL to build predictive models. In addition to coding, you will also create data visualizations using Tableau or PowerBI to communicate insights to stakeholders. We encourage experimentation and innovation at DataWorld. You will be supported by a team of senior data scientists who will mentor you and provide guidance as you grow in your role. Our projects range from small one-off analyses to large, multi-year initiatives, giving you the opportunity to work on a variety of interesting challenges. Key Responsibilities: You will be responsible for developing models that solve specific business problems, from recommendation systems to anomaly detection. You will also work on data wrangling and analysis, cleaning large datasets, and preparing them for machine learning pipelines. Additionally, you will participate in cross-functional teams, collaborating with product managers, engineers, and designers to deliver solutions that make a difference. Growth Path: At DataWorld, we believe in fostering talent. Entry-Level Data Scientists have the opportunity to advance to more senior roles, where they can take ownership of projects, lead teams, and contribute to the development of new products. We Offer: A dynamic working environment with opportunities for growth and learning, a competitive salary, health benefits, and a hybrid working model that allows flexibility. Join us and be a part of a team that is shaping the future of data-driven decision making.',
    'https://www.dataworld.com/jobs/data-scientist-entry',
    'Boston, MA',
    'USA'
);


INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Data Scientist',
    'InsightX',
    'Experience with SQL, machine learning models, and cloud services (AWS or GCP). Strong knowledge of data pipelines is a plus.',
    'Mid-Level',
    '2024-11-30',
    'About the Job: InsightX is a fast-growing data analytics company that helps businesses leverage data to make informed decisions. We are looking for a Mid-Level Data Scientist to join our team and contribute to building cutting-edge machine learning models and data pipelines. In this role, you will work with a diverse team of data scientists, engineers, and analysts to deliver solutions that drive business outcomes. As a Data Scientist at InsightX, you will be responsible for developing predictive models, conducting data analysis, and building data pipelines using tools such as SQL, Python, and cloud services like AWS or GCP. You will work on projects that involve large datasets, requiring you to preprocess data, perform feature engineering, and deploy models into production environments. Key Responsibilities: In this role, you will work closely with cross-functional teams to identify business problems that can be solved using data. You will apply machine learning techniques to build models that predict customer behavior, optimize processes, and provide actionable insights. You will also work on automating data pipelines and ensuring the scalability and reliability of our data infrastructure. At InsightX, we foster a collaborative environment where data scientists are encouraged to take ownership of their projects. You will have the opportunity to present your findings to clients and internal stakeholders, helping them understand how data-driven solutions can improve business performance. Growth Opportunities: As a Mid-Level Data Scientist, you will have the chance to grow into more senior roles, where you will lead teams, mentor junior data scientists, and contribute to the development of new data products. We also offer opportunities for professional development, including access to online courses, conferences, and internal training programs. We Offer: A dynamic work environment with opportunities for growth and learning, competitive salary, comprehensive health benefits, and the flexibility to work remotely or in our Toronto office. At InsightX, we are committed to fostering a culture of innovation and collaboration. Join us and help shape the future of data science!',
    'https://www.insightx.com/jobs/data-scientist-mid',
    'Toronto, Canada',
    'Canada'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Data Scientist',
    'Quantify AI',
    'Proficiency in deep learning frameworks such as TensorFlow or PyTorch. Experience with big data tools (Hadoop, Spark).',
    'Senior-Level',
    '2024-12-01',
    'About the Job: Quantify AI is hiring a Senior Data Scientist to develop state-of-the-art AI models and handle large-scale data processing. As a leader in artificial intelligence and big data analytics, we work with global clients to harness the power of data to drive business innovation. In this role, you will work on some of the most challenging and exciting projects in the field of AI, using cutting-edge technologies to deliver impactful results. As a Senior Data Scientist, you will lead the development of deep learning models, natural language processing (NLP) applications, and large-scale data pipelines. You will work with a talented team of engineers and data scientists to build and deploy AI solutions that solve real-world business problems. Your work will involve designing and optimizing models, tuning hyperparameters, and improving model performance. Key Responsibilities: In this role, you will lead projects from conception to deployment, working closely with clients to understand their business needs and translate them into data science solutions. You will also be responsible for mentoring junior data scientists, conducting code reviews, and contributing to the overall data strategy of the company. At Quantify AI, we believe in fostering a culture of innovation and continuous learning. You will have access to the latest tools and technologies, as well as opportunities to attend conferences and workshops to stay at the forefront of the field. Growth Opportunities: As a Senior Data Scientist, you will have the opportunity to grow into leadership roles, such as Principal Data Scientist or Head of Data Science. You will also play a key role in shaping the company’s data strategy and contributing to the development of new AI products. We Offer: A highly competitive salary, stock options, comprehensive health benefits, and the flexibility to work remotely. Join us and be part of a company that is at the cutting edge of AI and data science innovation.',
    'https://www.quantifyai.com/jobs/data-scientist-senior',
    'Los Angeles, CA',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Data Scientist',
    'FutureData Labs',
    'Experience with predictive modeling, data wrangling, and statistical analysis. Expertise in SQL and NoSQL databases is required.',
    'Mid-Level',
    '2024-11-25',
    'About the Job: FutureData Labs is seeking a Data Scientist to join our team and work on predictive models that drive business strategy. As a Mid-Level Data Scientist, you will have the opportunity to apply your skills in data analysis, machine learning, and statistical modeling to solve complex business problems for clients across various industries. In this role, you will work with large datasets, preprocess data, and build predictive models using a variety of machine learning algorithms. You will collaborate with data engineers to ensure that our data pipelines are efficient and scalable. Additionally, you will create data visualizations and reports that communicate key insights to stakeholders and help guide business decisions. We are looking for a candidate who is passionate about data and enjoys working in a collaborative environment. You will have the opportunity to work with modern data tools such as Python, SQL, and cloud platforms like AWS. Your work will directly impact the success of our clients by providing them with actionable insights that drive growth. Key Responsibilities: In this role, you will be responsible for developing predictive models, conducting data analysis, and working closely with cross-functional teams to implement data-driven solutions. You will also have the opportunity to explore new data sources, develop data pipelines, and contribute to the development of data products that enhance our clients’ operations. Growth Opportunities: As a Mid-Level Data Scientist, you will have the opportunity to grow into senior roles, where you will take on more responsibility and lead data science projects. We provide opportunities for continuous learning and professional development, including access to online courses, conferences, and mentorship programs. We Offer: A competitive salary, comprehensive health benefits, and the flexibility to work remotely or in our Berlin office. At FutureData Labs, we are committed to creating a collaborative and innovative work environment where employees can grow and thrive. Join us and be part of a team that is shaping the future of data-driven business solutions!',
    'https://www.futuredata.com/jobs/data-scientist-mid',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Data Scientist',
    'TechAnalytics',
    'Proficiency in Python, machine learning techniques, and working knowledge of Tableau or PowerBI.',
    'Entry-Level',
    '2024-12-10',
    'About the Job: TechAnalytics is looking for an Entry-Level Data Scientist to work on projects involving data analysis and reporting for clients across various industries. In this role, you will use your skills in Python and machine learning to develop models that help businesses make data-driven decisions. You will also create dashboards and visualizations using tools like Tableau and PowerBI to communicate insights to stakeholders. As an Entry-Level Data Scientist, you will work closely with senior data scientists and engineers to learn best practices in data wrangling, model development, and data visualization. You will have the opportunity to work on real-world projects that have a direct impact on our clients’ success. Whether it’s predicting customer churn, optimizing marketing campaigns, or improving operational efficiency, your work will help drive business outcomes. Key Responsibilities: You will be responsible for cleaning and preprocessing data, building machine learning models, and creating visualizations that communicate insights to stakeholders. You will also work on automating data analysis workflows and contributing to the development of data products. At TechAnalytics, we believe in fostering a collaborative work environment where team members can learn from each other and grow in their roles. You will have access to training programs, mentorship, and opportunities to attend conferences and workshops to stay up to date with the latest trends in data science. Growth Opportunities: As an Entry-Level Data Scientist, you will have the opportunity to grow into more senior roles as you gain experience. We offer a clear career path, with opportunities for promotion and professional development. We Offer: A competitive salary, comprehensive health benefits, and a flexible work environment. We also offer opportunities for remote work and professional development. Join us and help shape the future of data science at TechAnalytics!',
    'https://www.techanalytics.com/jobs/data-scientist-entry',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Business Development Manager',
    'Global Ventures',
    'Experience in sales strategy, client engagement, and business growth. Experience in managing key accounts is a plus.',
    'Senior-Level',
    '2024-11-25',
    'About the Job: Global Ventures is looking for an experienced Senior Business Development Manager to lead efforts in expanding into new global markets. As a key player in the company’s growth strategy, you will be responsible for identifying new business opportunities, developing strategic partnerships, and driving revenue growth across multiple regions. In this role, you will work closely with our executive team to develop and execute business strategies that align with our global vision. Your responsibilities will include managing relationships with key clients, negotiating deals, and closing high-value contracts. You will also work on developing new market entry strategies, identifying potential partners, and overseeing the sales pipeline. As the Senior Business Development Manager, you will lead a team of business development professionals, providing mentorship and guidance to help them achieve their targets. Key Responsibilities: In this role, you will develop and implement business development strategies, identify new revenue streams, and build relationships with key stakeholders. You will also work closely with marketing and product teams to ensure that our offerings align with market demands. Your role will involve extensive networking, attending industry events, and representing Global Ventures at conferences and trade shows. Growth Opportunities: At Global Ventures, we believe in fostering leadership. As a senior member of the team, you will have the opportunity to take on additional responsibilities, such as managing larger teams, overseeing global expansion projects, and contributing to the company’s long-term growth strategy. We Offer: A highly competitive salary, performance-based bonuses, and comprehensive health and retirement benefits. We also offer opportunities for career development and professional growth, including access to leadership training programs and executive mentorship.',
    'https://www.globalventures.com/jobs/business-development-senior',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Business Development Manager',
    'MarketPro',
    'Proven track record in sales and business development. Knowledge of marketing strategies and B2B sales is required.',
    'Mid-Level',
    '2024-12-05',
    'About the Job: MarketPro is looking for a Mid-Level Business Development Manager to help expand our portfolio of B2B clients and drive business growth. In this role, you will be responsible for identifying new business opportunities, nurturing client relationships, and executing strategies that increase our market share. You will work closely with our sales and marketing teams to align business development initiatives with overall company goals. As a Business Development Manager at MarketPro, you will be the driving force behind our sales strategy, working to grow our presence in key markets. You will engage with potential clients, understand their business needs, and provide tailored solutions that add value to their operations. Your ability to build and maintain long-lasting relationships will be key to your success. Key Responsibilities: In this role, you will develop and manage a pipeline of new business opportunities, from lead generation to deal closure. You will work with cross-functional teams to ensure that our solutions meet the needs of our clients and exceed their expectations. You will also represent MarketPro at industry events, networking with potential clients and partners to build new relationships. Growth Opportunities: MarketPro offers a dynamic work environment with ample opportunities for growth. As a Mid-Level Business Development Manager, you will have the chance to move into more senior roles, such as Director of Business Development or Sales Manager. We provide ongoing training and professional development to help you succeed in your role. We Offer: A competitive salary, commission-based incentives, health benefits, and a collaborative work environment. We also offer opportunities for career growth and advancement. Join us at MarketPro and be a part of a company that is transforming the B2B market!',
    'https://www.marketpro.com/jobs/business-development-mid',
    'New York, NY',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Business Development Manager',
    'TechBridge',
    'Experience in developing strategic partnerships, client acquisition, and revenue growth. Knowledge of tech industry is a plus.',
    'Senior-Level',
    '2024-12-01',
    'About the Job: TechBridge is a leading technology company that specializes in providing digital solutions to businesses across the globe. We are seeking a Senior Business Development Manager to lead our efforts in expanding our market presence and growing our client base. In this role, you will work closely with our executive team to identify new business opportunities, build strategic partnerships, and drive revenue growth. As a Senior Business Development Manager at TechBridge, you will be responsible for identifying new markets, building relationships with key stakeholders, and negotiating high-value contracts. You will also be responsible for leading our sales strategy, ensuring that we meet our revenue targets and continue to grow our market share. Key Responsibilities: You will be responsible for developing and executing business development strategies, managing key client relationships, and overseeing the sales process from lead generation to deal closure. You will also work with our marketing and product teams to ensure that our solutions are aligned with market demands. Growth Opportunities: TechBridge offers a fast-paced and dynamic work environment with ample opportunities for growth. As a Senior Business Development Manager, you will have the opportunity to move into more senior leadership roles, such as Director of Business Development or Vice President of Sales. We Offer: A highly competitive salary, performance-based bonuses, and comprehensive health and retirement benefits. We also provide opportunities for career development and professional growth, including leadership training programs and executive mentorship. Join TechBridge and help shape the future of digital solutions!',
    'https://www.techbridge.com/jobs/business-development-senior',
    'San Francisco, CA',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Business Development Manager',
    'NextStep Enterprises',
    'Experience in international markets, business strategy, and key account management.',
    'Mid-Level',
    '2024-11-20',
    'About the Job: NextStep Enterprises is seeking a Mid-Level Business Development Manager to help us expand into international markets. In this role, you will be responsible for identifying new business opportunities, managing key accounts, and developing strategies that increase our market share globally. You will work closely with our executive team to ensure that our business development efforts align with our long-term growth strategy. As a Business Development Manager at NextStep, you will be the driving force behind our international expansion efforts, working to build relationships with clients and partners in key regions. You will be responsible for identifying new markets, developing entry strategies, and negotiating contracts with key stakeholders. Key Responsibilities: In this role, you will be responsible for managing a portfolio of key accounts, developing business development strategies, and working closely with cross-functional teams to ensure that our solutions meet the needs of our clients. You will also represent NextStep at industry events and conferences, networking with potential clients and partners to build new relationships. Growth Opportunities: NextStep offers a dynamic work environment with ample opportunities for growth. As a Mid-Level Business Development Manager, you will have the opportunity to move into more senior roles, such as Director of Business Development or Sales Manager. We provide ongoing training and professional development to help you succeed in your role. We Offer: A competitive salary, commission-based incentives, health benefits, and a collaborative work environment. Join us at NextStep and be a part of a company that is transforming the way businesses operate in international markets!',
    'https://www.nextstep.com/jobs/business-development-mid',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Business Development Manager',
    'SalesDrive Corp',
    'Experience in sales leadership, client relationship management, and strategic planning.',
    'Senior-Level',
    '2024-11-30',
    'About the Job: SalesDrive Corp is looking for a Senior Business Development Manager to lead our sales and business development efforts. As a key member of the team, you will be responsible for developing and executing business development strategies, managing key client relationships, and driving revenue growth. You will also be responsible for identifying new business opportunities and expanding our market presence. As a Senior Business Development Manager, you will work closely with our executive team to develop and implement strategies that align with our long-term growth goals. You will be responsible for managing a portfolio of key accounts, negotiating high-value contracts, and ensuring that we meet our revenue targets. Key Responsibilities: In this role, you will lead the sales process from lead generation to deal closure, working closely with cross-functional teams to ensure that our solutions meet the needs of our clients. You will also be responsible for developing and managing a sales pipeline, identifying new business opportunities, and building relationships with key stakeholders. Growth Opportunities: At SalesDrive Corp, we believe in fostering leadership and providing opportunities for growth. As a Senior Business Development Manager, you will have the opportunity to move into more senior leadership roles, such as Director of Sales or Vice President of Business Development. We Offer: A highly competitive salary, performance-based bonuses, and comprehensive health and retirement benefits. Join SalesDrive Corp and be a part of a company that is transforming the way businesses operate!',
    'https://www.salesdrive.com/jobs/business-development-senior',
    'Toronto, Canada',
    'Canada'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'AI/ML Engineer',
    'AI Solutions',
    'Experience with TensorFlow, PyTorch, and machine learning algorithms. Knowledge of AWS or GCP is preferred.',
    'Mid-Level',
    '2024-12-01',
    'About the Job: AI Solutions is hiring a Mid-Level AI/ML Engineer to join our team and work on cutting-edge machine learning models and AI-driven solutions. As an AI/ML Engineer, you will have the opportunity to work with some of the brightest minds in the field, developing models that power real-world applications in industries such as finance, healthcare, and retail. You will work on building, training, and deploying machine learning models using frameworks such as TensorFlow and PyTorch. You will also be responsible for ensuring that our models are scalable and can handle large volumes of data. In addition, you will collaborate with cross-functional teams to deploy models into production environments, using cloud platforms like AWS and GCP. Key Responsibilities: In this role, you will work on developing machine learning models, training neural networks, and optimizing models for performance. You will also be responsible for deploying models into production and working with DevOps teams to ensure scalability and reliability. Your day-to-day tasks will involve working with large datasets, conducting feature engineering, and tuning model hyperparameters. Growth Opportunities: AI Solutions offers numerous growth opportunities, including the chance to move into more senior roles, such as Senior AI/ML Engineer or Technical Lead. We also offer opportunities for professional development, including access to conferences, workshops, and mentorship programs. We Offer: A highly competitive salary, comprehensive health and dental benefits, and a flexible work environment. Join AI Solutions and be a part of a team that is transforming industries with AI-driven innovation!',
    'https://www.aisolutions.com/jobs/ai-ml-engineer-mid',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'AI/ML Engineer',
    'AI Solutions',
    'Experience with TensorFlow, PyTorch, and machine learning algorithms. Knowledge of AWS or GCP is preferred.',
    'Mid-Level',
    '2024-12-01',
    'About the Job: AI Solutions is hiring a Mid-Level AI/ML Engineer to join our team and work on cutting-edge machine learning models and AI-driven solutions. As an AI/ML Engineer, you will have the opportunity to work with some of the brightest minds in the field, developing models that power real-world applications in industries such as finance, healthcare, and retail. You will work on building, training, and deploying machine learning models using frameworks such as TensorFlow and PyTorch. You will also be responsible for ensuring that our models are scalable and can handle large volumes of data. In addition, you will collaborate with cross-functional teams to deploy models into production environments, using cloud platforms like AWS and GCP. Key Responsibilities: In this role, you will work on developing machine learning models, training neural networks, and optimizing models for performance. You will also be responsible for deploying models into production and working with DevOps teams to ensure scalability and reliability. Your day-to-day tasks will involve working with large datasets, conducting feature engineering, and tuning model hyperparameters. Growth Opportunities: AI Solutions offers numerous growth opportunities, including the chance to move into more senior roles, such as Senior AI/ML Engineer or Technical Lead. We also offer opportunities for professional development, including access to conferences, workshops, and mentorship programs. We Offer: A highly competitive salary, comprehensive health and dental benefits, and a flexible work environment. Join AI Solutions and be a part of a team that is transforming industries with AI-driven innovation!',
    'https://www.aisolutions.com/jobs/ai-ml-engineer-mid',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'AI/ML Engineer',
    'DeepMind Innovations',
    'Proficiency in deep learning frameworks (TensorFlow, PyTorch) and working with large datasets.',
    'Senior-Level',
    '2024-11-25',
    'About the Job: DeepMind Innovations is seeking a Senior AI/ML Engineer to lead the development of cutting-edge AI models for some of the most complex challenges in AI research today. You will join a dynamic team of researchers and engineers who are pushing the boundaries of artificial intelligence and machine learning. Our projects range from deep learning and reinforcement learning to natural language processing (NLP) and computer vision. As a Senior AI/ML Engineer, you will work closely with our research team to design, train, and deploy state-of-the-art machine learning models that drive our AI initiatives. You will be responsible for handling large datasets, developing efficient algorithms, and optimizing models for real-world applications. Your expertise in TensorFlow, PyTorch, and other AI tools will be critical to the success of our projects. Key Responsibilities: In this role, you will lead AI model development, from data preprocessing and model training to deployment and scaling. You will work with large datasets and collaborate with cross-functional teams to deploy models into production. You will also mentor junior engineers and contribute to the overall AI strategy at DeepMind. Growth Opportunities: DeepMind offers exciting opportunities for career growth. As a senior engineer, you will have the chance to take on leadership roles within the team, driving key AI projects and shaping the future of AI innovation at DeepMind. We Offer: A highly competitive salary, stock options, comprehensive health benefits, and the flexibility to work remotely. DeepMind is committed to fostering a collaborative and innovative work environment where you can grow and thrive. Join us and be part of the future of AI.',
    'https://www.deepmindinnovations.com/jobs/ai-ml-engineer-senior',
    'San Francisco, CA',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'AI/ML Engineer',
    'FutureAI Labs',
    'Experience with NLP models, computer vision, and reinforcement learning techniques.',
    'Mid-Level',
    '2024-12-10',
    'About the Job: FutureAI Labs is seeking a Mid-Level AI/ML Engineer to develop innovative AI solutions in natural language processing (NLP), computer vision, and reinforcement learning. You will work on advanced AI models that are used to solve real-world problems across various industries, including healthcare, retail, and finance. In this role, you will collaborate with a team of AI researchers and engineers to design and deploy machine learning models that drive our AI initiatives. You will have the opportunity to work with cutting-edge tools such as TensorFlow, PyTorch, and cloud platforms like AWS and GCP. Your work will involve building models that process large datasets, improve AI decision-making, and enhance the accuracy of our algorithms. Key Responsibilities: You will be responsible for developing and deploying NLP and computer vision models, working with large datasets, and optimizing models for real-time performance. You will also contribute to research initiatives in reinforcement learning and collaborate with cross-functional teams to implement AI-driven solutions. Growth Opportunities: FutureAI Labs offers numerous opportunities for professional development and growth. As you gain experience, you will have the opportunity to take on more responsibility, lead AI projects, and contribute to the development of new AI technologies. We Offer: A competitive salary, comprehensive health benefits, and a collaborative work environment that fosters innovation. Join FutureAI Labs and help shape the future of artificial intelligence!',
    'https://www.futureai.com/jobs/ai-ml-engineer-mid',
    'New York, NY',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'AI/ML Engineer',
    'QuantAI',
    'Proficiency in Python, machine learning algorithms, and working knowledge of cloud services (AWS, GCP).',
    'Entry-Level',
    '2024-12-15',
    'About the Job: QuantAI is hiring an Entry-Level AI/ML Engineer to assist in developing machine learning models and AI-driven systems for financial services. This is an exciting opportunity to join a fast-paced company that is leveraging AI to transform the financial industry. As an Entry-Level AI/ML Engineer, you will work with large financial datasets, building models that predict market trends, optimize trading strategies, and improve risk management. You will have the opportunity to work with Python, TensorFlow, and cloud services such as AWS and GCP. You will also collaborate with senior engineers and data scientists to ensure that our AI models are scalable, reliable, and provide valuable insights for our clients. Key Responsibilities: You will be responsible for developing and training machine learning models, conducting data analysis, and deploying models into production environments. You will also collaborate with other teams to optimize the performance of our AI systems. Growth Opportunities: At QuantAI, we offer a clear career path for growth. As an Entry-Level Engineer, you will have the opportunity to take on more responsibility, develop your technical skills, and contribute to the company’s overall AI strategy. We Offer: A competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely. Join QuantAI and be part of a company that is revolutionizing the financial industry with AI!',
    'https://www.quantai.com/jobs/ai-ml-engineer-entry',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'AI/ML Engineer',
    'TechAI Labs',
    'Experience with deep learning, data science, and AI model deployment. Knowledge of cloud platforms is a plus.',
    'Senior-Level',
    '2024-11-30',
    'About the Job: TechAI Labs is seeking a Senior AI/ML Engineer to lead the design and implementation of AI models for complex systems in industries such as healthcare, finance, and logistics. As a Senior Engineer, you will be responsible for developing deep learning models, building AI-driven products, and deploying models into cloud environments. You will work closely with a team of data scientists and software engineers to ensure that our AI solutions are scalable, reliable, and meet the needs of our clients. Your expertise in deep learning, data science, and cloud platforms will be critical to the success of our projects. Key Responsibilities: In this role, you will lead the development of AI models, collaborate with cross-functional teams, and ensure that our AI solutions are optimized for performance. You will also mentor junior engineers and contribute to the overall AI strategy at TechAI Labs. Growth Opportunities: At TechAI Labs, we offer numerous opportunities for growth and leadership. As a Senior Engineer, you will have the opportunity to take on more responsibility, lead AI projects, and contribute to the company’s long-term AI vision.
We Offer: A highly competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely. Join TechAI Labs and help shape the future of AI-driven innovation!',
    'https://www.techaiglabs.com/jobs/ai-ml-engineer-senior',
    'Toronto, Canada',
    'Canada'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Financial Analyst',
    'Capital Advisors',
    'Proficiency in financial modeling, data analysis, and Excel. Experience with PowerBI or Tableau is a plus.',
    'Entry-Level',
    '2024-12-01',
    'About the Job: Capital Advisors is seeking an Entry-Level Financial Analyst to join our dynamic team. As a Financial Analyst, you will be responsible for analyzing financial data, building financial models, and providing insights to support business decision-making. You will work closely with senior analysts and finance managers to provide recommendations on investments, budgeting, and forecasting. Your role will involve conducting financial analysis, preparing financial reports, and presenting findings to stakeholders. You will also work with tools such as Excel, PowerBI, and Tableau to create data visualizations that help drive business strategies. Key Responsibilities: In this role, you will assist in developing financial models, conducting variance analysis, and preparing reports for management. You will also work on budgeting and forecasting, helping the company make informed financial decisions. Growth Opportunities: As an Entry-Level Financial Analyst, you will have the opportunity to grow within the company. Capital Advisors offers training and professional development opportunities to help you advance in your career. We Offer: A competitive salary, health benefits, and a collaborative work environment. Join Capital Advisors and be part of a team that is shaping the future of financial services!',
    'https://www.capitaladvisors.com/jobs/financial-analyst-entry',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Financial Analyst',
    'FinTech Global',
    'Experience with financial modeling, Excel, and SQL. Familiarity with financial forecasting techniques is required.',
    'Mid-Level',
    '2024-12-15',
    'About the Job: FinTech Global is hiring a Mid-Level Financial Analyst to develop financial models and contribute to strategic financial planning. In this role, you will analyze financial data, create forecasts, and work closely with cross-functional teams to support business decisions. Your expertise in Excel, SQL, and financial analysis will be crucial to driving the company’s financial success. You will collaborate with senior finance professionals to provide insights into profitability, cost optimization, and risk management. You will also play a key role in developing financial strategies that align with the company’s long-term goals. Key Responsibilities: You will be responsible for financial forecasting, variance analysis, and preparing financial reports. You will also develop models that support decision-making and provide recommendations to management on financial strategies. Growth Opportunities: At FinTech Global, we provide opportunities for growth and advancement. As you gain experience, you will have the opportunity to take on leadership roles within the finance team. We Offer: A competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely or in our New York office. Join FinTech Global and be part of a company that is transforming financial services!',
    'https://www.fintechglobal.com/jobs/financial-analyst-mid',
    'New York, NY',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Financial Analyst',
    'WealthPoint',
    'Proficiency in data analysis, financial modeling, and tools such as Excel and SQL.',
    'Senior-Level',
    '2024-12-05',
    'About the Job: WealthPoint is looking for a Senior Financial Analyst to lead complex financial modeling and provide insights that drive strategic decisions. In this role, you will work with senior management to analyze financial data, create forecasts, and develop strategies that support business growth. You will lead a team of analysts, providing mentorship and guidance as they develop their skills. You will also be responsible for preparing financial reports, conducting risk assessments, and presenting findings to stakeholders. Key Responsibilities: As a Senior Financial Analyst, you will lead the financial analysis process, develop complex models, and provide recommendations to management. You will also work on budgeting, forecasting, and variance analysis. Growth Opportunities: WealthPoint offers numerous opportunities for career growth. As a senior member of the team, you will have the opportunity to move into leadership roles and contribute to the company’s overall financial strategy. We Offer: A highly competitive salary, performance-based bonuses, and comprehensive health and retirement benefits. Join WealthPoint and be part of a team that is shaping the future of financial services!',
    'https://www.wealthpoint.com/jobs/financial-analyst-senior',
    'Toronto, Canada',
    'Canada'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Financial Analyst',
    'Economy Insight',
    'Experience with financial forecasting, modeling, and reporting. Proficiency with Excel and data visualization tools.',
    'Mid-Level',
    '2024-11-30',
    'About the Job: Economy Insight is hiring a Mid-Level Financial Analyst to assist in developing financial reports and models that support our clients’ financial decision-making processes. You will work with a talented team of analysts and finance professionals to provide insights into financial performance, risk management, and investment strategies. You will be responsible for analyzing financial data, building financial models, and preparing reports for clients and internal stakeholders. You will also collaborate with cross-functional teams to ensure that our financial insights align with business goals. Key Responsibilities: In this role, you will develop financial models, conduct variance analysis, and prepare financial reports. You will also provide recommendations to management on financial strategies and investment opportunities. Growth Opportunities: At Economy Insight, we offer a clear path for growth. As you gain experience, you will have the opportunity to take on more responsibility and contribute to the company’s overall financial strategy. We Offer: A competitive salary, comprehensive health and retirement benefits, and a collaborative work environment. Join Economy Insight and be part of a team that is transforming the financial services industry!',
    'https://www.economyinsight.com/jobs/financial-analyst-mid',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Financial Analyst',
    'Global Investments',
    'Proficiency in Excel, SQL, and financial modeling. Experience with data visualization tools like PowerBI is a plus.',
    'Entry-Level',
    '2024-12-20',
    'About the Job: Global Investments is seeking an Entry-Level Financial Analyst to assist in financial data analysis and business strategy. In this role, you will work with senior analysts to analyze financial data, build models, and provide insights that support decision-making. You will also work on budgeting, forecasting, and risk analysis. Key Responsibilities: You will assist in developing financial models, preparing reports, and analyzing financial data. You will also work with senior analysts to provide recommendations to management on financial strategies and investment opportunities. Growth Opportunities: At Global Investments, we offer numerous opportunities for growth. As you gain experience, you will have the opportunity to take on more responsibility and contribute to the company’s financial strategy. We Offer: A competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely or in our London office. Join Global Investments and be part of a team that is shaping the future of the financial services industry!',
    'https://www.globalinvestments.com/jobs/financial-analyst-entry',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Business Analyst',
    'Strategy Corp',
    'Proficiency in business analysis, data modeling, and stakeholder management.',
    'Mid-Level',
    '2024-12-01',
    'About the Job: Strategy Corp is seeking a Mid-Level Business Analyst to assist in analyzing business processes, identifying inefficiencies, and providing recommendations to improve operations. In this role, you will work closely with stakeholders to gather requirements, develop solutions, and ensure that business objectives are met. You will be responsible for conducting business process analysis, developing data models, and preparing reports for management. You will also collaborate with cross-functional teams to implement solutions that improve business performance. Key Responsibilities: You will work on business analysis, process improvement, and stakeholder management. You will also develop business models, conduct data analysis, and provide recommendations to management. Growth Opportunities: Strategy Corp offers numerous opportunities for career growth. As you gain experience, you will have the opportunity to move into more senior roles, such as Senior Business Analyst or Project Manager. We Offer: A competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely. Join Strategy Corp and be part of a team that is shaping the future of business strategy!',
    'https://www.strategycorp.com/jobs/business-analyst-mid',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Data Analyst',
    'Insight Solutions',
    'Experience with data analysis, Excel, and SQL. Familiarity with data visualization tools like PowerBI is a plus.',
    'Entry-Level',
    '2024-11-30',
    'About the Job: Insight Solutions is hiring an Entry-Level Data Analyst to work on analyzing datasets and developing reports for clients across various industries. In this role, you will be responsible for data collection, cleaning, and analysis. You will also create data visualizations using tools such as PowerBI to communicate insights to stakeholders. Key Responsibilities: You will assist in data analysis, report development, and data visualization. You will also work with senior analysts to develop insights that support business decision-making. Growth Opportunities: At Insight Solutions, we offer a clear career path for growth. As you gain experience, you will have the opportunity to take on more responsibility and contribute to the company’s data strategy. We Offer: A competitive salary, comprehensive health benefits, and the flexibility to work remotely or in our New York office. Join Insight Solutions and be part of a company that is transforming the way businesses use data!',
    'https://www.insightsolutions.com/jobs/data-analyst-entry',
    'New York, NY',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Marketing Analyst',
    'Bright Marketing',
    'Experience with marketing analytics, tools like Google Analytics, and working knowledge of Excel and SQL.',
    'Mid-Level',
    '2024-12-05',
    'About the Job: Bright Marketing is seeking a Mid-Level Marketing Analyst to support the marketing team in campaign analysis and performance reporting. In this role, you will work on analyzing marketing data, developing insights, and providing recommendations to improve campaign effectiveness. Key Responsibilities: You will conduct marketing data analysis, develop reports, and provide recommendations for campaign improvement. You will also work with tools such as Google Analytics and SQL to track performance and generate insights. Growth Opportunities: Bright Marketing offers numerous opportunities for career growth. As you gain experience, you will have the opportunity to take on more responsibility and contribute to the company’s marketing strategy. We Offer: A competitive salary, comprehensive health benefits, and a collaborative work environment. Join Bright Marketing and be part of a company that is transforming the marketing industry!',
    'https://www.brightmarketing.com/jobs/marketing-analyst-mid',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Business Analyst',
    'ConsultTech',
    'Experience in business process analysis, data modeling, and stakeholder communication.',
    'Senior-Level',
    '2024-11-25',
    'About the Job: ConsultTech is looking for a Senior Business Analyst to lead efforts in analyzing business processes and driving strategic decisions. You will work closely with stakeholders to gather requirements, identify inefficiencies, and develop solutions that improve business performance. Key Responsibilities: As a Senior Business Analyst, you will lead business process analysis, develop data models, and provide recommendations to management. You will also work with cross-functional teams to implement solutions that drive business growth. Growth Opportunities: ConsultTech offers numerous opportunities for career growth. As a senior member of the team, you will have the opportunity to take on leadership roles and contribute to the company’s overall business strategy. We Offer: A highly competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely. Join ConsultTech and be part of a team that is transforming the way businesses operate!',
    'https://www.consulttech.com/jobs/business-analyst-senior',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Financial Analyst',
    'EcoInvest',
    'Proficiency in financial analysis, Excel, SQL, and working with financial models.',
    'Mid-Level',
    '2024-11-30',
    'About the Job: EcoInvest is hiring a Mid-Level Financial Analyst to support the finance team in developing financial reports and models that drive business decision-making. In this role, you will be responsible for analyzing financial data, preparing reports, and providing insights that support business strategy. Key Responsibilities: You will assist in financial analysis, model development, and reporting. You will also collaborate with cross-functional teams to ensure that our financial insights align with business objectives. Growth Opportunities: At EcoInvest, we provide opportunities for growth and professional development. As you gain experience, you will have the opportunity to take on more responsibility and contribute to the company’s overall financial strategy. We Offer: A competitive salary, comprehensive health benefits, and a collaborative work environment. Join EcoInvest and be part of a company that is shaping the future of sustainable finance!',
    'https://www.ecoinvest.com/jobs/financial-analyst-mid',
    'Toronto, Canada',
    'Canada'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Project Leader',
    'Tech Pioneers',
    'Experience managing large-scale projects, knowledge of project management tools, and excellent communication skills.',
    'Senior-Level',
    '2024-12-01',
    'About the Job: Tech Pioneers is looking for a Senior Project Leader to oversee the development and execution of large-scale technology projects. As a Senior Project Leader, you will be responsible for managing project timelines, coordinating cross-functional teams, and ensuring that projects are delivered on time and within budget. Key Responsibilities: In this role, you will manage project teams, develop project plans, and ensure that project objectives are met. You will also communicate with stakeholders, provide updates on project progress, and mitigate risks. Growth Opportunities: Tech Pioneers offers numerous opportunities for growth and leadership. As a Senior Project Leader, you will have the opportunity to move into executive roles and contribute to the company’s long-term vision. We Offer: A highly competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely. Join Tech Pioneers and lead cutting-edge technology projects that shape the future of innovation!',
    'https://www.techpioneers.com/jobs/project-leader-senior',
    'San Francisco, CA',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Project Leader',
    'InnoTech',
    'Experience managing technology projects, proficiency in project management software, and strong leadership skills.',
    'Mid-Level',
    '2024-12-10',
    'About the Job: InnoTech is seeking a Mid-Level Project Leader to manage technology projects from concept to delivery. In this role, you will work with cross-functional teams to ensure that project objectives are met, timelines are adhered to, and budgets are maintained. You will also be responsible for providing regular updates to stakeholders and ensuring that project risks are mitigated. Key Responsibilities: You will be responsible for managing project teams, developing project plans, and ensuring that deliverables are met on time and within budget. You will also communicate with clients and internal stakeholders to provide updates on project progress. Growth Opportunities: At InnoTech, we offer numerous opportunities for professional development. As you gain experience, you will have the opportunity to take on more responsibility and lead larger, more complex projects. We Offer: A competitive salary, comprehensive health benefits, and a collaborative work environment. Join InnoTech and lead projects that drive technology innovation!',
    'https://www.innotech.com/jobs/project-leader-mid',
    'New York, NY',
    'USA'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Project Leader',
    'BrightTech Solutions',
    'Proficiency in project management methodologies (Agile, Waterfall), experience leading teams, and strong problem-solving skills.',
    'Mid-Level',
    '2024-12-05',
    'About the Job: BrightTech Solutions is hiring a Mid-Level Project Leader to oversee the planning, execution, and delivery of technology projects. In this role, you will be responsible for leading cross-functional teams, ensuring that project objectives are met, and managing stakeholder expectations. Key Responsibilities: You will develop project plans, lead project teams, and ensure that projects are delivered on time and within budget. You will also work with stakeholders to ensure that project goals are aligned with business objectives. Growth Opportunities: BrightTech Solutions offers numerous opportunities for career growth. As you gain experience, you will have the opportunity to move into more senior project management roles and contribute to the company’s long-term strategy. We Offer: A competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely. Join BrightTech Solutions and lead projects that are transforming the technology landscape!',
    'https://www.brighttechsolutions.com/jobs/project-leader-mid',
    'London, UK',
    'United Kingdom'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Project Leader',
    'GreenTech Innovations',
    'Experience leading sustainability-focused projects, proficiency in project management tools, and excellent communication skills.',
    'Senior-Level',
    '2024-12-20',
    'About the Job: GreenTech Innovations is hiring a Senior Project Leader to lead sustainability-focused projects in the renewable energy sector. In this role, you will be responsible for managing cross-functional teams, ensuring that project objectives are met, and communicating with stakeholders to provide updates on project progress. Key Responsibilities: You will lead the development and execution of sustainability-focused projects, manage project teams, and ensure that projects are delivered on time and within budget. You will also work with stakeholders to ensure that project goals are aligned with business objectives. Growth Opportunities: GreenTech Innovations offers numerous opportunities for career growth. As a Senior Project Leader, you will have the opportunity to take on more responsibility and contribute to the company’s sustainability strategy.We Offer: A highly competitive salary, comprehensive health and retirement benefits, and the flexibility to work remotely. Join GreenTech Innovations and lead projects that are shaping the future of sustainability!',
    'https://www.greentechinnovations.com/jobs/project-leader-senior',
    'Berlin',
    'Germany'
);

INSERT INTO joblistings (title, company, requirements, expected_experience, last_chance, listing, link, location, country)
VALUES (
    'Project Leader',
    'TechForce Global',
    'Experience managing global projects, knowledge of project management tools, and strong leadership skills.',
    'Mid-Level',
    '2024-12-15',
    'About the Job: TechForce Global is hiring a Mid-Level Project Leader to oversee the execution of global technology projects. In this role, you will work with cross-functional teams in multiple regions to ensure that project objectives are met, timelines are adhered to, and risks are mitigated. Key Responsibilities: You will be responsible for managing project teams, developing project plans, and ensuring that deliverables are met on time and within budget. You will also work with stakeholders across different regions to ensure project alignment with business goals. Growth Opportunities: TechForce Global offers numerous opportunities for professional development. As you gain experience, you will have the opportunity to take on larger, more complex projects and move into senior leadership roles.We Offer: A competitive salary, comprehensive health benefits, and the flexibility to work remotely. Join TechForce Global and lead projects that are driving global innovation!',
    'https://www.techforceglobal.com/jobs/project-leader-mid',
    'Toronto, Canada',
    'Canada'
);

