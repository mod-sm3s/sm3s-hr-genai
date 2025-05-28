# Paste the above SQL
# Ctrl + O to save, Ctrl + X to exit
-- Create the database

-- Create the database
CREATE DATABASE hr_assistant;

-- Use the database
USE hr_assistant;

-- Create the updated employees table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_name VARCHAR(100),
    employee_email VARCHAR(100),
    phone VARCHAR(20),
    position VARCHAR(100),
    skills TEXT,
    learning_track TEXT,
    certificates TEXT,
    joined_since DATE,
    years_experience INT,
    department VARCHAR(100)
);

-- Insert sample employee data
INSERT INTO employees (
    employee_name, employee_email, phone, position, skills, learning_track,
    certificates, joined_since, years_experience, department
) VALUES 
('Alice Johnson', 'alice@company.com', '123-456-7890', 'Data Scientist',
 'Python, SQL, Machine Learning', 'AI/ML', 'Coursera AI Cert',
 '2019-06-15', 5, 'Engineering'),

('Bob Smith', 'bob@company.com', '555-987-6543', 'Backend Developer',
 'Java, Spring, SQL', 'Full Stack Dev', 'Oracle Java SE 11',
 '2018-04-10', 7, 'Engineering'),

('Carol Davis', 'carol@company.com', '321-654-0987', 'HR Specialist',
 'Recruiting, Compliance', 'HR Ops', 'SHRM-CP',
 '2020-01-20', 4, 'Human Resources'),

('David Lee', 'david@company.com', '999-888-7777', 'DevOps Engineer',
 'Docker, Kubernetes, AWS', 'DevOps Mastery', 'AWS Solutions Architect',
 '2017-08-01', 8, 'DevOps'),

('Emma White', 'emma@company.com', '111-222-3333', 'ML Engineer',
 'TensorFlow, Python, PyTorch', 'Deep Learning Path', 'DeepLearning.ai',
 '2021-03-01', 3, 'AI Team'),

('Faisal Rahman', 'faisal@company.com', '222-333-4444', 'Business Analyst',
 'Excel, Power BI, SQL', 'Data Analysis', 'Google Data Cert',
 '2022-07-10', 2, 'Business'),

('Natalie Brooks', 'natalie@company.com', '777-888-9999', 'Frontend Developer',
 'JavaScript, React, HTML, CSS', 'Frontend Dev', 'Meta Frontend Cert',
 '2020-11-05', 4, 'Engineering'),

('Imran Khan', 'imran@company.com', '888-999-0000', 'Cloud Architect',
 'AWS, Azure, Terraform', 'Cloud Infra', 'Microsoft Azure Expert',
 '2016-02-12', 9, 'IT Operations');

