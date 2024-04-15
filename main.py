from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

def read_tasks():
    tasks = []
    with open('tasks.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tasks.append(row)
    return tasks

def write_tasks(tasks):
    with open('tasks.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'description', 'status', 'user']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)

def create_tasks_file_if_not_exists():
    if not os.path.exists('tasks.csv'):
        with open('tasks.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'description', 'status', 'user']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

@app.route('/')
def index():
    create_tasks_file_if_not_exists()
    tasks = read_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    tasks = read_tasks()
    new_task = {
        'id': len(tasks) + 1,
        'title': request.form['title'],
        'description': request.form['description'],
        'status': request.form['status'],
        'user': request.form['user']
    }
    tasks.append(new_task)
    write_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    tasks = read_tasks()
    if request.method == 'POST':
        for task in tasks:
            if task['id'] == str(task_id):
                task['title'] = request.form['title']
                task['description'] = request.form['description']
                task['status'] = request.form['status']
                task['user'] = request.form['user']
                break
        write_tasks(tasks)
        return redirect(url_for('index'))
    else:
        for task in tasks:
            if task['id'] == str(task_id):
                return render_template('edit_task.html', task=task)
        return 'Užduotis nerasta', 404

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    tasks = read_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == str(task_id):
            del tasks[i]
            break
    write_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/change_status/<int:task_id>', methods=['POST'])
def change_status(task_id):
    tasks = read_tasks()
    for task in tasks:
        if task['id'] == str(task_id):
            task['status'] = request.form['status']
            break
    write_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)