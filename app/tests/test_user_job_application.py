def create_job_application():
    job = Job.query.first()
    user = User.query.first()

    if job and user:
        application = JobApplication(
            applicant_first_name='John',
            applicant_last_name='Doe',
            applicant_email_address='john@example.com',
            applicant_location='Paris',
            motivation='I am highly motivated to work in this position.',
            linkedin_url='https://www.linkedin.com/in/johndoe/',
            github_url='https://github.com/johndoe',
            dribble_url='https://dribbble.com/johndoe',
            date_of_birth=datetime(1990, 5, 15),
            apply_at=datetime.utcnow(),
            CV_url='https://example.com/johns_cv.pdf',
            user=user,
            job=job
        )

        db.session.add(application)
        db.session.commit()

        print("Job application created successfully!")
    else:
        print("Error: No job or user found in the database.")

