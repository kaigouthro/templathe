class TaskStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_task(self, task: str, completed: bool):
        with open(self.file_path, 'a') as file:
            file.write(f'{task},{completed}\n')

    def get_all_tasks(self):
        tasks = []
        with open(self.file_path, 'r') as file:
            for line in file:
                task, completed = line.strip().split(',')
                tasks.append({'task': task, 'completed': completed == 'True'})
        return tasks

    def get_completed_tasks(self):
        tasks = self.get_all_tasks()
        return [task for task in tasks if task['completed']]

    def get_incomplete_tasks(self):
        tasks = self.get_all_tasks()
        return [task for task in tasks if not task['completed']]


# Create an instance of TaskStorage
storage = TaskStorage('task_data.txt')

# Save tasks
storage.save_task('Task 1', True)
storage.save_task('Task 2', False)
storage.save_task('Task 3', True)

# Get all tasks
all_tasks = storage.get_all_tasks()
print(all_tasks)

# Get completed tasks
completed_tasks = storage.get_completed_tasks()
print(completed_tasks)
