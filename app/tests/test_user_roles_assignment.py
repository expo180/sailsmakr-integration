import unittest
from flask import current_app
from app import create_app, db
from app.models import User, Role

class UserRoleAssignmentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_ceo_role_assignment(self):
        ceo_email = current_app.config['COMPANY_CEO']
        ceo_user = User(email=ceo_email, password='password')
        db.session.add(ceo_user)
        db.session.commit()
        self.assertEqual(ceo_user.role.name, 'CEO')

    def test_hr_manager_role_assignment(self):
        hr_email = current_app.config['COMPANY_HR_MANAGER']
        hr_user = User(email=hr_email, password='password')
        db.session.add(hr_user)
        db.session.commit()
        self.assertEqual(hr_user.role.name, 'HR Manager')

    def test_employee_role_assignment(self):
        agent_email = 'agent1@example.com'  # Assuming this is in the AGENTS_EMAILS list
        agent_user = User(email=agent_email, password='password')
        db.session.add(agent_user)
        db.session.commit()
        self.assertEqual(agent_user.role.name, 'Employee')

    def test_default_user_role_assignment(self):
        default_user_email = 'newuser@example.com'
        default_user = User(email=default_user_email, password='password')
        db.session.add(default_user)
        db.session.commit()
        self.assertEqual(default_user.role.name, 'User')

if __name__ == '__main__':
    unittest.main()
