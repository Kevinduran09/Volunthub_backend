class Task:
    def __init__(self, id, title, status, description, priority, event_id, completed_by):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.priority = priority
        self.event_id = event_id
        self.completed_by = completed_by
